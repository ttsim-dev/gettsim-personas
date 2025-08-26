from __future__ import annotations

import inspect
from dataclasses import dataclass, fields, make_dataclass
from pathlib import Path
from typing import TYPE_CHECKING, TypeAlias

import dags
import dags.tree as dt
import numpy as np
from ttsim.interface_dag_elements.orig_policy_objects import load_module
from ttsim.interface_dag_elements.shared import to_datetime

from _gettsim_personas.persona_elements import (
    DEFAULT_END_DATE,
    DEFAULT_START_DATE,
    PersonaDescription,
    PersonaInputElement,
    PersonaPIDElement,
    PersonaTargetElement,
    TimeDependentPersonaElement,
)
from _gettsim_personas.typing import PersonaElement
from _gettsim_personas.upsert import upsert_input_data

if TYPE_CHECKING:
    import datetime
    from types import ModuleType

    from _gettsim_personas.typing import DashedISOString, NestedData, NestedStrings

LinspaceGrid: TypeAlias = type


@dataclass(frozen=True)
class Persona:
    description: str
    policy_date: datetime.date
    evaluation_date: datetime.date
    input_data_tree: NestedData
    tt_targets_tree: NestedStrings

    def upsert_input_data(self, input_data_to_upsert: NestedData) -> Persona:
        """Upsert persona input data.

        Create a copy of this persona and **up**date or in**sert** input data. Useful if
        you want to obtain input data columns that vary over a range of values other
        than `('einnahmen', 'bruttolohn_m')`.

        Pass the array to be used for upserting as `input_data_to_upsert`. Note that the
        length of this array must be a multiple of the length of the original persona
        input data (because this function creates copies of the persona input data).

        The new households will have the exact same configuration as the original
        household, except for the variables you upserted and the IDs and pointers
        required by GETTSIM (these are not copied but set to reflect the same household
        structure as the base household for the copied households).

        Example:
        -------
        >>> from gettsim_personas import einkommensteuer_sozialabgaben
        >>> base_persona = einkommensteuer_sozialabgaben.Couple1Child(
        >>>     policy_date_str="2025-01-01",
        >>> )
        >>> data_to_upsert = {
        >>>     "einnahmen": {"bruttolohn_m": np.array([4, 5, 6, 7, 8, 9])},
        >>> }
        >>> upserted_persona = base_persona.upsert_input_data(data_to_upsert)
        >>> upserted_persona.input_data_tree
        >>> {
        >>>     "p_id": np.array([0, 1, 2, 3, 4, 5]),
        >>>     "p_id_elternteil_1": np.array([-1, -1, 0, -1, -1, 3]),
        >>>     "einnahmen": {"bruttolohn_m": np.array([4, 5, 6, 7, 8, 9])},
        >>> }

        Args:
            input_data_to_upsert:
                NestedData with data to be upserted.

        Returns:
            A new persona with upserted input data.
        """
        return Persona(
            description=self.description,
            policy_date=self.policy_date,
            evaluation_date=self.evaluation_date,
            input_data_tree=upsert_input_data(
                input_data=self.input_data_tree,
                data_to_upsert=input_data_to_upsert,
            ),
            tt_targets_tree=self.tt_targets_tree,
        )


