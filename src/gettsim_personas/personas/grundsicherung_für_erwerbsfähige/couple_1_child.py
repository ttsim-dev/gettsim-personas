from datetime import date

import numpy as np

from gettsim_personas.persona_objects import Persona, PersonaNotImplementedError

alg_2_persona = Persona(
    description="""Persona to compute mean-tested transfers for low-income households.
    Jointly taxed married couple with one child. Income from pensions, parental leave
    benefits and subsistence benefits for the elderly are set to zero.""",
    start_date=date(2005, 1, 1),
    end_date=date(2022, 12, 31),
    input_data_tree={
        "p_id": np.array([0, 1, 2]),
        "hh_id": np.array([0, 0, 0]),
        "alter": np.array([30, 30, 6]),
        "alter_monate": np.array([360, 360, 60]),
        "arbeitslosengeld_2": {"p_id_einstandspartner": np.array([1, 0, -1])},
        "arbeitsstunden_w": np.array([15, 0, 0]),
        "behinderungsgrad": np.array([0, 0, 0]),
        "einkommensteuer": {
            "abzüge": {
                "beitrag_private_rentenversicherung_m": np.array([0, 0, 0]),
                "kinderbetreuungskosten_m": np.array([0, 0, 100]),
                "p_id_kinderbetreuungskostenträger": np.array([-1, -1, 0]),
            },
            "einkünfte": {
                "aus_forst_und_landwirtschaft": {"betrag_y": np.array([0, 0, 0])},
                "aus_gewerbebetrieb": {"betrag_y": np.array([0, 0, 0])},
                "aus_selbstständiger_arbeit": {"betrag_y": np.array([0, 0, 0])},
                "aus_vermietung_und_verpachtung": {"betrag_y": np.array([0, 0, 0])},
                "ist_hauptberuflich_selbstständig": np.array([False, False, False]),
                "sonstige": {"alle_weiteren_y": np.array([0, 0, 0])},
            },
            "gemeinsam_veranlagt": np.array([True, True, False]),
        },
        "einnahmen": {
            "bruttolohn_m": np.array([1000, 0, 0]),
            "kapitalerträge_y": np.array([0.0, 0.0, 0]),
            "renten": {
                "gesetzliche_m": np.array([0, 0, 0]),
                "betriebliche_altersvorsorge_m": np.array([0, 0, 0]),
                "geförderte_private_vorsorge_m": np.array([0, 0, 0]),
                "sonstige_private_vorsorge_m": np.array([0, 0, 0]),
            },
        },
        "elterngeld": {"betrag_m": np.array([0, 0, 0])},
        "familie": {
            "alleinerziehend": np.array([False, False, False]),
            "p_id_ehepartner": np.array([1, 0, -1]),
            "p_id_elternteil_1": np.array([-1, -1, 0]),
            "p_id_elternteil_2": np.array([-1, -1, 1]),
        },
        "geburtsjahr": np.array([1995, 1995, 2015]),
        "geburtsmonat": np.array([1, 1, 1]),
        "grundsicherung": {"im_alter": {"betrag_m_eg": np.array([0, 0, 0])}},
        "kindergeld": {
            "in_ausbildung": np.array([False, False, False]),
            "p_id_empfänger": np.array([-1, -1, 0]),
        },
        "sozialversicherung": {
            "arbeitslosen": {
                "arbeitssuchend": np.array([False, False, False]),
                "mean_nettoeinkommen_in_12_monaten_vor_arbeitslosigkeit_m": np.array(
                    [0, 0, 0]
                ),
                "monate_beitragspflichtig_versichert_in_letzten_30_monaten": np.array(
                    [0, 0, 0]
                ),
                "monate_durchgängigen_bezugs_von_arbeitslosengeld": np.array([0, 0, 0]),
                "monate_sozialversicherungspflichtiger_beschäftigung_in_letzten_5_jahren": np.array(
                    [0, 0, 0]
                ),
            },
            "kranken": {
                "beitrag": {"privat_versichert": np.array([False, False, False])}
            },
            "pflege": {"beitrag": {"hat_kinder": np.array([True, True, False])}},
            "rente": {
                "bezieht_rente": np.array([False, False, False]),
                "jahr_renteneintritt": np.array([2070, 2070, 2090]),
            },
        },
        "unterhalt": {"tatsächlich_erhaltener_betrag_m": np.array([0, 0, 0])},
        "unterhaltsvorschuss": {"betrag_m": np.array([0, 0, 0])},
        "vermögen": np.array([0, 0, 0]),
        "wohnen": {
            "bewohnt_eigentum_hh": np.array([False, False, False]),
            "bruttokaltmiete_m_hh": np.array([0, 0, 0]),
            "heizkosten_m_hh": np.array([0, 0, 0]),
            "wohnfläche_hh": np.array([0, 0, 0]),
            "baujahr_immobilie_hh": np.array([2000, 2000, 2000]),
        },
        "wohngeld": {"mietstufe_hh": np.array([5, 5, 5])},
        "wohnort_ost_hh": np.array([False, False, False]),
    },
    tt_targets_tree={
        "einkommensteuer": {
            "betrag_m_sn": None,
        },
        "sozialversicherung": {
            "rente": {
                "beitrag": {
                    "betrag_versicherter_m": None,
                },
            },
            "kranken": {
                "beitrag": {
                    "betrag_versicherter_m": None,
                },
            },
            "pflege": {
                "beitrag": {
                    "betrag_versicherter_m": None,
                },
            },
            "arbeitslosen": {
                "beitrag": {
                    "betrag_versicherter_m": None,
                },
                "betrag_m": None,
            },
        },
        "arbeitslosengeld_2": {
            "betrag_m_bg": None,
        },
        "wohngeld": {
            "betrag_m_wthh": None,
        },
        "kinderzuschlag": {
            "betrag_m_bg": None,
        },
        "kindergeld": {
            "betrag_m": None,
        },
    },
)

