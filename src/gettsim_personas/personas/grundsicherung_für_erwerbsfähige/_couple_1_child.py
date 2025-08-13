import datetime

import numpy as np

from gettsim_personas.persona_objects import (
    PersonaDescription,
    persona_input_element,
    persona_target_element,
)

description = PersonaDescription(
    description="""Persona to compute mean-tested transfers for low-income households.
    Jointly taxed married couple with one child. Income from pensions, parental leave
    benefits and subsistence benefits for the elderly are set to zero.""",
)


@persona_input_element(start_date="2005-01-01")
def p_id() -> np.ndarray:
    return np.array([0, 1, 2])


@persona_input_element(start_date="2005-01-01")
def hh_id() -> np.ndarray:
    return np.array([0, 0, 0])


@persona_input_element(start_date="2005-01-01")
def alter() -> np.ndarray:
    return np.array([30, 30, 6])


@persona_input_element(start_date="2005-01-01")
def alter_monate(alter: np.ndarray) -> np.ndarray:
    return alter * 12


@persona_input_element(start_date="2005-01-01", end_date="2022-12-31")
def arbeitslosengeld_2__p_id_einstandspartner() -> np.ndarray:
    return np.array([1, 0, -1])


@persona_input_element(start_date="2023-01-01")
def bürgergeld__p_id_einstandspartner() -> np.ndarray:
    return np.array([1, 0, -1])


@persona_input_element(start_date="2023-01-01")
def bürgergeld__bezug_im_vorjahr() -> np.ndarray:
    return np.array([False, False, False])


@persona_input_element(start_date="2005-01-01")
def arbeitsstunden_w() -> np.ndarray:
    return np.array([15, 0, 0])


@persona_input_element(start_date="2005-01-01")
def behinderungsgrad() -> np.ndarray:
    return np.array([0, 0, 0])


@persona_input_element(start_date="2005-01-01")
def einkommensteuer__abzüge__beitrag_private_rentenversicherung_m() -> np.ndarray:
    return np.array([0, 0, 0])


@persona_input_element(start_date="2005-01-01")
def einkommensteuer__abzüge__kinderbetreuungskosten_m() -> np.ndarray:
    return np.array([0, 0, 100])


@persona_input_element(start_date="2005-01-01")
def einkommensteuer__abzüge__p_id_kinderbetreuungskostenträger() -> np.ndarray:
    return np.array([-1, -1, 0])


@persona_input_element(start_date="2005-01-01")
def einkommensteuer__einkünfte__aus_forst_und_landwirtschaft__betrag_y() -> np.ndarray:
    return np.array([0, 0, 0])


@persona_input_element(start_date="2005-01-01")
def einkommensteuer__einkünfte__aus_gewerbebetrieb__betrag_y() -> np.ndarray:
    return np.array([0, 0, 0])


@persona_input_element(start_date="2005-01-01")
def einkommensteuer__einkünfte__aus_selbstständiger_arbeit__betrag_y() -> np.ndarray:
    return np.array([0, 0, 0])


@persona_input_element(start_date="2005-01-01")
def einkommensteuer__einkünfte__aus_vermietung_und_verpachtung__betrag_y() -> (
    np.ndarray
):
    return np.array([0, 0, 0])


@persona_input_element(start_date="2005-01-01")
def einkommensteuer__einkünfte__ist_hauptberuflich_selbstständig() -> np.ndarray:
    return np.array([False, False, False])


@persona_input_element(start_date="2005-01-01")
def einkommensteuer__einkünfte__sonstige__alle_weiteren_y() -> np.ndarray:
    return np.array([0, 0, 0])


@persona_input_element(start_date="2005-01-01")
def einkommensteuer__gemeinsam_veranlagt() -> np.ndarray:
    return np.array([True, True, False])


@persona_input_element(start_date="2005-01-01")
def einnahmen__bruttolohn_m() -> np.ndarray:
    return np.array([1000, 0, 0])


@persona_input_element(start_date="2005-01-01")
def einnahmen__kapitalerträge_y() -> np.ndarray:
    return np.array([0.0, 0.0, 0])


@persona_input_element(start_date="2005-01-01")
def einnahmen__renten__gesetzliche_m() -> np.ndarray:
    return np.array([0, 0, 0])


@persona_input_element(start_date="2005-01-01")
def einnahmen__renten__geförderte_private_vorsorge_m() -> np.ndarray:
    return np.array([0, 0, 0])


@persona_input_element(start_date="2005-01-01")
def einnahmen__renten__sonstige_private_vorsorge_m() -> np.ndarray:
    return np.array([0, 0, 0])


@persona_input_element(start_date="2005-01-01")
def einnahmen__renten__betriebliche_altersvorsorge_m() -> np.ndarray:
    return np.array([0, 0, 0])


@persona_input_element(start_date="2005-01-01")
def elterngeld__betrag_m() -> np.ndarray:
    return np.array([0, 0, 0])


@persona_input_element(start_date="2005-01-01")
def familie__alleinerziehend() -> np.ndarray:
    return np.array([False, False, False])


@persona_input_element(start_date="2005-01-01")
def familie__p_id_ehepartner() -> np.ndarray:
    return np.array([1, 0, -1])


@persona_input_element(start_date="2005-01-01")
def familie__p_id_elternteil_1() -> np.ndarray:
    return np.array([-1, -1, 0])


@persona_input_element(start_date="2005-01-01")
def familie__p_id_elternteil_2() -> np.ndarray:
    return np.array([-1, -1, 1])


