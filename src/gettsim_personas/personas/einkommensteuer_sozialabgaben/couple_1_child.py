import numpy as np

from gettsim_personas.persona_objects import Persona

couple_1_child = Persona(
    description=(
        """Persona to compute income taxes and social insurance contributions. Jointly
        taxed married couple with one child. All transfers are set to zero; don't use
        this persona for low- to mid-income households, as they may be eligible for
        (means-tested) transfers."""
    ),
    input_data_tree={
        "alter": np.array([30, 30, 10]),
        "arbeitsstunden_w": np.array([39, 39, 0]),
        "behinderungsgrad": np.array([0, 0, 0]),
        "geburtsjahr": np.array([1995, 1995, 2015]),
        "p_id": np.array([0, 1, 2]),
        "wohnort_ost_hh": np.array([False, False, False]),
        "einnahmen": {
            "bruttolohn_m": np.array([3000, 3000, 0]),
            "kapitalerträge_y": np.array([500.0, 0.0, 0]),
            "renten": {
                "gesetzliche_m": np.array([0, 0, 0]),
                "geförderte_private_vorsorge_m": np.array([0, 0, 0]),
                "sonstige_private_vorsorge_m": np.array([0, 0, 0]),
                "betriebliche_altersvorsorge_m": np.array([0, 0, 0]),
            },
        },
        "einkommensteuer": {
            "einkünfte": {
                "ist_hauptberuflich_selbstständig": np.array([False, False, False]),
                "aus_gewerbebetrieb": {
                    "betrag_m": np.array([0, 0, 0]),
                },
                "aus_vermietung_und_verpachtung": {
                    "betrag_m": np.array([0, 0, 0]),
                },
                "aus_forst_und_landwirtschaft": {
                    "betrag_m": np.array([0, 0, 0]),
                },
                "aus_selbstständiger_arbeit": {
                    "betrag_m": np.array([0, 0, 0]),
                },
                "sonstige": {
                    "alle_weiteren_m": np.array([0, 0, 0]),
                },
            },
            "abzüge": {
                "beitrag_private_rentenversicherung_m": np.array([0, 0, 0]),
                "kinderbetreuungskosten_m": np.array([0.0, 0.0, 100.0]),
                "p_id_kinderbetreuungskostenträger": np.array([-1, -1, 0]),
            },
            "gemeinsam_veranlagt": np.array([True, True, False]),
        },
        "sozialversicherung": {
            "rente": {
                "jahr_renteneintritt": np.array([2060, 2060, 2080]),
            },
            "kranken": {
                "beitrag": {
                    "privat_versichert": np.array([False, False, False]),
                },
            },
            "pflege": {
                "beitrag": {
                    "hat_kinder": np.array([True, True, False]),
                },
            },
        },
        "familie": {
            "alleinerziehend": np.array([False, False, False]),
            "p_id_ehepartner": np.array([1, 0, -1]),
            "p_id_elternteil_1": np.array([-1, -1, 0]),
            "p_id_elternteil_2": np.array([-1, -1, 1]),
        },
        "kindergeld": {
            "in_ausbildung": np.array([False, False, False]),
            "p_id_empfänger": np.array([-1, -1, 0]),
        },
    },
    tt_targets_tree={
        "einkommensteuer": {
            "betrag_m_sn": None,
        },
        "sozialversicherung": {
            "pflege": {
                "beitrag": {
                    "betrag_versicherter_m": None,
                },
            },
            "kranken": {
                "beitrag": {
                    "betrag_versicherter_m": None,
                },
            },
            "rente": {
                "beitrag": {
                    "betrag_versicherter_m": None,
                },
            },
            "arbeitslosen": {
                "beitrag": {
                    "betrag_versicherter_m": None,
                },
            },
        },
    },
)
