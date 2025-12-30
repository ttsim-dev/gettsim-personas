from __future__ import annotations

import datetime
import inspect
from dataclasses import dataclass
from typing import TYPE_CHECKING, ParamSpec, TypeVar

import numpy as np
from ttsim.tt.column_objects_param_function import _convert_and_validate_dates

if TYPE_CHECKING:
    from collections.abc import Callable
    from types import FunctionType
    from typing import Any

    from _gettsim_personas.typing import DashedISOString


DEFAULT_START_DATE = datetime.date(1900, 1, 1)
DEFAULT_END_DATE = datetime.date(2100, 12, 31)


FunArgTypes = ParamSpec("FunArgTypes")
ReturnType = TypeVar("ReturnType")


@dataclass(frozen=True)
class PersonaPIDElement:
    """An object that returns a p_id array for a persona."""

    function: FunctionType[..., Any]
    tt_qname: str = "p_id"
    orig_name: str = "p_id"

    def __post_init__(self):
        _fail_if_p_ids_not_consecutive_starting_at_zero(self.function())

    def __call__(
        self, *args: FunArgTypes.args, **kwargs: FunArgTypes.kwargs
    ) -> ReturnType:
        return self.function(*args, **kwargs)

    @property
    def __signature__(self):
        return inspect.signature(self.function)

    @property
    def persona_size(self) -> int:
        return len(self.function())


def persona_pid_element() -> Callable[[FunctionType[..., Any]], PersonaPIDElement]:
    def inner(func: FunctionType[..., Any]) -> PersonaPIDElement:
        return PersonaPIDElement(function=func)

    return inner


@dataclass(frozen=True)
class TimeDependentPersonaElement:
    """An element of some OrigPersonaOverTime that depends on a policy date."""

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
    function: FunctionType[FunArgTypes, ReturnType]

    def __call__(
        self, *args: FunArgTypes.args, **kwargs: FunArgTypes.kwargs
    ) -> ReturnType:
        return self.function(*args, **kwargs)

    @property
    def __signature__(self):
        return inspect.signature(self.function)


def persona_input_element(
    *,
    tt_qname: str | None = None,
    start_date: DashedISOString | datetime.date = DEFAULT_START_DATE,
    end_date: DashedISOString | datetime.date = DEFAULT_END_DATE,
) -> Callable[[Callable[..., Any]], PersonaInputElement]:
    """Decorator to create an instance of PersonaInputElement."""
    start_date, end_date = _convert_and_validate_dates(
        start_date=start_date,
        end_date=end_date,
    )

    def inner(func: FunctionType[..., Any]) -> PersonaInputElement:
        func_name = getattr(func, "__name__", "")
        return PersonaInputElement(
            orig_name=func_name,
            tt_qname=tt_qname if tt_qname else func_name,
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
) -> Callable[[FunctionType[..., Any]], PersonaTargetElement]:
    start_date, end_date = _convert_and_validate_dates(
        start_date=start_date,
        end_date=end_date,
    )

    def inner(func: FunctionType[..., Any]) -> PersonaTargetElement:
        func_name = getattr(func, "__name__", "")
        return PersonaTargetElement(
            orig_name=func_name,
            tt_qname=func_name,
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
) -> Callable[[FunctionType[..., Any]], PersonaDescription]:
    start_date, end_date = _convert_and_validate_dates(
        start_date=start_date,
        end_date=end_date,
    )

    def inner(func: FunctionType[..., Any]) -> PersonaDescription:
        func_name = getattr(func, "__name__", "")
        return PersonaDescription(
            orig_name=func_name,
            description=description,
            start_date=start_date,
            end_date=end_date,
        )

    return inner


def _fail_if_p_ids_not_consecutive_starting_at_zero(p_ids: np.ndarray) -> None:
    if not np.all(p_ids == np.arange(len(p_ids))):
        msg = f"p_ids must be consecutive starting at zero. Got: {p_ids}"
        raise ValueError(msg)