@persona_input_element(start_date="2005-01-01")
def geburtsjahr(
    evaluation_date: datetime.date,
    alter: np.ndarray,
) -> np.ndarray:
    return evaluation_date.year - alter


@persona_input_element(start_date="2005-01-01")
def kindergeld__in_ausbildung() -> np.ndarray:
    return np.array([False, False, False])


@persona_input_element(start_date="2005-01-01")
def kindergeld__p_id_empfänger() -> np.ndarray:
    return np.array([-1, -1, 0])


@persona_input_element(start_date="2005-01-01")
def sozialversicherung__arbeitslosen__arbeitssuchend() -> np.ndarray:
    return np.array([False, False, False])


@persona_input_element(start_date="2005-01-01")
def sozialversicherung__arbeitslosen__mean_nettoeinkommen_in_12_monaten_vor_arbeitslosigkeit_m() -> (
    np.ndarray
):
    return np.array([0, 0, 0])


@persona_input_element(start_date="2005-01-01")
def sozialversicherung__arbeitslosen__monate_beitragspflichtig_versichert_in_letzten_30_monaten() -> (
    np.ndarray
):
    return np.array([0, 0, 0])


@persona_input_element(start_date="2005-01-01")
def sozialversicherung__arbeitslosen__monate_durchgängigen_bezugs_von_arbeitslosengeld() -> (
    np.ndarray
):
    return np.array([0, 0, 0])


@persona_input_element(start_date="2005-01-01")
def sozialversicherung__arbeitslosen__monate_sozialversicherungspflichtiger_beschäftigung_in_letzten_5_jahren() -> (
    np.ndarray
):
    return np.array([0, 0, 0])


@persona_input_element(start_date="2005-01-01")
def sozialversicherung__kranken__beitrag__privat_versichert() -> np.ndarray:
    return np.array([False, False, False])


@persona_input_element(start_date="2005-01-01")
def sozialversicherung__pflege__beitrag__hat_kinder() -> np.ndarray:
    return np.array([True, True, False])


@persona_input_element(start_date="2005-01-01")
def sozialversicherung__rente__bezieht_rente() -> np.ndarray:
    return np.array([False, False, False])


@persona_input_element(start_date="2005-01-01")
def sozialversicherung__rente__jahr_renteneintritt(
    evaluation_date: datetime.date,
    alter: np.ndarray,
) -> np.ndarray:
    return evaluation_date.year - alter + 65


@persona_input_element(start_date="2005-01-01")
def unterhalt__tatsächlich_erhaltener_betrag_m() -> np.ndarray:
    return np.array([0, 0, 0])


@persona_input_element(start_date="2005-01-01")
def unterhaltsvorschuss__betrag_m() -> np.ndarray:
    return np.array([0, 0, 0])


@persona_input_element(start_date="2005-01-01")
def vermögen() -> np.ndarray:
    return np.array([0, 0, 0])


@persona_input_element(start_date="2005-01-01")
def wohnen__bewohnt_eigentum_hh() -> np.ndarray:
    return np.array([False, False, False])


@persona_input_element(start_date="2005-01-01")
def wohnen__bruttokaltmiete_m_hh() -> np.ndarray:
    return np.array([0, 0, 0])


@persona_input_element(start_date="2005-01-01")
def wohnen__heizkosten_m_hh() -> np.ndarray:
    return np.array([0, 0, 0])


@persona_input_element(start_date="2005-01-01")
def wohnen__wohnfläche_hh() -> np.ndarray:
    return np.array([0, 0, 0])


@persona_input_element(start_date="2005-01-01", end_date="2008-12-31")
def wohnen__baujahr_immobilie_hh() -> np.ndarray:
    return np.array([2000, 2000, 2000])


@persona_input_element(start_date="2005-01-01")
def wohngeld__mietstufe_hh() -> np.ndarray:
    return np.array([5, 5, 5])


@persona_input_element(start_date="2005-01-01", end_date="2024-01-01")
def wohnort_ost_hh() -> np.ndarray:
    return np.array([False, False, False])


@persona_target_element(start_date="2005-01-01")
def einkommensteuer__betrag_m_sn() -> None:
    pass


@persona_target_element(start_date="2005-01-01")
def sozialversicherung__rente__beitrag__betrag_versicherter_y() -> None:
    pass


@persona_target_element(start_date="2005-01-01")
def sozialversicherung__kranken__beitrag__betrag_versicherter_y() -> None:
    pass


@persona_target_element(start_date="2005-01-01")
def sozialversicherung__pflege__beitrag__betrag_versicherter_y() -> None:
    pass


@persona_target_element(start_date="2005-01-01")
def sozialversicherung__arbeitslosen__beitrag__betrag_versicherter_y() -> None:
    pass


@persona_target_element(start_date="2005-01-01")
def sozialversicherung__arbeitslosen__betrag_m() -> None:
    pass


@persona_target_element(start_date="2005-01-01", end_date="2022-12-31")
def arbeitslosengeld_2__betrag_m_bg() -> None:
    pass


@persona_target_element(start_date="2023-01-01")
def bürgergeld__betrag_m_bg() -> None:
    pass


@persona_target_element(start_date="2005-01-01")
def wohngeld__betrag_m_wthh() -> None:
    pass


@persona_target_element(start_date="2005-01-01")
def kinderzuschlag__betrag_m_bg() -> None:
    pass


@persona_target_element(start_date="2005-01-01")
def kindergeld__betrag_m() -> None:
    pass
