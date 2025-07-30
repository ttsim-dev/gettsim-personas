import numpy as np

from gettsim_personas import GETTSIMPersonas


def test_end_to_end():
    persona = GETTSIMPersonas.einkommensteuer_sozialabgaben.couple_1_child(
        date_str="2020-01-01",
        bruttolohn_m_linspace_spec={
            0: {"bottom": 0, "top": 100000},
            1: {"bottom": 0, "top": 100000},
            2: {"bottom": 0, "top": 100000},
        },
        n_points=10,
    )
    assert len(persona.input_data_tree["p_id"]) == 30
    assert len(persona.input_data_tree["einnahmen"]["bruttolohn_m"]) == 30
    assert np.array_equal(
        persona.input_data_tree["einnahmen"]["bruttolohn_m"][:3],
        np.array([0, 0, 0]),
    )
    assert np.array_equal(
        persona.input_data_tree["einnahmen"]["bruttolohn_m"][-3:],
        np.array([100000, 100000, 100000]),
    )
