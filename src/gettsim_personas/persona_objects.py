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

    from gettsim_personas.typing import NestedData, NestedStrings


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

    specs_file: Path
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

        active_specs = self.active_specs(policy_date)
        qname_input_data = _get_qname_input_data(
            persona_name=self.name,
            evaluation_date=evaluation_date,
            input_columns=self.active_input_columns(active_specs),
        )
        return PersonaForDate(
            description=self.active_description(active_specs),
            input_data_tree=dt.unflatten_from_qnames(qname_input_data),
            tt_targets_tree=dt.unflatten_from_qnames(
                self.active_tt_targets(active_specs)
            ),
        )

    def orig_specs(self) -> list[TimeDependentPersonaSpec]:
        return load_persona_specs_from_module(self.specs_file)

    def active_specs(
        self, policy_date: datetime.date
    ) -> list[TimeDependentPersonaSpec]:
        active_specs = [
            spec for spec in self.orig_specs() if spec.is_active(policy_date)
        ]
        _fail_if_active_qnames_overlap(
            active_specs=active_specs,
            persona_name=self.name,
        )
        _fail_if_more_than_one_description_is_active(
            active_specs=active_specs,
            persona_name=self.name,
        )
        return active_specs

    def active_input_columns(
        self, active_specs: list[TimeDependentPersonaSpec]
    ) -> list[InputColumn]:
        return [s for s in active_specs if isinstance(s, InputColumn)]

    def active_tt_targets(
        self, active_specs: list[TimeDependentPersonaSpec]
    ) -> list[TTTarget]:
        return {s.qname: None for s in active_specs if isinstance(s, TTTarget)}

    def active_description(
        self, active_specs: list[TimeDependentPersonaSpec]
    ) -> PersonaDescription:
        return next(s for s in active_specs if isinstance(s, PersonaDescription))

    def _fail_if_persona_not_implemented(
        self,
        policy_date: datetime.date,
    ) -> None:
        if not (self.start_date <= policy_date <= self.end_date):
            raise NotImplementedError(self.error_if_not_implemented)


@dataclass(frozen=True)
class TimeDependentPersonaSpec:
    """A persona specification object that depends on a policy date."""

    start_date: datetime.date
    end_date: datetime.date

    def is_active(self, policy_date: datetime.date) -> bool:
        """Check if the function is active at a given date."""
        return self.start_date <= policy_date <= self.end_date


@dataclass(frozen=True)
class InputColumn(TimeDependentPersonaSpec):
    """An object that returns input data for one qname."""

    qname: str
    function: Callable[FunArgTypes, ReturnType]

    def __call__(
        self, *args: FunArgTypes.args, **kwargs: FunArgTypes.kwargs
    ) -> ReturnType:
        return self.func(*args, **kwargs)


def input_column(
    *,
    qname: str | None = None,
    start_date: str | datetime.date = DEFAULT_START_DATE,
    end_date: str | datetime.date = DEFAULT_END_DATE,
) -> Callable[[Callable[..., Any]], InputColumn]:
    """Decorator to create an instance of InputColumn."""
    start_date, end_date = convert_and_validate_dates(
        start_date=start_date,
        end_date=end_date,
    )

    def inner(func: Callable[..., Any]) -> InputColumn:
        return InputColumn(
            qname=qname if qname else func.__name__,
            start_date=start_date,
            end_date=end_date,
        )

    return inner


@dataclass(frozen=True)
class TTTarget(TimeDependentPersonaSpec):
    """An object that stores one qname to be used as a TT target."""

    qname: str


def target_column(
    *,
    qname: str | None = None,
    start_date: str | datetime.date = DEFAULT_START_DATE,
    end_date: str | datetime.date = DEFAULT_END_DATE,
) -> Callable[[Callable[..., Any]], TTTarget]:
    start_date, end_date = convert_and_validate_dates(
        start_date=start_date,
        end_date=end_date,
    )

    def inner(func: Callable[..., Any]) -> TTTarget:
        return TTTarget(
            qname=qname if qname else func.__name__,
            start_date=start_date,
            end_date=end_date,
        )

    return inner


@dataclass(frozen=True)
class PersonaDescription(TimeDependentPersonaSpec):
    """An object that stores a description of a persona."""

    description: str


def _get_qname_input_data(
    persona_name: str,
    evaluation_date: datetime.date,
    input_columns: list[InputColumn],
) -> dict[str, np.ndarray]:
    f = dags.concatenate_functions(
        functions=[spec.function for spec in input_columns],
        targets=[spec.qname for spec in input_columns],
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


def load_persona_specs_from_module(
    module: ModuleType,
) -> list[TimeDependentPersonaSpec]:
    persona_specs_in_this_module: list[TimeDependentPersonaSpec] = []
    for _, obj in inspect.getmembers(module):
        if isinstance(obj, TimeDependentPersonaSpec):
            persona_specs_in_this_module.append(obj)
    return persona_specs_in_this_module


def _fail_if_more_than_one_description_is_active(
    active_specs: list[TimeDependentPersonaSpec], persona_name: str
) -> None:
    descriptions = [s for s in active_specs if isinstance(s, PersonaDescription)]
    if len(descriptions) > 1:
        msg = f"More than one PersonaDescription is active for {persona_name}"
        raise ValueError(msg)


def _fail_if_active_qnames_overlap(
    active_specs: list[TimeDependentPersonaSpec], persona_name: str
) -> None:
    all_qnames: set[str] = set()
    overlapping_qnames: set[str] = set()
    for spec in active_specs:
        if spec.qname in all_qnames:
            overlapping_qnames.add(spec.qname)
        else:
            all_qnames.add(spec.qname)
    if overlapping_qnames:
        msg = (
            f"Active qnames overlap for {persona_name}. "
            f"Overlapping qnames: {overlapping_qnames}"
        )
        raise ValueError(msg)
