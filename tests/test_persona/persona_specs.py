from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from gettsim_personas.persona_objects import (
    PersonaDescription,
    input_column,
    target_column,
)

if TYPE_CHECKING:
    import datetime


description_until_2009 = PersonaDescription(
    end_date="2009-12-31",
    description="Test description valid until 2009.",
)


description_since_2010 = PersonaDescription(
    start_date="2010-01-01",
    description="Test description valid since 2010.",
)


@input_column()
def some_input_column() -> np.ndarray:
    return np.array([1, 2, 3])


@input_column(end_date="2009-12-31")
def input_column_until_2009() -> np.ndarray:
    return np.array([1, 2, 3])


@input_column(start_date="2010-01-01")
def input_column_since_2010() -> np.ndarray:
    return np.array([1, 2, 3])


@input_column(qname="input_qname_via_decorator")
def some_irrelevant_name() -> np.ndarray:
    return np.array([1, 2, 3])


@input_column()
def some_qname_depending_on_another_qname(
    some_input_column: np.ndarray,
) -> np.ndarray:
    return 2 * some_input_column


@input_column()
def true_if_evaluation_year_at_least_2015(
    evaluation_date: datetime.date,
) -> np.ndarray:
    return evaluation_date.year >= np.array([2015, 2015, 2015])


@input_column()
def qname_depending_on_evaluation_date_and_another_qname(
    evaluation_date: datetime.date,
    some_qname_depending_on_another_qname: np.ndarray,
) -> np.ndarray:
    return evaluation_date.year >= some_qname_depending_on_another_qname


@target_column()
def some_target_qname():
    pass


@target_column(end_date="2009-12-31")
def some_target_qname_until_2009():
    pass


@target_column(start_date="2010-01-01")
def some_target_qname_since_2010():
    pass
