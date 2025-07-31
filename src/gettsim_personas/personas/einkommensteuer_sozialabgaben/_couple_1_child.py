import numpy as np
from dataclasses import dataclass
from gettsim_personas.persona_objects import Persona

@dataclass(frozen=True)
class _AtomicRangeSpec:
    min: float
    max: float

@dataclass(frozen=True)
class RangeSpec3Persons:

    p0: _AtomicRangeSpec
    p1: _AtomicRangeSpec
    p2: _AtomicRangeSpec


# Include all the common stuff in the decorator
@make_persona(
        policy_date: str,
        evaluation_date: str | None = None,
        n_points: int = 101,
)
def persona(**kwargs) -> Persona:
    """Jointly taxed married couple with one child, who never applies for
    any means-tested transfers.

    Use safely for upper-income households where this provides a
    minimal set of required input values.

    Only use for lower-income households if you want to know what happens
    in the absence of means-tested transfers.
    """
    print(__doc__)

    return Persona(
        description=__doc__,
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
