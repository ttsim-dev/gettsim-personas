import datetime
import inspect
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pytest
from numpy.testing import assert_array_equal

from _gettsim_personas.persona_elements import (
    persona_description,
    persona_input_element,
    persona_pid_element,
    persona_target_element,
)
from _gettsim_personas.persona_objects import (
    LinspaceGridProtocol,
    OrigPersonaOverTime,
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
        "hh_id",
        "einnahmen__bruttolohn_m",
    }
    orig_names = {el.orig_name for el in SamplePersona.elements}
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
        "hh_id",
        "einnahmen__bruttolohn_m",
    }
    tt_qnames = {
        el.tt_qname for el in SamplePersona.elements if hasattr(el, "tt_qname")
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
                "hh_id",
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
                "hh_id",
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
            persona_name="some persona",
        )


def test_fail_if_active_tt_qnames_overlap_via_persona_object():
    with pytest.raises(ValueError, match=r"Overlapping qnames: \{'input_1'\}"):
        SamplePersonaWithOverlappingElements(policy_date_str="2015-01-01")


def test_do_not_fail_if_active_qnames_do_not_overlap():
    _fail_if_active_tt_qnames_overlap(
        active_elements=[
            input_element_always_active,
            time_dependent_persona_input_element_active_since_2010,
        ],
        persona_name="some persona",
    )


def test_fail_if_multiple_descriptions_are_active():
    with pytest.raises(ValueError, match="More than one PersonaDescription is active"):
        _fail_if_not_exactly_one_description_is_active(
            active_elements=[
                active_description,
                another_active_description,
                input_element_always_active,
            ],
            persona_name="some persona",
        )


def test_do_not_fail_if_only_one_description_is_active():
    _fail_if_not_exactly_one_description_is_active(
        active_elements=[
            active_description,
            input_element_always_active,
        ],
        persona_name="some persona",
    )


def test_sample_persona_raises_error_if_called_with_invalid_date():
    with pytest.raises(
        NotImplementedError, match=r"This Persona is not implemented before 2015."
    ):
        SamplePersonaWithStartAndEndDate(policy_date_str="2014-01-01")


def test_call_persona_with_evaluation_date():
    persona2015 = SamplePersona(
        policy_date_str="2015-01-01",
        evaluation_date_str="2015-01-01",
    )
    assert_array_equal(
        persona2015.input_data_tree["true_if_evaluation_year_at_least_2015"],
        np.array([True, True, True]),
    )

    persona2014 = SamplePersona(
        policy_date_str="2015-01-01",
        evaluation_date_str="2014-01-01",
    )
    assert_array_equal(
        persona2014.input_data_tree["true_if_evaluation_year_at_least_2015"],
        np.array([False, False, False]),
    )


def test_bruttolohn_m_linspace_grid_invalid_wrong_type():
    with pytest.raises(
        TypeError,
        match=r"The LinspaceGrid has not been instantiated correctly.",
    ):
        _fail_if_bruttolohn_m_linspace_grid_is_invalid(
            linspace_grid={
                "n_points": 10,
            },  # ty: ignore[invalid-argument-type]
            p_id_array=np.array([1, 2, 3]),
        )


def test_bruttolohn_m_linspace_grid_invalid_wrong_number_of_p_ids():
    @dataclass(frozen=True)
    class InvalidLinspaceGrid(LinspaceGridProtocol):
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


def test_linspace_grid_accepts_one_keyword_per_member_plus_n_points():
    """`LinspaceGrid` of a statically typed persona takes `p0..pN` and `n_points`.

    The annotation on `persona` is what gives this test its value: it makes type
    checkers resolve `LinspaceGrid` to `type[LinspaceGridProtocol]` rather than to
    an unknown type, so the protocol must declare a constructor accepting these
    keywords for the call below to type-check.
    """
    persona: OrigPersonaOverTime = SamplePersona
    grid = persona.LinspaceGrid(p0=1.0, p1=2.0, p2=3.0, n_points=5)
    assert grid.n_points == 5