@dataclass
class OrigPersonaOverTime:
    """A persona containing inputs and targets to use with GETTSIM."""

    path_to_persona_elements: Path
    start_date: datetime.date = DEFAULT_START_DATE
    end_date: datetime.date = DEFAULT_END_DATE
    error_if_not_implemented: str | None = None

    def __post_init__(self):
        p_id = next(
            el for el in self.orig_elements() if isinstance(el, PersonaPIDElement)
        )
        self.LinspaceGrid = make_linspace_grid_class(p_id.persona_size)
        self.LinspaceRange = LinspaceRange

    def __call__(
        self,
        *,
        policy_date_str: DashedISOString,
        evaluation_date_str: DashedISOString | None = None,
        bruttolohn_m_linspace_grid: LinspaceGrid | None = None,
    ) -> Persona:
        """An instance of persona for a given policy and evaluation date.

        Args:
            policy_date_str:
                The date of the policy environment.
            evaluation_date_str:
                (Optional) The date for which the persona is evaluated. If not provided,
                the policy date is used.
            bruttolohn_m_linspace_grid:
                (Optional) A linspace grid of einnahmen__bruttolohn_m. Use if you want
                to calculate taxes and transfers over a range of earnings. The grid
                specifies for each p_id a constant value or the range of earnings to be
                evaluated. Create the grid via the LinspaceGrid method of this class.

        Example:
            >>> from gettsim_personas.de.einkommensteuer_sozialabgaben import Couple1Child
            >>> persona = Couple1Child(
            ...     policy_date_str="2025-01-01",
            ...     evaluation_date_str="2025-01-01",
            ...     bruttolohn_m_linspace_grid=Couple1Child.LinspaceGrid(
            ...         p0=Couple1Child.LinspaceRange(bottom=0, top=10000),
            ...         p1=Couple1Child.LinspaceRange(bottom=0, top=10000),
            ...         p2=0,
            ...         n_points=100,
            ...     ),
            ... )

        Returns:
            A Persona object containing the persona's description, input data, and
            targets.
        """  # noqa: E501
        policy_date = to_datetime(policy_date_str)
        evaluation_date = (
            policy_date if not evaluation_date_str else to_datetime(evaluation_date_str)
        )

        self._fail_if_persona_not_implemented(policy_date)

        active_elements = self.active_elements(policy_date)
        qname_input_data = _get_qname_input_data(
            evaluation_date=evaluation_date,
            persona_input_elements=active_persona_input_elements(active_elements),
        )
        _fail_if_qname_input_data_differs_in_length_from_p_id_array(qname_input_data)

        if bruttolohn_m_linspace_grid:
            _fail_if_bruttolohn_m_linspace_grid_is_invalid(
                linspace_grid=bruttolohn_m_linspace_grid,
                p_id_array=qname_input_data["p_id"],
            )
            qname_input_data = upsert_with_bruttolohn_m_linspace_grid(
                qname_input_data=qname_input_data,
                bruttolohn_m_linspace_grid=bruttolohn_m_linspace_grid,
            )

        return Persona(
            description=active_description(active_elements).description,
            policy_date=policy_date,
            evaluation_date=evaluation_date,
            input_data_tree=dt.unflatten_from_qnames(qname_input_data),
            tt_targets_tree=dt.unflatten_from_qnames(
                active_tt_targets(active_elements)
            ),
        )

    def orig_elements(self) -> list[PersonaElement]:
        module = load_module(
            path=self.path_to_persona_elements,
            root=Path(__file__).parent.parent.parent,
        )
        persona_elements = load_persona_elements_from_module(module)
        _fail_if_not_exactly_one_p_id_array_in_persona_elements(
            persona_elements=persona_elements,
            path_to_persona_elements=self.path_to_persona_elements,
        )
        return persona_elements

    def active_elements(self, policy_date: datetime.date) -> list[PersonaElement]:
        active_elements: list[PersonaElement] = []
        for el in self.orig_elements():
            if isinstance(el, TimeDependentPersonaElement):
                if el.is_active(policy_date):
                    active_elements.append(el)
            elif isinstance(el, PersonaPIDElement):
                active_elements.append(el)
        _fail_if_active_tt_qnames_overlap(
            active_elements=active_elements,
            path_to_persona_elements=self.path_to_persona_elements,
        )
        _fail_if_not_exactly_one_description_is_active(
            active_elements=active_elements,
            path_to_persona_elements=self.path_to_persona_elements,
        )
        return active_elements

    def _fail_if_persona_not_implemented(
        self,
        policy_date: datetime.date,
    ) -> None:
        if not (self.start_date <= policy_date <= self.end_date):
            raise NotImplementedError(self.error_if_not_implemented)


@dataclass(frozen=True)
class LinspaceRange:
    bottom: float
    top: float


LinspaceParameter: TypeAlias = LinspaceRange | float | int