bürgergeld_persona = Persona(
    description="""Persona to compute mean-tested transfers for low-income households.
    Jointly taxed married couple with one child. Income from pensions, parental leave
    benefits and subsistence benefits for the elderly are set to zero.""",
    start_date=date(2023, 1, 1),
    input_data_tree={
        "p_id": np.array([0, 1, 2]),
        "hh_id": np.array([0, 0, 0]),
        "alter": np.array([30, 30, 6]),
        "alter_monate": np.array([360, 360, 60]),
        "arbeitslosengeld_2": {
            "bezug_im_vorjahr": np.array([True, True, True]),
            "p_id_einstandspartner": np.array([1, 0, -1]),
        },
        "arbeitsstunden_w": np.array([15, 0, 0]),
        "behinderungsgrad": np.array([0, 0, 0]),
        "einkommensteuer": {
            "abzüge": {
                "beitrag_private_rentenversicherung_m": np.array([0, 0, 0]),
                "kinderbetreuungskosten_m": np.array([0, 0, 100]),
                "p_id_kinderbetreuungskostenträger": np.array([-1, -1, 0]),
            },
            "einkünfte": {
                "aus_forst_und_landwirtschaft": {"betrag_y": np.array([0, 0, 0])},
                "aus_gewerbebetrieb": {"betrag_y": np.array([0, 0, 0])},
                "aus_selbstständiger_arbeit": {"betrag_y": np.array([0, 0, 0])},
                "aus_vermietung_und_verpachtung": {"betrag_y": np.array([0, 0, 0])},
                "ist_hauptberuflich_selbstständig": np.array([False, False, False]),
                "sonstige": {"alle_weiteren_y": np.array([0, 0, 0])},
            },
            "gemeinsam_veranlagt": np.array([True, True, False]),
        },
        "einnahmen": {
            "bruttolohn_m": np.array([1000, 0, 0]),
            "kapitalerträge_y": np.array([0.0, 0.0, 0]),
            "renten": {
                "gesetzliche_m": np.array([0, 0, 0]),
                "betriebliche_altersvorsorge_m": np.array([0, 0, 0]),
                "geförderte_private_vorsorge_m": np.array([0, 0, 0]),
                "sonstige_private_vorsorge_m": np.array([0, 0, 0]),
            },
        },
        "elterngeld": {"betrag_m": np.array([0, 0, 0])},
        "familie": {
            "alleinerziehend": np.array([False, False, False]),
            "p_id_ehepartner": np.array([1, 0, -1]),
            "p_id_elternteil_1": np.array([-1, -1, 0]),
            "p_id_elternteil_2": np.array([-1, -1, 1]),
        },
        "geburtsjahr": np.array([1995, 1995, 2015]),
        "geburtsmonat": np.array([1, 1, 1]),
        "grundsicherung": {"im_alter": {"betrag_m_eg": np.array([0, 0, 0])}},
        "kindergeld": {
            "in_ausbildung": np.array([False, False, False]),
            "p_id_empfänger": np.array([-1, -1, 0]),
        },
        "sozialversicherung": {
            "arbeitslosen": {
                "arbeitssuchend": np.array([False, False, False]),
                "mean_nettoeinkommen_in_12_monaten_vor_arbeitslosigkeit_m": np.array(
                    [0, 0, 0]
                ),
                "monate_beitragspflichtig_versichert_in_letzten_30_monaten": np.array(
                    [0, 0, 0]
                ),
                "monate_durchgängigen_bezugs_von_arbeitslosengeld": np.array([0, 0, 0]),
                "monate_sozialversicherungspflichtiger_beschäftigung_in_letzten_5_jahren": np.array(
                    [0, 0, 0]
                ),
            },
            "kranken": {
                "beitrag": {"privat_versichert": np.array([False, False, False])}
            },
            "pflege": {"beitrag": {"hat_kinder": np.array([True, True, False])}},
            "rente": {
                "bezieht_rente": np.array([False, False, False]),
                "jahr_renteneintritt": np.array([2070, 2070, 2090]),
            },
        },
        "unterhalt": {"tatsächlich_erhaltener_betrag_m": np.array([0, 0, 0])},
        "unterhaltsvorschuss": {"betrag_m": np.array([0, 0, 0])},
        "vermögen": np.array([0, 0, 0]),
        "wohnen": {
            "bewohnt_eigentum_hh": np.array([False, False, False]),
            "bruttokaltmiete_m_hh": np.array([400, 400, 400]),
            "heizkosten_m_hh": np.array([80, 80, 80]),
            "wohnfläche_hh": np.array([50, 50, 50]),
            "baujahr_immobilie_hh": np.array([2000, 2000, 2000]),
        },
        "wohngeld": {"mietstufe_hh": np.array([5, 5, 5])},
        "wohnort_ost_hh": np.array([False, False, False]),
    },
    tt_targets_tree={
        "einkommensteuer": {
            "betrag_m_sn": None,
        },
        "sozialversicherung": {
            "rente": {
                "beitrag": {
                    "betrag_versicherter_m": None,
                },
            },
            "kranken": {
                "beitrag": {
                    "betrag_versicherter_m": None,
                },
            },
            "pflege": {
                "beitrag": {
                    "betrag_versicherter_m": None,
                },
            },
            "arbeitslosen": {
                "beitrag": {
                    "betrag_versicherter_m": None,
                },
                "betrag_m": None,
            },
        },
        "arbeitslosengeld_2": {
            "betrag_m_bg": None,
        },
        "wohngeld": {
            "betrag_m_wthh": None,
        },
        "kinderzuschlag": {
            "betrag_m_bg": None,
        },
        "kindergeld": {
            "betrag_m": None,
        },
    },
)


ERROR_IF_NO_ACTIVE_PERSONA_FOUND = PersonaNotImplementedError(
    "Personas are available from 2005. Basic income support is not implemented in "
    "GETTSIM before 2005."
)