def test_bruttolohn_m_linspace_grid_invalid_bottom_larger_than_top():
    linspace_grid = SamplePersona.LinspaceGrid(
        p0=SamplePersona.LinspaceRange(bottom=0, top=1),
        p1=SamplePersona.LinspaceRange(bottom=0, top=1),
        p2=SamplePersona.LinspaceRange(bottom=1, top=0),
        n_points=10,
    )
    with pytest.raises(
        ValueError,
        match=r"The lower bound of the linspace must be less than the upper bound.",
    ):
        _fail_if_bruttolohn_m_linspace_grid_is_invalid(
            linspace_grid=linspace_grid,
            p_id_array=np.array([0, 1, 2]),
        )


def test_bruttolohn_m_linspace_grid_invalid_n_points_zero():
    def call_invalid():
        linspace_grid = SamplePersona.LinspaceGrid(
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
        match=r"The number of points in the linspace must be greater than 0.",
    ):
        call_invalid()


def test_bruttolohn_m_is_default_value_if_no_linspace_grid_is_provided():
    persona = SamplePersona(
        policy_date_str="2015-01-01",
        evaluation_date_str="2015-01-01",
    )
    assert_array_equal(
        persona.input_data_tree["einnahmen"]["bruttolohn_m"],
        np.array([1, 2, 3]),
    )


def test_bruttolohn_m_is_upserted_if_linspace_grid_is_provided():
    persona = SamplePersona(
        policy_date_str="2015-01-01",
        evaluation_date_str="2015-01-01",
        bruttolohn_m_linspace_grid=SamplePersona.LinspaceGrid(
            p0=SamplePersona.LinspaceRange(bottom=0, top=1),
            p1=SamplePersona.LinspaceRange(bottom=0, top=1),
            p2=0,
            n_points=2,
        ),
    )
    assert_array_equal(
        persona.input_data_tree["einnahmen"]["bruttolohn_m"],
        np.array([0, 0, 0, 1, 1, 0]),
    )


def test_bruttolohn_m_is_upserted_if_linspace_grid_is_provided_with_constant_value():
    persona = SamplePersona(
        policy_date_str="2015-01-01",
        evaluation_date_str="2015-01-01",
        bruttolohn_m_linspace_grid=SamplePersona.LinspaceGrid(
            p0=1,
            p1=SamplePersona.LinspaceRange(bottom=0, top=1),
            p2=2,
            n_points=2,
        ),
    )
    assert_array_equal(
        persona.input_data_tree["einnahmen"]["bruttolohn_m"],
        np.array([1, 0, 2, 1, 1, 2]),
    )


def test_tt_targets_include_hh_id_if_multiple_households_in_persona():
    persona = SamplePersona(
        policy_date_str="2015-01-01",
        evaluation_date_str="2015-01-01",
    )

    upserted_persona = persona.upsert_input_data({"x": np.array([0, 0, 1, 1, 2, 2])})
    assert "hh_id" in upserted_persona.tt_targets_tree

    persona_with_bruttolohn_m_linspace_grid = SamplePersona(
        policy_date_str="2015-01-01",
        evaluation_date_str="2015-01-01",
        bruttolohn_m_linspace_grid=SamplePersona.LinspaceGrid(
            p0=SamplePersona.LinspaceRange(bottom=0, top=1),
            p1=SamplePersona.LinspaceRange(bottom=0, top=1),
            p2=0,
            n_points=2,
        ),
    )

    assert "hh_id" in persona_with_bruttolohn_m_linspace_grid.tt_targets_tree


def test_persona_call_fails_if_input_data_differs_in_length_from_p_id_array():
    with pytest.raises(
        ValueError,
        match=r"The input data for input_1 has a different length than the p_id array.",
    ):
        SamplePersonaWithInvalidLengthOfInputData(
            policy_date_str="2015-01-01",
        )


def test_persona_description_is_string_after_instantiation():
    persona = SamplePersona(
        policy_date_str="2015-01-01",
        evaluation_date_str="2015-01-01",
    )
    assert isinstance(persona.description, str)


@persona_description(description="A persona built from explicitly passed elements.")
def explicit_description():
    pass