def active_persona_input_elements(
    active_elements: list[PersonaElement],
) -> dict[str, PersonaInputElement | PersonaPIDElement]:
    """Active input elements of a persona."""
    return {
        s.tt_qname: s
        for s in active_elements
        if isinstance(s, PersonaInputElement | PersonaPIDElement)
    }


def active_tt_targets(
    active_elements: list[PersonaElement],
) -> dict[str, PersonaTargetElement]:
    """Active target elements of a persona."""
    return {
        s.tt_qname: None for s in active_elements if isinstance(s, PersonaTargetElement)
    }


def active_description(active_elements: list[PersonaElement]) -> PersonaDescription:
    """Active description element of a persona."""
    return next(s for s in active_elements if isinstance(s, PersonaDescription))


def make_linspace_grid_class(size: int):
    """Dynamically create a LinspaceGrid dataclass for the given persona size.

    Example:
        LinspaceGrid = make_linspace_grid_class(3)
        grid = LinspaceGrid(p0=..., p1=..., p2=..., n_points=...)

    Parameters can be either LinspaceRange objects or numeric values:
        - LinspaceRange(bottom=1000, top=3000): creates a range from 1000 to 3000
        - 4000: creates a constant value of 4000 (no range)
    """
    fields = [(f"p{i}", LinspaceParameter) for i in range(size)]
    fields.append(("n_points", int))
    return make_dataclass(f"LinspaceGrid{size}PIDs", fields, frozen=True)


def upsert_with_bruttolohn_m_linspace_grid(
    qname_input_data: dict[str, np.ndarray],
    bruttolohn_m_linspace_grid: LinspaceGrid,
) -> dict[str, np.ndarray]:
    """Upsert the bruttolohn_m_linspace_grid into the qname_input_data."""
    linspace_by_p_id = {}
    for p_id in bruttolohn_m_linspace_grid.__dict__:
        if p_id == "n_points":
            continue

        param_value = bruttolohn_m_linspace_grid.__getattribute__(p_id)

        if isinstance(param_value, LinspaceRange):
            # Create a range from bottom to top
            linspace_by_p_id[p_id] = np.linspace(
                param_value.bottom,
                param_value.top,
                bruttolohn_m_linspace_grid.n_points,
            )
        else:
            # Create a constant array with the same value
            linspace_by_p_id[p_id] = np.full(
                bruttolohn_m_linspace_grid.n_points,
                float(param_value),
            )

    bruttolohn_m_grid = np.array(
        [
            value
            for pair in zip(*linspace_by_p_id.values(), strict=False)
            for value in pair
        ]
    )
    return upsert_input_data(
        input_data=qname_input_data,
        data_to_upsert={
            "einnahmen__bruttolohn_m": bruttolohn_m_grid,
        },
    )


def _get_qname_input_data(
    evaluation_date: datetime.date,
    persona_input_elements: dict[str, PersonaInputElement],
) -> dict[str, np.ndarray]:
    f = dags.concatenate_functions(
        functions=persona_input_elements,
        targets=list(persona_input_elements.keys()),
        return_type="dict",
    )
    args = dags.get_free_arguments(f)

    if args == ["evaluation_date"]:
        return f(evaluation_date=evaluation_date)
    if args:
        # We only support "evaluation_date" or no parameter at all for now
        msg = (
            f"The following parameters are needed to create the input data for this "
            f"persona: {args}. "
        )
        raise ValueError(msg)
    return f()


def load_persona_elements_from_module(
    module: ModuleType,
) -> list[PersonaElement]:
    persona_elements_in_this_module: list[PersonaElement] = []
    for _, obj in inspect.getmembers(module):
        if isinstance(obj, PersonaElement):
            persona_elements_in_this_module.append(obj)
    return persona_elements_in_this_module


def _fail_if_not_exactly_one_p_id_array_in_persona_elements(
    persona_elements: list[PersonaElement],
    path_to_persona_elements: Path,
) -> None:
    p_id_arrays = [el for el in persona_elements if isinstance(el, PersonaPIDElement)]
    if len(p_id_arrays) != 1:
        msg = (
            f"Expected exactly one p_id array in {path_to_persona_elements!s}. "
            f"Found {len(p_id_arrays)}."
        )
        raise ValueError(msg)


