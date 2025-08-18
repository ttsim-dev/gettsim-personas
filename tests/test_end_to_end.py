import numpy as np
from gettsim import InputData, MainTarget, TTTargets, main

from gettsim_personas.einkommensteuer_sozialabgaben import Couple1Child


def test_end_to_end():
    policy_date_str = "2020-01-01"
    persona = Couple1Child(
        policy_date=policy_date_str,
        bruttolohn_m_linspace_grid=Couple1Child.LinspaceGrid(
            p0=Couple1Child.LinspaceRange(bottom=0, top=5000),
            p1=Couple1Child.LinspaceRange(bottom=0, top=5000),
            p2=Couple1Child.LinspaceRange(bottom=0, top=0),
            n_points=10,
        ),
    )
    main(
        main_target=MainTarget.results.tree,
        input_data=InputData.tree(persona.input_data_tree),
        tt_targets=TTTargets(tree=persona.tt_targets_tree),
        policy_date_str=policy_date_str,
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
        policy_date=policy_date_str,
    )
    assert len(persona.input_data_tree["einnahmen"]["bruttolohn_m"]) == 3
