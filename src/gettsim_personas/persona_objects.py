from __future__ import annotations

import datetime
import itertools
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gettsim_personas.typing import NestedData, NestedTargetDict


DEFAULT_PERSONA_START_DATE = datetime.date(1900, 1, 1)
DEFAULT_PERSONA_END_DATE = datetime.date(2100, 12, 31)


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

    def __call__(self, *, date_str: str) -> Persona:
        """Return a persona active at a given date.

        Args:
            date_str: Date as string (YYYY-MM-DD)
        """
        date = datetime.date.fromisoformat(date_str)

        for persona in self.personas:
            if persona.start_date <= date <= persona.end_date:
                return persona
        msg = f"No persona found for date {date_str}. Consider using a different one."
        raise NotImplementedError(msg)

    def __post_init__(self):
        _fail_if_active_dates_overlap(self.personas)


@dataclass
class GETTSIMPersonas:
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

    def personas_active_at_date(self, date_str: str) -> PersonaCollection:
        """Get all personas active at a given date."""
        date = datetime.date.fromisoformat(date_str)
        return PersonaCollection(
            personas=[
                persona
                for persona in self._all_personas()
                if persona.start_date <= date <= persona.end_date
            ]
        )


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
