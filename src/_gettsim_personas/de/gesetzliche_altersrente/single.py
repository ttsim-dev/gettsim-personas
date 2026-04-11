import datetime

import numpy as np

from _gettsim_personas.persona_elements import (
    persona_description,
    persona_input_element,
    persona_pid_element,
    persona_target_element,
)


@persona_description(
    description="""Persona to compute public pension benefits and income taxes
    for a single adult who receives Altersrente from the statutory pension system.""",
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
    return np.array([70])


@persona_input_element()
def arbeitsstunden_w() -> np.ndarray:
    return np.array([0])


@persona_input_element()
def behinderungsgrad() -> np.ndarray:
    return np.array([0])


@persona_input_element(end_date="2017-12-31")
def weiblich() -> np.ndarray:
    return np.array([False])


@persona_input_element()
def geburtsjahr(
    evaluation_date: datetime.date,
    alter: np.ndarray,
) -> np.ndarray:
    return evaluation_date.year - alter


@persona_input_element()
def geburtsmonat(alter: np.ndarray) -> np.ndarray:
    return np.full(alter.shape, 1, dtype=int)


@persona_input_element(end_date="2024-12-31")
def wohnort_ost_hh() -> np.ndarray:
    return np.array([False])


@persona_input_element()
def einnahmen__bruttolohn_m() -> np.ndarray:
    return np.array([0])


@persona_input_element()
def einnahmen__kapitalerträge_y() -> np.ndarray:
    return np.array([0])


@persona_input_element()
def einnahmen__renten__aus_berufsständischen_versicherungen_m() -> np.ndarray:
    return np.array([0])


@persona_input_element()
def einnahmen__renten__betriebliche_altersvorsorge_m() -> np.ndarray:
    return np.array([0])


@persona_input_element()
def einnahmen__renten__sonstige_private_vorsorge_m() -> np.ndarray:
    return np.array([0])


@persona_input_element()
def einnahmen__renten__geförderte_private_vorsorge_m() -> np.ndarray:
    return np.array([0])


@persona_input_element()
def einkommensteuer__einkünfte__sonstige__rente__alter_beginn_leistungsbezug_sonstige_private_vorsorge() -> (
    np.ndarray
):
    return np.array([65])


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
def einkommensteuer__abzüge__kinderbetreuungskosten_m() -> np.ndarray:
    return np.array([0])


@persona_input_element()
def einkommensteuer__abzüge__p_id_kinderbetreuungskostenträger() -> np.ndarray:
    return np.array([-1])


@persona_input_element()
def einkommensteuer__gemeinsam_veranlagt() -> np.ndarray:
    return np.array([False])


@persona_input_element()
def sozialversicherung__kranken__beitrag__privat_versichert() -> np.ndarray:
    return np.array([False])


@persona_input_element()
def sozialversicherung__pflege__beitrag__hat_kinder() -> np.ndarray:
    return np.array([False])


@persona_input_element()
def familie__alleinerziehend() -> np.ndarray:
    return np.array([False])


@persona_input_element()
def familie__p_id_ehepartner() -> np.ndarray:
    return np.array([-1])


@persona_input_element()
def familie__p_id_elternteil_1() -> np.ndarray:
    return np.array([-1])


@persona_input_element()
def familie__p_id_elternteil_2() -> np.ndarray:
    return np.array([-1])


@persona_input_element()
def kindergeld__in_ausbildung() -> np.ndarray:
    return np.array([False])


@persona_input_element()
def kindergeld__p_id_empfänger() -> np.ndarray:
    return np.array([-1])


@persona_input_element()
def sozialversicherung__rente__bezieht_rente() -> np.ndarray:
    return np.array([True])


@persona_input_element()
def sozialversicherung__rente__erwerbsminderung__voll_erwerbsgemindert() -> np.ndarray:
    return np.array([False])


@persona_input_element()
def sozialversicherung__rente__erwerbsminderung__teilweise_erwerbsgemindert() -> (
    np.ndarray
):
    return np.array([False])


@persona_input_element(end_date="2017-12-31")
def sozialversicherung__rente__altersrente__für_frauen__pflichtsbeitragsjahre_ab_alter_40() -> (
    np.ndarray
):
    return np.array([0.0])


@persona_input_element(end_date="2017-12-31")
def sozialversicherung__rente__altersrente__wegen_arbeitslosigkeit__arbeitslos_für_1_jahr_nach_alter_58_ein_halb() -> (
    np.ndarray
):
    return np.array([False])


@persona_input_element(end_date="2017-12-31")
def sozialversicherung__rente__altersrente__wegen_arbeitslosigkeit__pflichtbeitragsjahre_8_von_10() -> (
    np.ndarray
):
    return np.array([False])


@persona_input_element(end_date="2009-12-31")
def sozialversicherung__rente__altersrente__wegen_arbeitslosigkeit__vertrauensschutz_1997() -> (
    np.ndarray
):
    return np.array([False])


@persona_input_element(end_date="2017-12-31")
def sozialversicherung__rente__altersrente__wegen_arbeitslosigkeit__vertrauensschutz_2004() -> (
    np.ndarray
):
    return np.array([False])


@persona_input_element()
def sozialversicherung__rente__jahr_renteneintritt(
    evaluation_date: datetime.date,
    alter: np.ndarray,
) -> np.ndarray:
    return np.full(alter.shape, evaluation_date.year - 5, dtype=int)


@persona_input_element()
def sozialversicherung__rente__monat_renteneintritt() -> np.ndarray:
    return np.array([1])


@persona_input_element(end_date="2023-06-30")
def sozialversicherung__rente__entgeltpunkte_west() -> np.ndarray:
    return np.array([40.0])


@persona_input_element(end_date="2023-06-30")
def sozialversicherung__rente__entgeltpunkte_ost() -> np.ndarray:
    return np.array([0.0])


@persona_input_element(start_date="2023-07-01")
def sozialversicherung__rente__entgeltpunkte() -> np.ndarray:
    return np.array([40.0])


@persona_input_element()
def sozialversicherung__rente__pflichtbeitragsmonate() -> np.ndarray:
    return np.array([540.0])


@persona_input_element()
def sozialversicherung__rente__freiwillige_beitragsmonate() -> np.ndarray:
    return np.array([0.0])


@persona_input_element()
def sozialversicherung__rente__ersatzzeiten_monate() -> np.ndarray:
    return np.array([0.0])


@persona_input_element()
def sozialversicherung__rente__kinderberücksichtigungszeiten_monate() -> np.ndarray:
    return np.array([0.0])


@persona_input_element()
def sozialversicherung__rente__krankheitszeiten_ab_16_bis_24_monate() -> np.ndarray:
    return np.array([0.0])


@persona_input_element()
def sozialversicherung__rente__monate_geringfügiger_beschäftigung() -> np.ndarray:
    return np.array([0.0])


@persona_input_element()
def sozialversicherung__rente__monate_in_arbeitslosigkeit() -> np.ndarray:
    return np.array([0.0])


@persona_input_element()
def sozialversicherung__rente__monate_in_arbeitsunfähigkeit() -> np.ndarray:
    return np.array([0.0])


@persona_input_element()
def sozialversicherung__rente__monate_in_ausbildungssuche() -> np.ndarray:
    return np.array([0.0])


@persona_input_element()
def sozialversicherung__rente__monate_in_mutterschutz() -> np.ndarray:
    return np.array([0.0])


@persona_input_element()
def sozialversicherung__rente__monate_in_schulausbildung() -> np.ndarray:
    return np.array([0.0])


@persona_input_element()
def sozialversicherung__rente__monate_mit_bezug_entgeltersatzleistungen_wegen_arbeitslosigkeit() -> (
    np.ndarray
):
    return np.array([0.0])


@persona_input_element()
def sozialversicherung__rente__pflegeberücksichtigungszeiten_monate() -> np.ndarray:
    return np.array([0.0])


@persona_input_element(start_date="2018-01-01", end_date="2022-12-31")
def sozialversicherung__rente__altersrente__höchster_bruttolohn_letzte_15_jahre_vor_rente_y() -> (
    np.ndarray
):
    return np.array([50000.0])


@persona_input_element(start_date="2021-01-01")
def sozialversicherung__rente__grundrente__bewertungszeiten_monate() -> np.ndarray:
    return np.array([540])


@persona_input_element(start_date="2021-01-01")
def sozialversicherung__rente__grundrente__grundrentenzeiten_monate() -> np.ndarray:
    return np.array([540])


@persona_input_element(start_date="2021-01-01")
def sozialversicherung__rente__grundrente__mean_entgeltpunkte() -> np.ndarray:
    return np.array([0.8])


@persona_input_element(start_date="2021-01-01")
def sozialversicherung__rente__grundrente__gesamteinnahmen_aus_renten_vorjahr_m() -> (
    np.ndarray
):
    return np.array([0.0])


@persona_input_element(start_date="2021-01-01")
def sozialversicherung__rente__grundrente__bruttolohn_vorjahr_y() -> np.ndarray:
    return np.array([0.0])


@persona_input_element(start_date="2021-01-01")
def sozialversicherung__rente__grundrente__einnahmen_aus_selbstständiger_arbeit_vorvorjahr_y() -> (
    np.ndarray
):
    return np.array([0.0])


@persona_input_element(start_date="2021-01-01")
def sozialversicherung__rente__grundrente__einnahmen_aus_vermietung_und_verpachtung_vorvorjahr_y() -> (
    np.ndarray
):
    return np.array([0.0])


@persona_input_element(start_date="2021-01-01")
def sozialversicherung__rente__grundrente__einnahmen_aus_kapitalvermögen_vorvorjahr_y() -> (
    np.ndarray
):
    return np.array([0.0])


@persona_target_element()
def sozialversicherung__rente__altersrente__betrag_m() -> None:
    pass


@persona_target_element()
def einkommensteuer__betrag_y_sn() -> None:
    pass


@persona_target_element()
def sozialversicherung__kranken__beitrag__betrag_versicherter_y() -> None:
    pass


@persona_target_element()
def sozialversicherung__pflege__beitrag__betrag_versicherter_y() -> None:
    pass
