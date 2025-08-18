import datetime
from dataclasses import dataclass

import numpy as np
import pytest
from numpy.testing import assert_array_equal

from gettsim_personas.persona_elements import (
    persona_description,
    persona_input_element,
)
from gettsim_personas.persona_objects import (
    _fail_if_active_tt_qnames_overlap,
    _fail_if_bruttolohn_m_linspace_grid_is_invalid,
    _fail_if_not_exactly_one_description_is_active,
)
from tests.personas_for_testing import (
    SamplePersona,
    SamplePersonaWithInvalidLengthOfInputData,
    SamplePersonaWithOverlappingElements,
    SamplePersonaWithStartAndEndDate,
)


@persona_input_element()
def input_element_always_active():
    return 1


@persona_input_element(start_date="2010-01-01")
def time_dependent_persona_input_element_active_since_2010():
    return 1


@persona_input_element(tt_qname="input_element_always_active")
def another_input_element_always_active():
    return 1


@persona_description(description="")
def active_description():
    pass


@persona_description(description="")
def another_active_description():
    pass


def test_sample_personas_have_expected_orig_persona_elements():
    expected_orig_names = {
        "description_until_2009",
        "description_since_2010",
        "some_time_dependent_persona_input_element",
        "time_dependent_persona_input_element_until_2009",
        "time_dependent_persona_input_element_since_2010",
        "some_irrelevant_name",
        "some_qname_depending_on_another_qname",
        "true_if_evaluation_year_at_least_2015",
        "qname_depending_on_evaluation_date_and_another_qname",
        "some_target_qname",
        "some_target_qname_until_2009",
        "some_target_qname_since_2010",
        "p_id",
        "einnahmen__bruttolohn_m",
    }
    orig_names = {el.orig_name for el in SamplePersona.orig_elements()}
    assert expected_orig_names == orig_names

    expected_tt_qnames = {
        "some_time_dependent_persona_input_element",
        "time_dependent_persona_input_element_until_2009",
        "time_dependent_persona_input_element_since_2010",
        "input_qname_via_decorator",
        "some_qname_depending_on_another_qname",
        "true_if_evaluation_year_at_least_2015",
        "qname_depending_on_evaluation_date_and_another_qname",
        "some_target_qname",
        "some_target_qname_until_2009",
        "some_target_qname_since_2010",
        "p_id",
        "einnahmen__bruttolohn_m",
    }
    tt_qnames = {
        el.tt_qname for el in SamplePersona.orig_elements() if hasattr(el, "tt_qname")
    }
    assert expected_tt_qnames == tt_qnames


@pytest.mark.parametrize(
    (
        "policy_date",
        "expected_tt_qnames",
    ),
    [
        (
            datetime.date(2009, 1, 1),
            {
                "description_until_2009",
                "some_time_dependent_persona_input_element",
                "time_dependent_persona_input_element_until_2009",
                "some_irrelevant_name",
                "some_qname_depending_on_another_qname",
                "true_if_evaluation_year_at_least_2015",
                "qname_depending_on_evaluation_date_and_another_qname",
                "some_target_qname",
                "some_target_qname_until_2009",
                "p_id",
                "einnahmen__bruttolohn_m",
            },
        ),
        (
            datetime.date(2010, 1, 1),
            {
                "description_since_2010",
                "some_time_dependent_persona_input_element",
                "time_dependent_persona_input_element_since_2010",
                "some_irrelevant_name",
                "some_qname_depending_on_another_qname",
                "true_if_evaluation_year_at_least_2015",
                "qname_depending_on_evaluation_date_and_another_qname",
                "some_target_qname",
                "some_target_qname_since_2010",
                "p_id",
                "einnahmen__bruttolohn_m",
            },
        ),
    ],
)
def test_sample_persona_has_expected_active_persona_elements(
    policy_date, expected_tt_qnames
):
    active_tt_qnames = {
        el.orig_name for el in SamplePersona.active_elements(policy_date)
    }
    assert active_tt_qnames == expected_tt_qnames


def test_fail_if_active_tt_qnames_overlap():
    with pytest.raises(
        ValueError,
        match=r"Overlapping qnames: \{'input_element_always_active'\}",
    ):
        _fail_if_active_tt_qnames_overlap(
            active_elements=[
                input_element_always_active,
                another_input_element_always_active,
                time_dependent_persona_input_element_active_since_2010,
            ],
            path_to_persona_elements="",
        )


def test_fail_if_active_tt_qnames_overlap_via_persona_object():
    with pytest.raises(ValueError, match=r"Overlapping qnames: \{'input_1'\}"):
        SamplePersonaWithOverlappingElements(policy_date="2015-01-01")


def test_do_not_fail_if_active_qnames_do_not_overlap():
    _fail_if_active_tt_qnames_overlap(
        active_elements=[
            input_element_always_active,
            time_dependent_persona_input_element_active_since_2010,
        ],
        path_to_persona_elements="",
    )


