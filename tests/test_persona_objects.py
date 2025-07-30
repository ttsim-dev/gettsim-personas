"""Tests for persona_objects module."""

from datetime import date

import pytest

from gettsim_personas.persona_objects import Persona, PersonaCollection


def test_persona_collection_without_overlap():
    persona1 = Persona(
        description="Persona 1",
        input_data_tree={},
        tt_targets_tree={},
        start_date=date(2020, 1, 1),
        end_date=date(2020, 12, 31),
    )

    persona2 = Persona(
        description="Persona 2",
        input_data_tree={},
        tt_targets_tree={},
        start_date=date(2021, 1, 1),
        end_date=date(2021, 12, 31),
    )

    collection = PersonaCollection(personas=[persona1, persona2])
    assert len(collection.personas) == 2


def test_persona_collection_with_overlap():
    persona1 = Persona(
        description="Persona 1",
        input_data_tree={},
        tt_targets_tree={},
        start_date=date(2020, 1, 1),
        end_date=date(2020, 12, 31),
    )

    persona2 = Persona(
        description="Persona 2",
        input_data_tree={},
        tt_targets_tree={},
        start_date=date(2020, 6, 1),
        end_date=date(2021, 6, 30),
    )

    with pytest.raises(
        ValueError, match="Multiple personas are active at the same date"
    ):
        PersonaCollection(personas=[persona1, persona2])


def test_persona_collection_single_persona():
    persona = Persona(
        description="Single Persona",
        input_data_tree={},
        tt_targets_tree={},
        start_date=date(2020, 1, 1),
        end_date=date(2020, 12, 31),
    )

    collection = PersonaCollection(personas=[persona])
    assert len(collection.personas) == 1


def test_persona_collection_empty():
    collection = PersonaCollection(personas=[])
    assert len(collection.personas) == 0


def test_persona_collection_call_method():
    persona1 = Persona(
        description="Persona 1",
        input_data_tree={},
        tt_targets_tree={},
        start_date=date(2020, 1, 1),
        end_date=date(2020, 12, 31),
    )

    persona2 = Persona(
        description="Persona 2",
        input_data_tree={},
        tt_targets_tree={},
        start_date=date(2021, 1, 1),
        end_date=date(2021, 12, 31),
    )

    collection = PersonaCollection(personas=[persona1, persona2])

    found_persona = collection(policy_date_str="2020-06-15")
    assert found_persona == persona1

    found_persona = collection(policy_date_str="2021-06-15")
    assert found_persona == persona2

    with pytest.raises(NotImplementedError, match="No persona found for date"):
        collection(policy_date_str="2019-06-15")
