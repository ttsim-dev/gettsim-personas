import datetime

import numpy as np

from _gettsim_personas.persona_elements import (
    persona_description,
    persona_input_element,
    persona_pid_element,
    persona_target_element,
)


@persona_description(
    description="""Persona to compute mean-tested transfers for low-income single adults.
        Income from pensions, parental leave benefits, child-related transfers,
        and subsistence benefits for the elderly are set to zero.""",
    start_date="2005-01-01",
)
def description() -> None:
    pass


@persona_pid_element()
def p_id() -> np.ndarray:
    return np.array([0])


@persona_input_element()
def hh_id() -> np.ndarray:
    return np.array([0])


@persona_input_element()
def alter() -> np.ndarray:
    return np.array([30])


@persona_input_element()
def arbeitsstunden_w() -> np.ndarray:
    return np.array([39])


@persona_input_element()
def behinderungsgrad() -> np.ndarray:
    return np.array([0])


@persona_input_element()
def geburtsjahr(
    evaluation_date: datetime.date,
    alter: np.ndarray,
) -> np.ndarray:
    return evaluation_date.year - alter


@persona_input_element(end_date="2024-12-31")
def wohnort_ost_hh() -> np.ndarray:
    return np.array([False])


@persona_input_element()
def einnahmen__bruttolohn_m() -> np.ndarray:
    return np.array([2600])


@persona_input_element()
def einnahmen__kapitalerträge_y() -> np.ndarray:
    return np.array([0])


@persona_input_element()
def einkommensteuer__einkünfte__sonstige__rente__betrag_m() -> np.ndarray:
    return np.array([0])


@persona_input_element()
def sozialversicherung__kranken__beitrag__bemessungsgrundlage_rente_m() -> np.ndarray:
    return np.array([0])


@persona_input_element()
def einkommensteuer__einkünfte__ist_hauptberuflich_selbstständig() -> np.ndarray:
    return np.array([False])


@persona_input_element()
def einkommensteuer__einkünfte__aus_gewerbebetrieb__betrag_m() -> np.ndarray:
    return np.array([0])


@persona_input_element()
def einkommensteuer__einkünfte__aus_vermietung_und_verpachtung__betrag_m() -> (
    np.ndarray
):
    return np.array([0])


@persona_input_element()
def einkommensteuer__einkünfte__aus_forst_und_landwirtschaft__betrag_m() -> np.ndarray:
    return np.array([0])


@persona_input_element()
def einkommensteuer__einkünfte__aus_selbstständiger_arbeit__betrag_m() -> np.ndarray:
    return np.array([0])


@persona_input_element()
def einkommensteuer__einkünfte__sonstige__alle_weiteren_m() -> np.ndarray:
    return np.array([0])


@persona_input_element()
def einkommensteuer__abzüge__beitrag_private_rentenversicherung_m() -> np.ndarray:
    return np.array([0])


@persona_input_element()
def sozialversicherung__kranken__beitrag__privat_versichert() -> np.ndarray:
    return np.array([False])


@persona_input_element()
def einkommensteuer__gemeinsam_veranlagt() -> np.ndarray:
    return np.array([False])


@persona_input_element()
def familie__p_id_ehepartner() -> np.ndarray:
    return np.array([-1])


@persona_input_element()
def sozialversicherung__pflege__beitrag__hat_kinder() -> np.ndarray:
    return np.array([False])


@persona_input_element()
def familie__alleinerziehend() -> np.ndarray:
    return np.array([False])


@persona_input_element(start_date="2005-01-01", end_date="2022-12-31")
def arbeitslosengeld_2__p_id_einstandspartner() -> np.ndarray:
    return np.array([-1])  # Single -> kein Partner


@persona_input_element(start_date="2023-01-01")
def bürgergeld__p_id_einstandspartner() -> np.ndarray:
    return np.array([-1])


@persona_input_element(start_date="2023-01-01")
def bürgergeld__bezug_im_vorjahr() -> np.ndarray:
    return np.array([False])



@persona_input_element()
def wohnen__bewohnt_eigentum_hh() -> np.ndarray:
    return np.array([False])


@persona_input_element()
def wohnen__bruttokaltmiete_m_hh() -> np.ndarray:
    return np.array([450])  


@persona_input_element()
def wohnen__heizkosten_m_hh() -> np.ndarray:
    return np.array([50])


@persona_input_element()
def wohnen__wohnfläche_hh() -> np.ndarray:
    return np.array([45])


@persona_input_element(start_date="2005-01-01", end_date="2008-12-31")
def wohnen__baujahr_immobilie_hh() -> np.ndarray:
    return np.array([2000])


@persona_input_element()
def wohngeld__mietstufe_hh() -> np.ndarray:
    return np.array([3])  


@persona_input_element()
def vermögen() -> np.ndarray:
    return np.array([0])


@persona_input_element()
def unterhalt__tatsächlich_erhaltener_betrag_m() -> np.ndarray:
    return np.array([0])


@persona_input_element()
def unterhaltsvorschuss__betrag_m() -> np.ndarray:
    return np.array([0])


@persona_input_element()
def sozialversicherung__arbeitslosen__arbeitssuchend() -> np.ndarray:
    return np.array([False])


@persona_input_element()
def sozialversicherung__arbeitslosen__mean_nettoeinkommen_in_12_monaten_vor_arbeitslosigkeit_m() -> (
    np.ndarray
):
    return np.array([0])


@persona_input_element()
def sozialversicherung__arbeitslosen__monate_beitragspflichtig_versichert_in_letzten_30_monaten() -> (
    np.ndarray
):
    return np.array([0])


@persona_input_element()
def sozialversicherung__arbeitslosen__monate_durchgängigen_bezugs_von_arbeitslosengeld() -> (
    np.ndarray
):
    return np.array([0])


@persona_input_element()
def sozialversicherung__arbeitslosen__monate_sozialversicherungspflichtiger_beschäftigung_in_letzten_5_jahren() -> (
    np.ndarray
):
    return np.array([0])


@persona_input_element()
def elterngeld__betrag_m() -> np.ndarray:
    return np.array([0])


@persona_input_element()
def kindergeld__in_ausbildung() -> np.ndarray:
    return np.array([False])


@persona_input_element()
def kindergeld__p_id_empfänger() -> np.ndarray:
    return np.array([-1])



@persona_target_element()
def einkommensteuer__betrag_y_sn() -> None:
    return None


@persona_target_element()
def sozialversicherung__pflege__beitrag__betrag_versicherter_y() -> None:
    return None


@persona_target_element()
def sozialversicherung__kranken__beitrag__betrag_versicherter_y() -> None:
    return None


@persona_target_element()
def sozialversicherung__rente__beitrag__betrag_versicherter_y() -> None:
    return None


@persona_target_element()
def sozialversicherung__arbeitslosen__beitrag__betrag_versicherter_y() -> None:
    return None


@persona_target_element()
def sozialversicherung__arbeitslosen__betrag_y() -> None:
    pass


@persona_target_element(start_date="2005-01-01", end_date="2022-12-31")
def arbeitslosengeld_2__betrag_y_bg() -> None:
    pass


@persona_target_element(start_date="2023-01-01")
def bürgergeld__betrag_y_bg() -> None:
    pass


@persona_target_element()
def wohngeld__betrag_y_wthh() -> None:
    pass
