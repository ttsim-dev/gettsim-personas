from __future__ import annotations

import datetime
import inspect
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, ParamSpec, TypeVar

import dags
import dags.tree as dt

from gettsim_personas.utils import convert_and_validate_dates, load_module, to_datetime

if TYPE_CHECKING:
    from collections.abc import Callable
    from types import ModuleType
    from typing import Any

    import numpy as np

    from gettsim_personas.typing import DashedISOString, NestedData, NestedStrings


DEFAULT_START_DATE = datetime.date(1900, 1, 1)
DEFAULT_END_DATE = datetime.date(2100, 12, 31)

FunArgTypes = ParamSpec("FunArgTypes")
ReturnType = TypeVar("ReturnType")


@dataclass(frozen=True)
class PersonaForDate:
    description: str
    input_data_tree: NestedData
    tt_targets_tree: NestedStrings


@dataclass
class Persona:
    """A persona containing inputs and targets to use with GETTSIM."""

    path_to_persona_elements: Path
    start_date: datetime.date = DEFAULT_START_DATE
    end_date: datetime.date = DEFAULT_END_DATE
    error_if_not_implemented: str | None = None

    def __call__(
        self,
        *,
        policy_date: DashedISOString | datetime.date,
        evaluation_date: datetime.date | None = None,
    ) -> PersonaForDate:
        policy_date = to_datetime(policy_date)
        if evaluation_date is None:
            evaluation_date = policy_date
        else:
            evaluation_date = to_datetime(evaluation_date)

        self._fail_if_persona_not_implemented(policy_date)

        active_elements = self.active_elements(policy_date)
        qname_input_data = _get_qname_input_data(
            evaluation_date=evaluation_date,
            persona_input_elements=self.active_persona_input_elements(active_elements),
            path_to_persona_elements=self.path_to_persona_elements,
        )
        return PersonaForDate(
            description=self.active_description(active_elements),
            input_data_tree=dt.unflatten_from_qnames(qname_input_data),
            tt_targets_tree=dt.unflatten_from_qnames(
                self.active_tt_targets(active_elements)
            ),
        )

    def orig_elements(self) -> list[TimeDependentPersonaElement]:
        module = load_module(
            path=self.path_to_persona_elements,
            root=Path(__file__).parent.parent.parent,
        )
        return load_persona_elements_from_module(module)

    def active_elements(
        self, policy_date: datetime.date
    ) -> list[TimeDependentPersonaElement]:
        active_elements = [
            el for el in self.orig_elements() if el.is_active(policy_date)
        ]
        _fail_if_active_tt_qnames_overlap(
            active_elements=active_elements,
            path_to_persona_elements=self.path_to_persona_elements,
        )
        _fail_if_not_exactly_one_description_is_active(
            active_elements=active_elements,
            path_to_persona_elements=self.path_to_persona_elements,
        )
        return active_elements

    def active_persona_input_elements(
        self, active_elements: list[TimeDependentPersonaElement]
    ) -> list[PersonaInputElement]:
        return [s for s in active_elements if isinstance(s, PersonaInputElement)]

    def active_tt_targets(
        self, active_elements: list[TimeDependentPersonaElement]
    ) -> list[PersonaTargetElement]:
        return {
            s.tt_qname: None
            for s in active_elements
            if isinstance(s, PersonaTargetElement)
        }

    def active_description(
        self, active_elements: list[TimeDependentPersonaElement]
    ) -> PersonaDescription:
        return next(s for s in active_elements if isinstance(s, PersonaDescription))

    def _fail_if_persona_not_implemented(
        self,
        policy_date: datetime.date,
    ) -> None:
        if not (self.start_date <= policy_date <= self.end_date):
            raise NotImplementedError(self.error_if_not_implemented)


@dataclass(frozen=True)
class TimeDependentPersonaElement:
    """An element of some Persona that depends on a policy date."""

    start_date: datetime.date
    end_date: datetime.date

    def is_active(self, policy_date: datetime.date) -> bool:
        """Check if the function is active at a given date."""
        return self.start_date <= policy_date <= self.end_date


