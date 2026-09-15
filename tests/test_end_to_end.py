import numpy as np
from gettsim import InputData, MainTarget, TTTargets, main

import gettsim_personas
from gettsim_personas import OrigPersonaOverTime, persona_input_element
from gettsim_personas.einkommensteuer_sozialabgaben import Couple1Child


def test_end_to_end():
    policy_date_str = "2020-01-01"
    persona = Couple1Child(
        policy_date_str=policy_date_str,
        bruttolohn_m_linspace_grid=Couple1Child.LinspaceGrid(
            p0=Couple1Child.LinspaceRange(bottom=0, top=5000),
            p1=Couple1Child.LinspaceRange(bottom=0, top=5000),
            p2=0,
            n_points=10,
        ),
    )
    main(
        main_target=MainTarget.results.tree,
        input_data=InputData.tree(persona.input_data_tree),
        tt_targets=TTTargets.tree(persona.tt_targets_tree),
        policy_date=persona.policy_date,
        include_warn_nodes=False,
    )

    assert len(persona.input_data_tree["p_id"]) == 30
    assert len(persona.input_data_tree["einnahmen"]["bruttolohn_m"]) == 30
    assert np.array_equal(
        persona.input_data_tree["einnahmen"]["bruttolohn_m"][:3],
        np.array([0, 0, 0]),
    )
    assert np.array_equal(
        persona.input_data_tree["einnahmen"]["bruttolohn_m"][-3:],
        np.array([5000, 5000, 0]),
    )


def test_can_create_persona_with_default_bruttolohn():
    policy_date_str = "2020-01-01"
    persona = Couple1Child(
        policy_date_str=policy_date_str,
    )
    assert len(persona.input_data_tree["einnahmen"]["bruttolohn_m"]) == 3


def test_can_upsert_input_data():
    policy_date_str = "2020-01-01"
    persona = Couple1Child(
        policy_date_str=policy_date_str,
    )
    upserted_persona = persona.upsert_input_data(
        input_data_to_upsert={
            "einnahmen": {"bruttolohn_m": np.array([1, 2, 3, 4, 5, 6])}
        }
    )
    assert len(upserted_persona.input_data_tree["einnahmen"]["bruttolohn_m"]) == 6
    assert np.array_equal(
        upserted_persona.input_data_tree["einnahmen"]["bruttolohn_m"],
        np.array([1, 2, 3, 4, 5, 6]),
    )


def test_persona_building_blocks_are_importable_from_public_package():
    """The names needed to define a persona are part of the public API."""
    expected = {
        "LinspaceRange",
        "OrigPersonaOverTime",
        "persona_description",
        "persona_input_element",
        "persona_pid_element",
        "persona_target_element",
    }
    assert expected <= set(dir(gettsim_personas))


@persona_input_element(tt_qname="einnahmen__bruttolohn_m", start_date="2020-01-01")
def bruttolohn_m_since_2020() -> np.ndarray:
    return np.array([1234.0, 2345.0, 0.0])


ExtendedCouple1Child = OrigPersonaOverTime(
    elements=(bruttolohn_m_since_2020,),
    base=Couple1Child,
)


def test_extended_persona_uses_override_for_policy_date_in_its_active_range():
    persona = ExtendedCouple1Child(policy_date_str="2021-01-01")
    main(
        main_target=MainTarget.results.tree,
        input_data=InputData.tree(persona.input_data_tree),
        tt_targets=TTTargets.tree(persona.tt_targets_tree),
        policy_date=persona.policy_date,
        include_warn_nodes=False,
    )
    assert np.array_equal(
        persona.input_data_tree["einnahmen"]["bruttolohn_m"],
        np.array([1234.0, 2345.0, 0.0]),
    )


def test_extended_persona_uses_base_value_for_policy_date_before_override():
    persona = ExtendedCouple1Child(policy_date_str="2019-01-01")
    assert np.array_equal(
        persona.input_data_tree["einnahmen"]["bruttolohn_m"],
        np.array([3000, 3000, 0]),
    )