def _fail_if_not_exactly_one_description_is_active(
    active_elements: list[TimeDependentPersonaElement], path_to_persona_elements: Path
) -> None:
    descriptions = [s for s in active_elements if isinstance(s, PersonaDescription)]
    if len(descriptions) > 1:
        msg = (
            "More than one PersonaDescription is active at "
            f"{path_to_persona_elements!s}."
        )
        raise ValueError(msg)
    if len(descriptions) == 0:
        msg = f"No PersonaDescription found at {path_to_persona_elements!s}."
        raise ValueError(msg)


def _fail_if_active_tt_qnames_overlap(
    active_elements: list[TimeDependentPersonaElement], path_to_persona_elements: Path
) -> None:
    all_qnames: set[str] = set()
    overlapping_qnames: set[str] = set()
    for el in active_elements:
        if isinstance(el, PersonaDescription):
            # Should be unique, see _fail_if_not_exactly_one_description_is_active
            continue
        if el.tt_qname in all_qnames:
            overlapping_qnames.add(el.tt_qname)
        else:
            all_qnames.add(el.tt_qname)
    if overlapping_qnames:
        msg = (
            f"Active qnames overlap at {path_to_persona_elements!s}. "
            f"Overlapping qnames: {overlapping_qnames}"
        )
        raise ValueError(msg)


def _fail_if_bruttolohn_m_linspace_grid_is_invalid(
    linspace_grid: LinspaceGrid,
    p_id_array: np.ndarray,
) -> None:
    """Fail if the bruttolohn_m_linspace_spec is invalid."""
    # Because the LinspaceGrid is dynamically created, we cannot check for the
    # correct type directly.
    try:
        pids_in_linspace_grid = [
            f.name for f in fields(linspace_grid) if f.name != "n_points"
        ]
    except Exception as err:
        msg = (
            "The LinspaceGrid has not been instantiated correctly. "
            "Always instantiate via 'NameOfThePersona.LinspaceGrid'."
        )
        raise TypeError(msg) from err
    if not pids_in_linspace_grid or "n_points" not in [
        f.name for f in fields(linspace_grid)
    ]:
        msg = (
            "The LinspaceGrid has not been instantiated correctly. "
            "Always instantiate via 'NameOfThePersona.LinspaceGrid'."
        )
        raise TypeError(msg)
    if len(p_id_array) != len(pids_in_linspace_grid):
        msg = (
            f"The number of p_ids in the linspace grid must match the number of p_ids "
            "in the persona. The number of p_ids in the linspace grid is "
            f"{len(pids_in_linspace_grid)}, but the number of p_ids in the persona is "
            f"{len(p_id_array)}."
            "You likely used the wrong LinspaceGrid. Always instantiate via "
            "the LinspaceGrid method of this class."
        )
        raise ValueError(msg)
    for p_id in pids_in_linspace_grid:
        param_value = linspace_grid.__getattribute__(p_id)
        if isinstance(param_value, LinspaceRange):
            if param_value.bottom > param_value.top:
                msg = (
                    "The lower bound of the linspace must be less than the upper bound."
                )
                raise ValueError(msg)
        elif not isinstance(param_value, (int, float)):
            msg = (
                f"Parameter {p_id} must be either a LinspaceRange object or a numeric "
                "value."
            )
            raise TypeError(msg)
    if linspace_grid.n_points <= 0:
        msg = "The number of points in the linspace must be greater than 0."
        raise ValueError(msg)


def _fail_if_qname_input_data_differs_in_length_from_p_id_array(
    qname_input_data: dict[str, np.ndarray],
) -> None:
    p_id_array = qname_input_data["p_id"]
    for qname, array in qname_input_data.items():
        if len(array) != len(p_id_array):
            msg = (
                f"The input data for {qname} has a different length than the p_id "
                f"array. The length of {qname} is {len(array)}, but the length of "
                f"p_id is {len(p_id_array)}."
            )
            raise ValueError(msg)
