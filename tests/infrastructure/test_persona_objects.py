import datetime

import pytest
from personas_for_testing import (
    SamplePersona,
    SamplePersonaWithOverlappingElements,
)

from gettsim_personas.persona_objects import (
    _fail_if_active_tt_qnames_overlap,
    _fail_if_not_exactly_one_description_is_active,
    persona_description,
    persona_input_element,
)


@persona_input_element()
def persona_input_element_always_active():
    return 1


@persona_input_element(start_date="2010-01-01")
def persona_input_element_active_since_2010():
    return 1


@persona_input_element(tt_qname="persona_input_element_always_active")
def another_persona_input_element_always_active():
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
        "some_persona_input_element",
        "persona_input_element_until_2009",
        "persona_input_element_since_2010",
        "some_irrelevant_name",
        "some_qname_depending_on_another_qname",
        "true_if_evaluation_year_at_least_2015",
        "qname_depending_on_evaluation_date_and_another_qname",
        "some_target_qname",
        "some_target_qname_until_2009",
        "some_target_qname_since_2010",
    }
    orig_names = {el.orig_name for el in SamplePersona.orig_elements()}
    assert expected_orig_names == orig_names

    expected_tt_qnames = {
        "some_persona_input_element",
        "persona_input_element_until_2009",
        "persona_input_element_since_2010",
        "input_qname_via_decorator",
        "some_qname_depending_on_another_qname",
        "true_if_evaluation_year_at_least_2015",
        "qname_depending_on_evaluation_date_and_another_qname",
        "some_target_qname",
        "some_target_qname_until_2009",
        "some_target_qname_since_2010",
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
                "some_persona_input_element",
                "persona_input_element_until_2009",
                "some_irrelevant_name",
                "some_qname_depending_on_another_qname",
                "true_if_evaluation_year_at_least_2015",
                "qname_depending_on_evaluation_date_and_another_qname",
                "some_target_qname",
                "some_target_qname_until_2009",
            },
        ),
        (
            datetime.date(2010, 1, 1),
            {
                "description_since_2010",
                "some_persona_input_element",
                "persona_input_element_since_2010",
                "some_irrelevant_name",
                "some_qname_depending_on_another_qname",
                "true_if_evaluation_year_at_least_2015",
                "qname_depending_on_evaluation_date_and_another_qname",
                "some_target_qname",
                "some_target_qname_since_2010",
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
        match=r"Overlapping qnames: \{'persona_input_element_always_active'\}",
    ):
        _fail_if_active_tt_qnames_overlap(
            active_elements=[
                persona_input_element_always_active,
                another_persona_input_element_always_active,
                persona_input_element_active_since_2010,
            ],
            path_to_persona_elements="",
        )


def test_fail_if_active_tt_qnames_overlap_via_persona_object():
    with pytest.raises(ValueError, match=r"Overlapping qnames: \{'input_1'\}"):
        SamplePersonaWithOverlappingElements(policy_date="2015-01-01")


def test_do_not_fail_if_active_qnames_do_not_overlap():
    _fail_if_active_tt_qnames_overlap(
        active_elements=[
            persona_input_element_always_active,
            persona_input_element_active_since_2010,
        ],
        path_to_persona_elements="",
    )


def test_fail_if_multiple_descriptions_are_active():
    with pytest.raises(ValueError, match="More than one PersonaDescription is active"):
        _fail_if_not_exactly_one_description_is_active(
            active_elements=[
                active_description,
                another_active_description,
                persona_input_element_always_active,
            ],
            path_to_persona_elements="",
        )


def test_do_not_fail_if_only_one_description_is_active():
    _fail_if_not_exactly_one_description_is_active(
        active_elements=[
            active_description,
            persona_input_element_always_active,
        ],
        path_to_persona_elements="",
    )


# def test_persona_collection_without_overlap():
#     persona1 = Persona(
#         description="Persona 1",
#         input_data_tree={},
#         tt_targets_tree={},
#         start_date=date(2020, 1, 1),
#         end_date=date(2020, 12, 31),
#     )

#     persona2 = Persona(
#         description="Persona 2",
#         input_data_tree={},
#         tt_targets_tree={},
#         start_date=date(2021, 1, 1),
#         end_date=date(2021, 12, 31),
#     )

#     collection = PersonaCollection(path=tuple(), personas=[persona1, persona2])
#     assert len(collection.personas) == 2


# def test_persona_collection_with_overlap():
#     persona1 = Persona(
#         description="Persona 1",
#         input_data_tree={},
#         tt_targets_tree={},
#         start_date=date(2020, 1, 1),
#         end_date=date(2020, 12, 31),
#     )

#     persona2 = Persona(
#         description="Persona 2",
#         input_data_tree={},
#         tt_targets_tree={},
#         start_date=date(2020, 6, 1),
#         end_date=date(2021, 6, 30),
#     )

#     with pytest.raises(
#         ValueError, match="Multiple personas are active at the same date"
#     ):
#         PersonaCollection(path=tuple(), personas=[persona1, persona2])


# def test_persona_collection_single_persona():
#     persona = Persona(
#         description="Single Persona",
#         input_data_tree={},
#         tt_targets_tree={},
#         start_date=date(2020, 1, 1),
#         end_date=date(2020, 12, 31),
#     )

#     collection = PersonaCollection(path=tuple(), personas=[persona])
#     assert len(collection.personas) == 1


# def test_persona_collection_empty():
#     collection = PersonaCollection(path=tuple(), personas=[])
#     assert len(collection.personas) == 0


# def test_persona_collection_call_method():
#     persona1 = Persona(
#         description="Persona 1",
#         input_data_tree={},
#         tt_targets_tree={},
#         start_date=date(2020, 1, 1),
#         end_date=date(2020, 12, 31),
#     )

#     persona2 = Persona(
#         description="Persona 2",
#         input_data_tree={},
#         tt_targets_tree={},
#         start_date=date(2021, 1, 1),
#         end_date=date(2021, 12, 31),
#     )

#     not_implemented_error = PersonaNotImplementedError("Expected error message.")

#     collection = PersonaCollection(
#         path=tuple(),
#         personas=[persona1, persona2],
#         not_implemented_error=not_implemented_error,
#     )

#     found_persona = collection(policy_date_str="2020-06-15")
#     assert found_persona == persona1

#     found_persona = collection(policy_date_str="2021-06-15")
#     assert found_persona == persona2

#     with pytest.raises(PersonaNotImplementedError, match="Expected error message."):
#         collection(policy_date_str="2019-06-15")