def test_fail_if_multiple_descriptions_are_active():
    with pytest.raises(ValueError, match="More than one PersonaDescription is active"):
        _fail_if_not_exactly_one_description_is_active(
            active_elements=[
                active_description,
                another_active_description,
                input_element_always_active,
            ],
            path_to_persona_elements="",
        )


def test_do_not_fail_if_only_one_description_is_active():
    _fail_if_not_exactly_one_description_is_active(
        active_elements=[
            active_description,
            input_element_always_active,
        ],
        path_to_persona_elements="",
    )


def test_sample_persona_raises_error_if_called_with_invalid_date():
    with pytest.raises(
        NotImplementedError, match="This Persona is not implemented before 2015."
    ):
        SamplePersonaWithStartAndEndDate(policy_date="2014-01-01")


def test_call_persona_with_evaluation_date():
    persona2015 = SamplePersona(
        policy_date="2015-01-01",
        evaluation_date="2015-01-01",
    )
    assert_array_equal(
        persona2015.input_data_tree["true_if_evaluation_year_at_least_2015"],
        np.array([True, True, True]),
    )

    persona2014 = SamplePersona(
        policy_date="2015-01-01",
        evaluation_date="2014-01-01",
    )
    assert_array_equal(
        persona2014.input_data_tree["true_if_evaluation_year_at_least_2015"],
        np.array([False, False, False]),
    )


def test_bruttolohn_m_linspace_grid_invalid_wrong_type():
    with pytest.raises(
        TypeError,
        match="The LinspaceGridClass has not been instantiated correctly.",
    ):
        _fail_if_bruttolohn_m_linspace_grid_is_invalid(
            linspace_grid={"a": 1},
            p_id_array=np.array([1, 2, 3]),
        )


def test_bruttolohn_m_linspace_grid_invalid_wrong_number_of_p_ids():
    @dataclass(frozen=True)
    class InvalidLinspaceGrid:
        p0: int
        p1: int
        n_points: int

    with pytest.raises(
        ValueError,
        match="The number of p_ids in the linspace grid must match the number of p_ids",
    ):
        _fail_if_bruttolohn_m_linspace_grid_is_invalid(
            linspace_grid=InvalidLinspaceGrid(p0=1, p1=2, n_points=10),
            p_id_array=np.array([0, 1, 2, 3]),
        )


def test_bruttolohn_m_linspace_grid_invalid_bottom_larger_than_top():
    linspace_grid = SamplePersona.LinspaceGridClass(
        p0=SamplePersona.LinspaceRange(bottom=0, top=1),
        p1=SamplePersona.LinspaceRange(bottom=0, top=1),
        p2=SamplePersona.LinspaceRange(bottom=1, top=0),
        n_points=10,
    )
    with pytest.raises(
        ValueError,
        match="The lower bound of the linspace must be less than the upper bound.",
    ):
        _fail_if_bruttolohn_m_linspace_grid_is_invalid(
            linspace_grid=linspace_grid,
            p_id_array=np.array([0, 1, 2]),
        )


def test_bruttolohn_m_linspace_grid_invalid_n_points_zero():
    def call_invalid():
        linspace_grid = SamplePersona.LinspaceGridClass(
            p0=SamplePersona.LinspaceRange(bottom=0, top=1),
            p1=SamplePersona.LinspaceRange(bottom=0, top=1),
            p2=SamplePersona.LinspaceRange(bottom=0, top=1),
            n_points=0,
        )
        _fail_if_bruttolohn_m_linspace_grid_is_invalid(
            linspace_grid=linspace_grid,
            p_id_array=np.array([0, 1, 2]),
        )

    with pytest.raises(
        ValueError,
        match="The number of points in the linspace must be greater than 0.",
    ):
        call_invalid()


def test_bruttolohn_m_is_default_value_if_no_linspace_grid_is_provided():
    persona = SamplePersona(
        policy_date="2015-01-01",
        evaluation_date="2015-01-01",
    )
    assert_array_equal(
        persona.input_data_tree["einnahmen"]["bruttolohn_m"],
        np.array([1, 2, 3]),
    )


def test_bruttolohn_m_is_upserted_if_linspace_grid_is_provided():
    persona = SamplePersona(
        policy_date="2015-01-01",
        evaluation_date="2015-01-01",
        bruttolohn_m_linspace_grid=SamplePersona.LinspaceGridClass(
            p0=SamplePersona.LinspaceRange(bottom=0, top=1),
            p1=SamplePersona.LinspaceRange(bottom=0, top=1),
            p2=SamplePersona.LinspaceRange(bottom=0, top=0),
            n_points=2,
        ),
    )
    assert_array_equal(
        persona.input_data_tree["einnahmen"]["bruttolohn_m"],
        np.array([0, 0, 0, 1, 1, 0]),
    )


def test_persona_call_fails_if_input_data_differs_in_length_from_p_id_array():
    with pytest.raises(
        ValueError,
        match="The input data for input_1 has a different length than the p_id array.",
    ):
        SamplePersonaWithInvalidLengthOfInputData(
            policy_date="2015-01-01",
        )