@dataclass(frozen=True)
class PersonaInputElement(TimeDependentPersonaElement):
    """An object that returns input data for one TT qname."""

    orig_name: str
    tt_qname: str
    function: Callable[FunArgTypes, ReturnType]

    def __call__(
        self, *args: FunArgTypes.args, **kwargs: FunArgTypes.kwargs
    ) -> ReturnType:
        return self.function(*args, **kwargs)


def persona_input_element(
    *,
    tt_qname: str | None = None,
    start_date: DashedISOString | datetime.date = DEFAULT_START_DATE,
    end_date: DashedISOString | datetime.date = DEFAULT_END_DATE,
) -> Callable[[Callable[..., Any]], PersonaInputElement]:
    """Decorator to create an instance of PersonaInputElement."""
    start_date, end_date = convert_and_validate_dates(
        start_date=start_date,
        end_date=end_date,
    )

    def inner(func: Callable[..., Any]) -> PersonaInputElement:
        return PersonaInputElement(
            orig_name=func.__name__,
            tt_qname=tt_qname if tt_qname else func.__name__,
            function=func,
            start_date=start_date,
            end_date=end_date,
        )

    return inner


@dataclass(frozen=True)
class PersonaTargetElement(TimeDependentPersonaElement):
    """An object that stores one TT qname to be used as a TT target."""

    orig_name: str
    tt_qname: str


def persona_target_element(
    *,
    start_date: DashedISOString | datetime.date = DEFAULT_START_DATE,
    end_date: DashedISOString | datetime.date = DEFAULT_END_DATE,
) -> Callable[[Callable[..., Any]], PersonaTargetElement]:
    start_date, end_date = convert_and_validate_dates(
        start_date=start_date,
        end_date=end_date,
    )

    def inner(func: Callable[..., Any]) -> PersonaTargetElement:
        return PersonaTargetElement(
            orig_name=func.__name__,
            tt_qname=func.__name__,
            start_date=start_date,
            end_date=end_date,
        )

    return inner


@dataclass(frozen=True)
class PersonaDescription(TimeDependentPersonaElement):
    """An object that stores a description of a persona."""

    orig_name: str
    description: str


def persona_description(
    *,
    description: str,
    start_date: DashedISOString | datetime.date = DEFAULT_START_DATE,
    end_date: DashedISOString | datetime.date = DEFAULT_END_DATE,
) -> PersonaDescription:
    start_date, end_date = convert_and_validate_dates(
        start_date=start_date,
        end_date=end_date,
    )

    def inner(func: Callable[..., Any]) -> PersonaDescription:
        return PersonaDescription(
            orig_name=func.__name__,
            description=description,
            start_date=start_date,
            end_date=end_date,
        )

    return inner


def _get_qname_input_data(
    evaluation_date: datetime.date,
    persona_input_elements: list[PersonaInputElement],
) -> dict[str, np.ndarray]:
    f = dags.concatenate_functions(
        functions=[el.function for el in persona_input_elements],
        targets=[el.tt_qname for el in persona_input_elements],
        return_type="dict",
    )
    params = inspect.signature(f).parameters

    if params == "evaluation_date":
        return f(evaluation_date=evaluation_date)
    if params:
        # We only support "evaluation_date" or no parameter at all for now
        msg = (
            f"The following parameters are needed to create the input data for this "
            f"persona: {params}. "
        )
        raise ValueError(msg)
    return f()


def load_persona_elements_from_module(
    module: ModuleType,
) -> list[TimeDependentPersonaElement]:
    persona_elements_in_this_module: list[TimeDependentPersonaElement] = []
    for _, obj in inspect.getmembers(module):
        if isinstance(obj, TimeDependentPersonaElement):
            persona_elements_in_this_module.append(obj)
    return persona_elements_in_this_module


def _fail_if_not_exactly_one_description_is_active(
    active_elements: list[TimeDependentPersonaElement], path_to_persona_elements: Path
) -> None:
    descriptions = [s for s in active_elements if isinstance(s, PersonaDescription)]
    if len(descriptions) > 1:
        msg = f"More than one PersonaDescription is active at {path_to_persona_elements!s}."
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
