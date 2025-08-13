from __future__ import annotations

import datetime
import inspect
from dataclasses import dataclass
from typing import TYPE_CHECKING, ParamSpec, TypeVar

import dags
import dags.tree as dt

from gettsim_personas.utils import convert_and_validate_dates

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path
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


@dataclass(frozen=True)
class Persona:
    """A persona containing inputs and targets to use with GETTSIM."""

    path_to_persona_elements: Path
    name: str = __name__
    start_date: datetime.date = DEFAULT_START_DATE
    end_date: datetime.date = DEFAULT_END_DATE
    error_if_not_implemented: str | None = None

    def __call__(
        self,
        *,
        policy_date: datetime.date,
        evaluation_date: datetime.date | None = None,
    ) -> PersonaForDate:
        self._fail_if_persona_not_implemented(policy_date)

        if evaluation_date is None:
            evaluation_date = policy_date

        active_elements = self.active_elements(policy_date)
        qname_input_data = _get_qname_input_data(
            persona_name=self.name,
            evaluation_date=evaluation_date,
            input_columns=self.active_input_columns(active_elements),
        )
        return PersonaForDate(
            description=self.active_description(active_elements),
            input_data_tree=dt.unflatten_from_qnames(qname_input_data),
            tt_targets_tree=dt.unflatten_from_qnames(
                self.active_tt_targets(active_elements)
            ),
        )

    def orig_elements(self) -> list[TimeDependentPersonaElement]:
        return load_persona_elements_from_module(self.path_to_persona_elements)

    def active_elements(
        self, policy_date: datetime.date
    ) -> list[TimeDependentPersonaElement]:
        active_elements = [
            el for el in self.orig_elements() if el.is_active(policy_date)
        ]
        _fail_if_active_qnames_overlap(
            active_elements=active_elements,
            persona_name=self.name,
        )
        _fail_if_more_than_one_description_is_active(
            active_elements=active_elements,
            persona_name=self.name,
        )
        return active_elements

    def active_input_columns(
        self, active_elements: list[TimeDependentPersonaElement]
    ) -> list[InputColumn]:
        return [s for s in active_elements if isinstance(s, InputColumn)]

    def active_tt_targets(
        self, active_elements: list[TimeDependentPersonaElement]
    ) -> list[TTTarget]:
        return {s.qname: None for s in active_elements if isinstance(s, TTTarget)}

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
class InputColumn(TimeDependentPersonaElement):
    """An object that returns input data for one qname."""

    qname: str
    function: Callable[FunArgTypes, ReturnType]

    def __call__(
        self, *args: FunArgTypes.args, **kwargs: FunArgTypes.kwargs
    ) -> ReturnType:
        return self.function(*args, **kwargs)


def input_column(
    *,
    qname: str | None = None,
    start_date: DashedISOString | datetime.date = DEFAULT_START_DATE,
    end_date: DashedISOString | datetime.date = DEFAULT_END_DATE,
) -> Callable[[Callable[..., Any]], InputColumn]:
    """Decorator to create an instance of InputColumn."""
    start_date, end_date = convert_and_validate_dates(
        start_date=start_date,
        end_date=end_date,
    )

    def inner(func: Callable[..., Any]) -> InputColumn:
        return InputColumn(
            qname=qname if qname else func.__name__,
            function=func,
            start_date=start_date,
            end_date=end_date,
        )

    return inner


@dataclass(frozen=True)
class TTTarget(TimeDependentPersonaElement):
    """An object that stores one qname to be used as a TT target."""

    qname: str


def target_column(
    *,
    start_date: DashedISOString | datetime.date = DEFAULT_START_DATE,
    end_date: DashedISOString | datetime.date = DEFAULT_END_DATE,
) -> Callable[[Callable[..., Any]], TTTarget]:
    start_date, end_date = convert_and_validate_dates(
        start_date=start_date,
        end_date=end_date,
    )

    def inner(func: Callable[..., Any]) -> TTTarget:
        return TTTarget(
            qname=func.__name__,
            start_date=start_date,
            end_date=end_date,
        )

    return inner


@dataclass(frozen=True)
class PersonaDescription(TimeDependentPersonaElement):
    """An object that stores a description of a persona."""

    name: str
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
            name=func.__name__,
            start_date=start_date,
            end_date=end_date,
            description=description,
        )

    return inner


def _get_qname_input_data(
    persona_name: str,
    evaluation_date: datetime.date,
    input_columns: list[InputColumn],
) -> dict[str, np.ndarray]:
    f = dags.concatenate_functions(
        functions=[el.function for el in input_columns],
        targets=[el.qname for el in input_columns],
        return_type="dict",
    )
    params = inspect.signature(f).parameters

    if params == "evaluation_date":
        return f(evaluation_date=evaluation_date)
    if params:
        # We only support "evaluation_date" or no parameter at all for now
        msg = (
            f"The following parameters are needed to create the input data for persona "
            f"'{persona_name}': {params}. "
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


def _fail_if_more_than_one_description_is_active(
    active_elements: list[TimeDependentPersonaElement], persona_name: str
) -> None:
    descriptions = [s for s in active_elements if isinstance(s, PersonaDescription)]
    if len(descriptions) > 1:
        msg = f"More than one PersonaDescription is active for {persona_name}"
        raise ValueError(msg)


def _fail_if_active_qnames_overlap(
    active_elements: list[TimeDependentPersonaElement], persona_name: str
) -> None:
    all_qnames: set[str] = set()
    overlapping_qnames: set[str] = set()
    for el in active_elements:
        if el.qname in all_qnames:
            overlapping_qnames.add(el.qname)
        else:
            all_qnames.add(el.qname)
    if overlapping_qnames:
        msg = (
            f"Active qnames overlap for {persona_name}. "
            f"Overlapping qnames: {overlapping_qnames}"
        )
        raise ValueError(msg)
