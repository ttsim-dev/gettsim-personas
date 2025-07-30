from __future__ import annotations

import datetime
import itertools
from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal

import numpy as np

from gettsim_personas.upsert import upsert_input_data

if TYPE_CHECKING:
    from gettsim_personas.typing import NestedData, NestedTargetDict


DEFAULT_PERSONA_START_DATE = datetime.date(1900, 1, 1)
DEFAULT_PERSONA_END_DATE = datetime.date(2100, 12, 31)


BottomOrTop = Literal["bottom", "top"]
BruttolohnLinspaceSpec = dict[int, dict[BottomOrTop, float]]


@dataclass(frozen=True)
class Persona:
    description: str
    input_data_tree: NestedData
    tt_targets_tree: NestedTargetDict
    start_date: datetime.date = DEFAULT_PERSONA_START_DATE
    end_date: datetime.date = DEFAULT_PERSONA_END_DATE


@dataclass(frozen=True)
class PersonaCollection:
    """A collection of all available personas for a given path."""

    personas: list[Persona]
    not_implemented_error: PersonaNotImplementedError | None = None

    def __call__(
        self,
        *,
        policy_date_str: str,
        n_points: int = 1,
        bruttolohn_m_linspace_spec: BruttolohnLinspaceSpec | None = None,
    ) -> Persona:
        """Return a persona active at a given date.

        Args:
            policy_date_str:
                Date as string (YYYY-MM-DD)
            n_points:
                Optional, number of points to sample from the linspace specified via
                bruttolohn_m.
            bruttolohn_m_linspace_spec:
                Optional, if provided, earnings are sampled from the linspace specified
                here.
        """
        date = datetime.date.fromisoformat(policy_date_str)
        base_persona = None
        for persona in self.personas:
            if persona.start_date <= date <= persona.end_date:
                base_persona = persona
        if not base_persona:
            if isinstance(self.not_implemented_error, PersonaNotImplementedError):
                raise self.not_implemented_error
            msg = (
                f"No persona found for date {policy_date_str}. "
                "Consider using a different one."
            )
            raise PersonaNotImplementedError(msg)

        if bruttolohn_m_linspace_spec:
            return persona_with_upserted_bruttolohn(
                base_persona=base_persona,
                n_points=n_points,
                bruttolohn_m_linspace_spec=bruttolohn_m_linspace_spec,
            )
        return base_persona

    def __post_init__(self):
        _fail_if_active_dates_overlap(self.personas)


@dataclass
class _GETTSIMPersonas:
    """A collection of all available personas."""

    persona_collections: dict = None

    def __post_init__(self):
        """Set attributes for each persona after initialization."""
        # This avoids a circular import.
        from gettsim_personas.orig_personas import orig_personas  # noqa: PLC0415

        self.persona_collections = orig_personas()

        for path, persona in self.persona_collections.items():
            self._set_nested_attribute(path, persona)

    def _set_nested_attribute(self, path: tuple[str, ...], value: object) -> None:
        """Recursively set persona by path.

        Creates an intermediate object for each path level and sets the persona at the
        last level. Useful for IDE autocompletion.
        """

        def set_nested_attr(obj, path, value):
            if len(path) == 1:
                setattr(obj, path[0], value)
            else:
                if not hasattr(obj, path[0]):
                    intermediate = type(
                        "PersonaLevel", (), {"_set_nested_attribute": set_nested_attr}
                    )()
                    setattr(obj, path[0], intermediate)
                else:
                    intermediate = getattr(obj, path[0])
                intermediate._set_nested_attribute(path[1:], value)  # noqa: SLF001

        set_nested_attr(self, path, value)

    def _all_personas(self) -> list[Persona]:
        return [
            p
            for p_collection in self.persona_collections.values()
            for p in p_collection.personas
        ]

    def personas_active_at_date(self, policy_date_str: str) -> PersonaCollection:
        """Get all personas active at a given date."""
        date = datetime.date.fromisoformat(policy_date_str)
        return PersonaCollection(
            personas=[
                persona
                for persona in self._all_personas()
                if persona.start_date <= date <= persona.end_date
            ]
        )


class PersonaNotImplementedError(BaseException):
    """Error to be raised if a persona is not implemented."""


def _fail_if_active_dates_overlap(personas: list[Persona]) -> None:
    """Fail if multiple personas are active at the same date."""
    if len(personas) > 1:
        for persona1, persona2 in itertools.combinations(personas, 2):
            # Check if date ranges overlap
            if (
                persona1.start_date <= persona2.end_date
                and persona2.start_date <= persona1.end_date
            ):
                msg = (
                    f"Multiple personas are active at the same date. "
                    f"Overlapping periods: {persona1.start_date} - {persona1.end_date} "
                    f"and {persona2.start_date} - {persona2.end_date}."
                )
                raise ValueError(msg)


def persona_with_upserted_bruttolohn(
    base_persona: Persona,
    n_points: int,
    bruttolohn_m_linspace_spec: BruttolohnLinspaceSpec,
) -> Persona:
    _fail_if_bruttolohn_m_linspace_spec_invalid(
        base_persona=base_persona,
        bruttolohn_m_linspace_spec=bruttolohn_m_linspace_spec,
    )
    p_id_to_bruttolohn_m_linspace = {
        p_id: np.linspace(
            bounds["bottom"],
            bounds["top"],
            n_points,
        )
        for p_id, bounds in bruttolohn_m_linspace_spec.items()
    }

    # Create alternating array by interleaving arrays from different p_ids
    bruttolohn_m_array = np.array(
        [
            value
            for pair in zip(*p_id_to_bruttolohn_m_linspace.values(), strict=False)
            for value in pair
        ]
    )

    upserted_input_data = upsert_input_data(
        input_data=base_persona.input_data_tree,
        data_to_upsert={
            "einnahmen": {"bruttolohn_m": bruttolohn_m_array},
        },
    )

    return Persona(
        description=base_persona.description,
        input_data_tree=upserted_input_data,
        tt_targets_tree=base_persona.tt_targets_tree,
        start_date=base_persona.start_date,
        end_date=base_persona.end_date,
    )


def _fail_if_bruttolohn_m_linspace_spec_invalid(
    base_persona: Persona,
    bruttolohn_m_linspace_spec: BruttolohnLinspaceSpec,
) -> None:
    """Fail if the bruttolohn_m_linspace_spec is invalid."""
    if not isinstance(bruttolohn_m_linspace_spec, dict):
        msg = "bruttolohn_m_linspace_spec must be a dictionary."
        raise TypeError(msg)
    keys_in_spec = set(bruttolohn_m_linspace_spec.keys())
    p_id_in_base_persona = set(base_persona.input_data_tree.get("p_id"))
    if keys_in_spec != p_id_in_base_persona:
        msg = (
            "You must specify linspace bounds for each p_id in the base_persona."
            "The following p_ids are in the base_persona: "
            f"{p_id_in_base_persona}"
            "The following p_ids are in the bruttolohn_m_linspace_spec: "
            f"{keys_in_spec}"
        )
        raise ValueError(msg)
    for bounds in bruttolohn_m_linspace_spec.values():
        if not isinstance(bounds, dict) or {"bottom", "top"} != set(bounds.keys()):
            msg = (
                "For each p_id in the bruttolohn_m_linspace_spec, you must specify "
                "a dictionary with keys 'bottom' and 'top'."
            )
            raise TypeError(msg)
        if bounds["bottom"] > bounds["top"]:
            msg = "The lower bound of the linspace must be less than the upper bound."
            raise ValueError(msg)
