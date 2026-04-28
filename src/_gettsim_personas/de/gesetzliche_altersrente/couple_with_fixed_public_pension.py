import datetime

import numpy as np

from _gettsim_personas.persona_elements import (
    persona_description,
    persona_input_element,
    persona_pid_element,
    persona_target_element,
)


@persona_description(
    description="""Couple retiree receiving statutory pension benefits. Statutory
                pension benefits are fixed. Use this persona to compute income taxes and
                social security contributions.""",
    start_date="2005-01-01",
)
def description() -> None:
    pass


@persona_pid_element()
def p_id() -> np.ndarray:
    return np.array([0, 1])


@persona_input_element()
def hh_id() -> np.ndarray:
    return np.array([0, 0])


@persona_input_element()
def alter() -> np.ndarray:
    return np.array([68, 68])


@persona_input_element()
def arbeitsstunden_w() -> np.ndarray:
    return np.array([0, 0])


@persona_input_element()
def behinderungsgrad() -> np.ndarray:
    return np.array([0, 0])


@persona_input_element()
def geburtsjahr(
    evaluation_date: datetime.date,
    alter: np.ndarray,
) -> np.ndarray:
    return evaluation_date.year - alter


@persona_input_element(end_date="2024-12-31")
def wohnort_ost_hh() -> np.ndarray:
    return np.array([False, False])


@persona_input_element()
def einnahmen__bruttolohn_m() -> np.ndarray:
    return np.array([0, 0])


@persona_input_element()
def einnahmen__kapitalerträge_y() -> np.ndarray:
    return np.array([0, 0])


@persona_input_element()
def einnahmen__renten__aus_berufsständischen_versicherungen_m() -> np.ndarray:
    return np.array([0, 0])


@persona_input_element()
def einnahmen__renten__betriebliche_altersvorsorge_m() -> np.ndarray:
    return np.array([0, 0])


@persona_input_element()
def einnahmen__renten__sonstige_private_vorsorge_m() -> np.ndarray:
    return np.array([0, 0])


@persona_input_element()
def einnahmen__renten__geförderte_private_vorsorge_m() -> np.ndarray:
    return np.array([0, 0])


@persona_input_element(start_date="2005-01-01")
def einnahmen__renten__basisrente_m() -> np.ndarray:
    return np.array([0, 0])


@persona_input_element()
def einkommensteuer__einkünfte__sonstige__rente__alter_beginn_leistungsbezug_sonstige_private_vorsorge() -> (
    np.ndarray
):
    return np.array([65, 65])


@persona_input_element()
def einkommensteuer__einkünfte__ist_hauptberuflich_selbstständig() -> np.ndarray:
    return np.array([False, False])


@persona_input_element()
def einkommensteuer__einkünfte__aus_gewerbebetrieb__betrag_m() -> np.ndarray:
    return np.array([0, 0])


@persona_input_element()
def einkommensteuer__einkünfte__aus_vermietung_und_verpachtung__betrag_m() -> (
    np.ndarray
):
    return np.array([0, 0])


@persona_input_element()
def einkommensteuer__einkünfte__aus_forst_und_landwirtschaft__betrag_m() -> np.ndarray:
    return np.array([0, 0])


@persona_input_element()
def einkommensteuer__einkünfte__aus_selbstständiger_arbeit__betrag_m() -> np.ndarray:
    return np.array([0, 0])


@persona_input_element()
def einkommensteuer__einkünfte__aus_nichtselbstständiger_arbeit__tatsächliche_werbungskosten_y() -> (
    np.ndarray
):
    return np.array([0, 0])


@persona_input_element()
def einkommensteuer__einkünfte__sonstige__alle_weiteren_m() -> np.ndarray:
    return np.array([0, 0])


@persona_input_element()
def einkommensteuer__abzüge__beitrag_private_rentenversicherung_m() -> np.ndarray:
    return np.array([0, 0])


@persona_input_element()
def einkommensteuer__abzüge__kinderbetreuungskosten_m() -> np.ndarray:
    return np.array([0, 0])


@persona_input_element()
def einkommensteuer__abzüge__p_id_kinderbetreuungskostenträger() -> np.ndarray:
    return np.array([-1, -1])


@persona_input_element()
def einkommensteuer__gemeinsam_veranlagt() -> np.ndarray:
    return np.array([True, True])


@persona_input_element()
def sozialversicherung__kranken__beitrag__privat_versichert() -> np.ndarray:
    return np.array([False, False])


@persona_input_element()
def sozialversicherung__pflege__beitrag__hat_kinder() -> np.ndarray:
    return np.array([False, False])


@persona_input_element()
def familie__alleinerziehend() -> np.ndarray:
    return np.array([False, False])


@persona_input_element()
def familie__p_id_ehepartner() -> np.ndarray:
    return np.array([1, 0])


@persona_input_element()
def familie__p_id_elternteil_1() -> np.ndarray:
    return np.array([-1, -1])


@persona_input_element()
def familie__p_id_elternteil_2() -> np.ndarray:
    return np.array([-1, -1])


@persona_input_element()
def kindergeld__in_ausbildung() -> np.ndarray:
    return np.array([False, False])


@persona_input_element()
def kindergeld__p_id_empfänger() -> np.ndarray:
    return np.array([-1, -1])


@persona_input_element()
def sozialversicherung__rente__erwerbsminderung__betrag_m() -> np.ndarray:
    return np.array([0, 0])


@persona_input_element()
def sozialversicherung__rente__altersrente__betrag_m() -> np.ndarray:
    return np.array([2000.0, 2000.0])


@persona_input_element()
def sozialversicherung__rente__jahr_renteneintritt(
    evaluation_date: datetime.date,
) -> np.ndarray:
    return np.array([evaluation_date.year, evaluation_date.year])


@persona_target_element()
def einkommensteuer__betrag_m_sn() -> None:
    pass


@persona_target_element()
def solidaritätszuschlag__betrag_m_sn() -> None:
    pass


@persona_target_element()
def sozialversicherung__beiträge_versicherter_m_hh() -> None:
    pass
