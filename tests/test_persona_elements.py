import datetime

import numpy as np
import pytest
from numpy.testing import assert_array_equal

from gettsim_personas.persona_objects import (
    TimeDependentPersonaElement,
    persona_description,
    persona_input_element,
    persona_target_element,
)
from tests.personas_for_testing.persona_elements import (
    description_since_2010,
    description_until_2009,
    persona_input_element_since_2010,
    persona_input_element_until_2009,
    qname_depending_on_evaluation_date_and_another_qname,
    some_irrelevant_name,
    some_persona_input_element,
    some_qname_depending_on_another_qname,
    some_target_qname,
    some_target_qname_since_2010,
    some_target_qname_until_2009,
    true_if_evaluation_year_at_least_2015,
)

some_time_dependent_persona_element = TimeDependentPersonaElement(
    start_date=datetime.date(2000, 1, 1),
    end_date=datetime.date(2010, 1, 1),
)


def test_time_dependent_persona_elements():
    assert not some_time_dependent_persona_element.is_active(datetime.date(1999, 1, 1))
    assert some_time_dependent_persona_element.is_active(datetime.date(2005, 1, 1))
    assert not some_time_dependent_persona_element.is_active(datetime.date(2011, 1, 1))


def test_time_dependent_persona_elements_raises_error_for_invalid_dates():
    with pytest.raises(ValueError, match="must be before the end date"):

        @persona_input_element(start_date="2005-01-01", end_date="2004-01-01")
        def some_input():
            return 1

    with pytest.raises(ValueError, match="must be before the end date"):

        @persona_target_element(start_date="2005-01-01", end_date="2004-01-01")
        def some_target():
            pass

    with pytest.raises(ValueError, match="must be before the end date"):

        @persona_description(
            start_date="2005-01-01", end_date="2004-01-01", description=""
        )
        def some_description():
            pass


def test_persona_elements_have_correct_qname():
    assert some_persona_input_element.tt_qname == "some_persona_input_element"
    assert (
        persona_input_element_until_2009.tt_qname == "persona_input_element_until_2009"
    )
    assert (
        persona_input_element_since_2010.tt_qname == "persona_input_element_since_2010"
    )
    assert some_irrelevant_name.tt_qname == "input_qname_via_decorator"
    assert (
        some_qname_depending_on_another_qname.tt_qname
        == "some_qname_depending_on_another_qname"
    )
    assert some_target_qname.tt_qname == "some_target_qname"


def test_persona_elements_are_active_at_correct_dates():
    jan_01_2009 = datetime.date(2009, 1, 1)
    jan_01_2010 = datetime.date(2010, 1, 1)

    assert persona_input_element_until_2009.is_active(jan_01_2009)
    assert not persona_input_element_until_2009.is_active(jan_01_2010)

    assert not persona_input_element_since_2010.is_active(jan_01_2009)
    assert persona_input_element_since_2010.is_active(jan_01_2010)

    assert description_until_2009.is_active(jan_01_2009)
    assert not description_until_2009.is_active(jan_01_2010)

    assert not description_since_2010.is_active(jan_01_2009)
    assert description_since_2010.is_active(jan_01_2010)

    assert some_target_qname_until_2009.is_active(jan_01_2009)
    assert not some_target_qname_until_2009.is_active(jan_01_2010)

    assert not some_target_qname_since_2010.is_active(jan_01_2009)
    assert some_target_qname_since_2010.is_active(jan_01_2010)


def test_can_call_persona_input_element_elements():
    assert_array_equal(
        some_persona_input_element(),
        np.array([1, 2, 3]),
    )
    assert_array_equal(
        true_if_evaluation_year_at_least_2015(datetime.date(2016, 1, 1)),
        np.array([True, True, True]),
    )
    assert_array_equal(
        some_qname_depending_on_another_qname(np.array([1, 2, 3])), np.array([2, 4, 6])
    )
    assert_array_equal(
        qname_depending_on_evaluation_date_and_another_qname(
            evaluation_date=datetime.date(2010, 1, 1),
            some_qname_depending_on_another_qname=np.array([1, 2, 3]),
        ),
        np.array([True, True, True]),
    )