@persona_pid_element()
def explicit_p_id() -> np.ndarray:
    return np.array([0, 1])


@persona_input_element(tt_qname="hh_id")
def explicit_hh_id() -> np.ndarray:
    return np.array([0, 0])


@persona_input_element(tt_qname="einnahmen__bruttolohn_m")
def explicit_bruttolohn_m() -> np.ndarray:
    return np.array([100.0, 200.0])


@persona_target_element()
def einkommensteuer__betrag_y():
    pass


COMPLETE_ELEMENTS = (
    explicit_description,
    explicit_p_id,
    explicit_hh_id,
    explicit_bruttolohn_m,
    einkommensteuer__betrag_y,
)


@persona_input_element()
def einnahmen__bruttolohn_m() -> np.ndarray:
    return np.array([10.0, 20.0, 30.0])


@persona_input_element()
def some_new_input_element() -> np.ndarray:
    return np.array([7, 8, 9])


@persona_target_element()
def some_new_target_qname():
    pass


@persona_input_element()
def double_of_base_input_element(
    some_time_dependent_persona_input_element: np.ndarray,
) -> np.ndarray:
    return 2 * some_time_dependent_persona_input_element


@persona_description(
    description="Derived description since 2010.",
    start_date="2010-01-01",
)
def description_since_2010():
    pass


@persona_pid_element()
def p_id_with_two_members() -> np.ndarray:
    return np.array([0, 1])


def test_persona_from_explicit_elements_has_expected_input_data():
    """Explicitly passed input elements make up the persona's input data."""
    persona = OrigPersonaOverTime(elements=COMPLETE_ELEMENTS)(
        policy_date_str="2021-01-01"
    )
    assert_array_equal(
        persona.input_data_tree["einnahmen"]["bruttolohn_m"],
        np.array([100.0, 200.0]),
    )


def test_persona_from_explicit_elements_has_expected_targets():
    """Explicitly passed target elements make up the persona's targets."""
    persona = OrigPersonaOverTime(elements=COMPLETE_ELEMENTS)(
        policy_date_str="2021-01-01"
    )
    assert persona.tt_targets_tree == {"einkommensteuer": {"betrag_y": None}}


def test_persona_from_explicit_elements_has_expected_description():
    """The active description of the passed elements is the persona's description."""
    persona = OrigPersonaOverTime(elements=COMPLETE_ELEMENTS)(
        policy_date_str="2021-01-01"
    )
    assert persona.description == "A persona built from explicitly passed elements."


def test_persona_from_explicit_elements_fails_without_description():
    with pytest.raises(ValueError, match="No PersonaDescription found"):
        OrigPersonaOverTime(
            elements=(explicit_p_id, explicit_hh_id, explicit_bruttolohn_m)
        )(policy_date_str="2021-01-01")


def test_persona_from_explicit_elements_fails_without_p_id_element():
    with pytest.raises(ValueError, match="Expected exactly one p_id array"):
        OrigPersonaOverTime(elements=(explicit_description, explicit_hh_id))


def test_persona_fails_if_both_path_and_elements_are_passed():
    with pytest.raises(
        ValueError,
        match="Pass exactly one of 'path_to_persona_elements' and 'elements'",
    ):
        OrigPersonaOverTime(
            path_to_persona_elements=Path("some_persona_elements.py"),
            elements=COMPLETE_ELEMENTS,
        )


def test_persona_fails_if_neither_path_nor_elements_are_passed():
    with pytest.raises(
        ValueError,
        match="Pass exactly one of 'path_to_persona_elements' and 'elements'",
    ):
        OrigPersonaOverTime()


def test_passed_element_replaces_base_element_of_same_name():
    derived = SamplePersona.upsert_elements(einnahmen__bruttolohn_m)
    assert_array_equal(
        derived(policy_date_str="2021-01-01").input_data_tree["einnahmen"][
            "bruttolohn_m"
        ],
        np.array([10.0, 20.0, 30.0]),
    )


