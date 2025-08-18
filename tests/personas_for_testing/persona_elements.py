from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from _gettsim_personas.persona_elements import (
    persona_description,
    persona_input_element,
    persona_pid_element,
    persona_target_element,
)

if TYPE_CHECKING:
    import datetime


@persona_description(
    description="Test description valid until 2009.",
    end_date="2009-12-31",
)
def description_until_2009() -> None:
    pass


@persona_description(
    description="Test description valid since 2010.",
    start_date="2010-01-01",
)
def description_since_2010() -> None:
    pass


@persona_pid_element()
def p_id() -> np.ndarray:
    return np.array([0, 1, 2])


@persona_input_element()
def some_time_dependent_persona_input_element() -> np.ndarray:
    return np.array([1, 2, 3])


@persona_input_element(end_date="2009-12-31")
def time_dependent_persona_input_element_until_2009() -> np.ndarray:
    return np.array([1, 2, 3])


@persona_input_element(start_date="2010-01-01")
def time_dependent_persona_input_element_since_2010() -> np.ndarray:
    return np.array([1, 2, 3])


@persona_input_element(tt_qname="input_qname_via_decorator")
def some_irrelevant_name() -> np.ndarray:
    return np.array([1, 2, 3])


@persona_input_element()
def some_qname_depending_on_another_qname(
    some_time_dependent_persona_input_element: np.ndarray,
) -> np.ndarray:
    return 2 * some_time_dependent_persona_input_element


@persona_input_element()
def true_if_evaluation_year_at_least_2015(
    evaluation_date: datetime.date,
) -> np.ndarray:
    return evaluation_date.year >= np.array([2015, 2015, 2015])


@persona_input_element()
def qname_depending_on_evaluation_date_and_another_qname(
    evaluation_date: datetime.date,
    some_qname_depending_on_another_qname: np.ndarray,
) -> np.ndarray:
    return evaluation_date.year >= some_qname_depending_on_another_qname


@persona_target_element()
def some_target_qname():
    pass


@persona_target_element(end_date="2009-12-31")
def some_target_qname_until_2009():
    pass


@persona_target_element(start_date="2010-01-01")
def some_target_qname_since_2010():
    pass


@persona_input_element()
def einnahmen__bruttolohn_m() -> np.ndarray:
    return np.array([1, 2, 3])