def test_passed_input_element_is_added_to_base_input_data():
    derived = SamplePersona.upsert_elements(some_new_input_element)
    assert_array_equal(
        derived(policy_date_str="2021-01-01").input_data_tree["some_new_input_element"],
        np.array([7, 8, 9]),
    )


def test_passed_target_element_is_added_to_base_targets():
    derived = SamplePersona.upsert_elements(some_new_target_qname)
    assert (
        "some_new_target_qname" in derived(policy_date_str="2021-01-01").tt_targets_tree
    )


def test_passed_element_may_depend_on_base_element():
    derived = SamplePersona.upsert_elements(double_of_base_input_element)
    assert_array_equal(
        derived(policy_date_str="2021-01-01").input_data_tree[
            "double_of_base_input_element"
        ],
        np.array([2, 4, 6]),
    )


def test_passed_description_replaces_base_description_of_same_name():
    derived = SamplePersona.upsert_elements(description_since_2010)
    assert (
        derived(policy_date_str="2021-01-01").description
        == "Derived description since 2010."
    )


def test_base_description_applies_when_passed_description_is_inactive():
    derived = SamplePersona.upsert_elements(description_since_2010)
    assert (
        derived(policy_date_str="2005-01-01").description
        == "Test description valid until 2009."
    )


def test_overlap_among_passed_elements_raises():
    derived = SamplePersona.upsert_elements(
        input_element_always_active, another_input_element_always_active
    )
    with pytest.raises(
        ValueError, match=r"Overlapping qnames: \{'input_element_always_active'\}"
    ):
        derived(policy_date_str="2021-01-01")


def test_passed_p_id_element_replaces_base_p_id_element_in_linspace_grid():
    derived = SamplePersona.upsert_elements(p_id_with_two_members)
    assert list(inspect.signature(derived.LinspaceGrid).parameters) == [
        "p0",
        "p1",
        "n_points",
    ]


def test_derived_persona_raises_base_error_outside_base_date_range():
    derived = SamplePersonaWithStartAndEndDate.upsert_elements(some_new_input_element)
    with pytest.raises(
        NotImplementedError, match=r"This Persona is not implemented before 2015\."
    ):
        derived(policy_date_str="2014-01-01")


def test_bruttolohn_m_linspace_grid_works_on_derived_persona():
    derived = SamplePersona.upsert_elements(some_new_input_element)
    persona = derived(
        policy_date_str="2015-01-01",
        bruttolohn_m_linspace_grid=derived.LinspaceGrid(
            p0=derived.LinspaceRange(bottom=0, top=1),
            p1=derived.LinspaceRange(bottom=0, top=1),
            p2=0,
            n_points=2,
        ),
    )
    assert_array_equal(
        persona.input_data_tree["einnahmen"]["bruttolohn_m"],
        np.array([0, 0, 0, 1, 1, 0]),
    )


@persona_input_element()
def another_new_input_element() -> np.ndarray:
    return np.array([4, 5, 6])


@persona_input_element()
def some_target_qname() -> np.ndarray:
    return np.array([1, 1, 1])


def test_chained_extension_merges_elements_of_all_levels():
    """A persona extending a derived persona sees the elements of every level."""
    mid = SamplePersona.upsert_elements(some_new_input_element)
    leaf = mid.upsert_elements(another_new_input_element)
    input_data_tree = leaf(policy_date_str="2021-01-01").input_data_tree
    assert {
        "some_time_dependent_persona_input_element": input_data_tree[
            "some_time_dependent_persona_input_element"
        ].tolist(),
        "some_new_input_element": input_data_tree["some_new_input_element"].tolist(),
        "another_new_input_element": input_data_tree[
            "another_new_input_element"
        ].tolist(),
    } == {
        "some_time_dependent_persona_input_element": [1, 2, 3],
        "some_new_input_element": [7, 8, 9],
        "another_new_input_element": [4, 5, 6],
    }


def test_passed_input_element_replaces_base_target_of_same_name():
    """A passed element replaces the base element of the same name whatever its kind."""
    derived = SamplePersona.upsert_elements(some_target_qname)
    persona = derived(policy_date_str="2021-01-01")
    assert "some_target_qname" not in persona.tt_targets_tree
