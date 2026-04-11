import datetime

import numpy as np

from _gettsim_personas.persona_elements import (
    persona_description,
    persona_input_element,
    persona_pid_element,
    persona_target_element,
)


@persona_description(
    description="""Persona to compute Grundsicherung im Alter, Wohngeld, public
    pension benefits, and income taxes for a jointly-taxed married couple with one an
    adult child in a different household. Both partners receive Altersrente from the
    statutory pension system.""",
    start_date="2011-01-01",
)
def description() -> None:
    pass


@persona_pid_element()
def p_id() -> np.ndarray:
    return np.array([0, 1, 2])


@persona_input_element()
def hh_id() -> np.ndarray:
    return np.array([0, 0, 1])


@persona_input_element()
def alter() -> np.ndarray:
    return np.array([72, 70, 40])


@persona_input_element()
def arbeitsstunden_w() -> np.ndarray:
    return np.array([0, 0, 30])


@persona_input_element()
def behinderungsgrad() -> np.ndarray:
    return np.array([0, 0, 0])


@persona_input_element()
def schwerbehindert_grad_g() -> np.ndarray:
    return np.array([False, False, False])


@persona_input_element()
def alter_monate(alter: np.ndarray) -> np.ndarray:
    return alter * 12


@persona_input_element(end_date="2017-12-31")
def weiblich() -> np.ndarray:
    return np.array([False, True, False])


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
    return np.array([False, False, False])


@persona_input_element()
def einnahmen__bruttolohn_m() -> np.ndarray:
    return np.array([0, 0, 4_000])


@persona_input_element()
def einnahmen__kapitalerträge_y() -> np.ndarray:
    return np.array([0, 0, 0])


@persona_input_element()
def einnahmen__renten__aus_berufsständischen_versicherungen_m() -> np.ndarray:
    return np.array([0, 0, 0])


@persona_input_element()
def einnahmen__renten__betriebliche_altersvorsorge_m() -> np.ndarray:
    return np.array([0, 0, 0])


@persona_input_element()
def einnahmen__renten__sonstige_private_vorsorge_m() -> np.ndarray:
    return np.array([0, 0, 0])


@persona_input_element()
def einnahmen__renten__geförderte_private_vorsorge_m() -> np.ndarray:
    return np.array([0, 0, 0])


@persona_input_element()
def einkommensteuer__einkünfte__sonstige__rente__alter_beginn_leistungsbezug_sonstige_private_vorsorge() -> (
    np.ndarray
):
    return np.array([65, 65, 65])


@persona_input_element()
def einkommensteuer__einkünfte__ist_hauptberuflich_selbstständig() -> np.ndarray:
    return np.array([False, False, False])


@persona_input_element()
def einkommensteuer__einkünfte__aus_gewerbebetrieb__betrag_m() -> np.ndarray:
    return np.array([0, 0, 0])


@persona_input_element()
def einkommensteuer__einkünfte__aus_vermietung_und_verpachtung__betrag_m() -> (
    np.ndarray
):
    return np.array([0, 0, 0])


@persona_input_element()
def einkommensteuer__einkünfte__aus_forst_und_landwirtschaft__betrag_m() -> np.ndarray:
    return np.array([0, 0, 0])


@persona_input_element()
def einkommensteuer__einkünfte__aus_selbstständiger_arbeit__betrag_m() -> np.ndarray:
    return np.array([0, 0, 0])


@persona_input_element()
def einkommensteuer__einkünfte__sonstige__alle_weiteren_m() -> np.ndarray:
    return np.array([0, 0, 0])


@persona_input_element()
def einkommensteuer__abzüge__beitrag_private_rentenversicherung_m() -> np.ndarray:
    return np.array([0, 0, 0])


@persona_input_element()
def einkommensteuer__abzüge__kinderbetreuungskosten_m() -> np.ndarray:
    return np.array([0, 0, 0])


@persona_input_element()
def einkommensteuer__abzüge__p_id_kinderbetreuungskostenträger() -> np.ndarray:
    return np.array([-1, -1, -1])


@persona_input_element()
def einkommensteuer__gemeinsam_veranlagt() -> np.ndarray:
    return np.array([True, True, False])


@persona_input_element()
def sozialversicherung__kranken__beitrag__privat_versichert() -> np.ndarray:
    return np.array([False, False, False])


@persona_input_element()
def sozialversicherung__pflege__beitrag__hat_kinder() -> np.ndarray:
    return np.array([True, True, False])


@persona_input_element()
def familie__alleinerziehend() -> np.ndarray:
    return np.array([False, False, False])


@persona_input_element()
def familie__p_id_ehepartner() -> np.ndarray:
    return np.array([1, 0, -1])


@persona_input_element()
def familie__p_id_elternteil_1() -> np.ndarray:
    return np.array([-1, -1, 0])


@persona_input_element()
def familie__p_id_elternteil_2() -> np.ndarray:
    return np.array([-1, -1, 1])


@persona_input_element()
def kindergeld__in_ausbildung() -> np.ndarray:
    return np.array([False, False, False])


@persona_input_element()
def kindergeld__p_id_empfänger() -> np.ndarray:
    return np.array([-1, -1, 0])


@persona_input_element()
def sozialversicherung__rente__bezieht_rente() -> np.ndarray:
    return np.array([True, True, False])


@persona_input_element()
def sozialversicherung__rente__erwerbsminderung__betrag_m() -> np.ndarray:
    return np.array([0, 0, 0])


@persona_input_element(end_date="2017-12-31")
def sozialversicherung__rente__altersrente__für_frauen__pflichtsbeitragsjahre_ab_alter_40() -> (
    np.ndarray
):
    return np.array([0, 0, 0])


@persona_input_element(end_date="2017-12-31")
def sozialversicherung__rente__altersrente__wegen_arbeitslosigkeit__arbeitslos_für_1_jahr_nach_alter_58_ein_halb() -> (
    np.ndarray
):
    return np.array([False, False, False])


@persona_input_element(end_date="2017-12-31")
def sozialversicherung__rente__altersrente__wegen_arbeitslosigkeit__pflichtbeitragsjahre_8_von_10() -> (
    np.ndarray
):
    return np.array([False, False, False])


@persona_input_element(end_date="2017-12-31")
def sozialversicherung__rente__altersrente__wegen_arbeitslosigkeit__vertrauensschutz_2004() -> (
    np.ndarray
):
    return np.array([False, False, False])


@persona_input_element()
def sozialversicherung__rente__jahr_renteneintritt(
    evaluation_date: datetime.date,
    alter: np.ndarray,
) -> np.ndarray:
    return np.full(alter.shape, evaluation_date.year - 3, dtype=int)


@persona_input_element()
def sozialversicherung__rente__monat_renteneintritt() -> np.ndarray:
    return np.array([1, 1, 1])


@persona_input_element(end_date="2023-06-30")
def sozialversicherung__rente__entgeltpunkte_west() -> np.ndarray:
    return np.array([15.0, 4.0, 0.0])


@persona_input_element(end_date="2023-06-30")
def sozialversicherung__rente__entgeltpunkte_ost() -> np.ndarray:
    return np.array([0, 0, 0])


@persona_input_element(start_date="2023-07-01")
def sozialversicherung__rente__entgeltpunkte() -> np.ndarray:
    return np.array([15.0, 4.0, 0.0])


@persona_input_element()
def sozialversicherung__rente__pflichtbeitragsmonate() -> np.ndarray:
    return np.array([360.0, 80.0, 0.0])


@persona_input_element()
def sozialversicherung__rente__freiwillige_beitragsmonate() -> np.ndarray:
    return np.array([0.0, 0.0, 0.0])


@persona_input_element()
def sozialversicherung__rente__ersatzzeiten_monate() -> np.ndarray:
    return np.array([0.0, 0.0, 0.0])


@persona_input_element()
def sozialversicherung__rente__kinderberücksichtigungszeiten_monate() -> np.ndarray:
    return np.array([0.0, 0.0, 0.0])


@persona_input_element()
def sozialversicherung__rente__krankheitszeiten_ab_16_bis_24_monate() -> np.ndarray:
    return np.array([0.0, 0.0, 0.0])


@persona_input_element()
def sozialversicherung__rente__monate_geringfügiger_beschäftigung() -> np.ndarray:
    return np.array([0.0, 0.0, 0.0])


@persona_input_element()
def sozialversicherung__rente__monate_in_arbeitslosigkeit() -> np.ndarray:
    return np.array([0.0, 0.0, 0.0])


@persona_input_element()
def sozialversicherung__rente__monate_in_arbeitsunfähigkeit() -> np.ndarray:
    return np.array([0.0, 0.0, 0.0])


@persona_input_element()
def sozialversicherung__rente__monate_in_ausbildungssuche() -> np.ndarray:
    return np.array([0.0, 0.0, 0.0])


@persona_input_element()
def sozialversicherung__rente__monate_in_mutterschutz() -> np.ndarray:
    return np.array([0.0, 0.0, 0.0])


@persona_input_element()
def sozialversicherung__rente__monate_in_schulausbildung() -> np.ndarray:
    return np.array([0.0, 0.0, 0.0])


@persona_input_element()
def sozialversicherung__rente__monate_mit_bezug_entgeltersatzleistungen_wegen_arbeitslosigkeit() -> (
    np.ndarray
):
    return np.array([0.0, 0.0, 0.0])


@persona_input_element()
def sozialversicherung__rente__pflegeberücksichtigungszeiten_monate() -> np.ndarray:
    return np.array([0.0, 0.0, 0.0])


@persona_input_element(start_date="2018-01-01", end_date="2022-12-31")
def sozialversicherung__rente__altersrente__höchster_bruttolohn_letzte_15_jahre_vor_rente_y() -> (
    np.ndarray
):
    return np.array([22_000.0, 0.0, 0.0])


@persona_input_element(start_date="2021-01-01")
def sozialversicherung__rente__grundrente__bewertungszeiten_monate() -> np.ndarray:
    return np.array([360, 80, 0])


@persona_input_element(start_date="2021-01-01")
def sozialversicherung__rente__grundrente__grundrentenzeiten_monate() -> np.ndarray:
    return np.array([360, 80, 0])


@persona_input_element(start_date="2021-01-01")
def sozialversicherung__rente__grundrente__mean_entgeltpunkte() -> np.ndarray:
    return np.array([0.5, 0.2, 0.0])


@persona_input_element(start_date="2021-01-01")
def sozialversicherung__rente__grundrente__gesamteinnahmen_aus_renten_vorjahr_m() -> (
    np.ndarray
):
    return np.array([0.0, 0.0, 0.0])


@persona_input_element(start_date="2021-01-01")
def sozialversicherung__rente__grundrente__bruttolohn_vorjahr_y() -> np.ndarray:
    return np.array([0.0, 0.0, 0.0])


@persona_input_element(start_date="2021-01-01")
def sozialversicherung__rente__grundrente__einnahmen_aus_selbstständiger_arbeit_vorvorjahr_y() -> (
    np.ndarray
):
    return np.array([0.0, 0.0, 0.0])


@persona_input_element(start_date="2021-01-01")
def sozialversicherung__rente__grundrente__einnahmen_aus_vermietung_und_verpachtung_vorvorjahr_y() -> (
    np.ndarray
):
    return np.array([0.0, 0.0, 0.0])


@persona_input_element(start_date="2021-01-01")
def sozialversicherung__rente__grundrente__einnahmen_aus_kapitalvermögen_vorvorjahr_y() -> (
    np.ndarray
):
    return np.array([0.0, 0.0, 0.0])


@persona_input_element()
def wohnen__bewohnt_eigentum_hh() -> np.ndarray:
    return np.array([False, False, False])


@persona_input_element()
def wohnen__bruttokaltmiete_m_hh() -> np.ndarray:
    return np.array([650, 650, 400])


@persona_input_element()
def wohnen__heizkosten_m_hh() -> np.ndarray:
    return np.array([60, 60, 55])


@persona_input_element()
def wohnen__wohnfläche_hh() -> np.ndarray:
    return np.array([75, 75, 40])


@persona_input_element()
def wohngeld__mietstufe_hh() -> np.ndarray:
    return np.array([3, 3, 4])


@persona_input_element()
def vermögen() -> np.ndarray:
    return np.array([0, 0, 0])


@persona_input_element()
def unterhalt__tatsächlich_erhaltener_betrag_m() -> np.ndarray:
    return np.array([0, 0, 0])


@persona_input_element()
def unterhaltsvorschuss__betrag_m() -> np.ndarray:
    return np.array([0, 0, 0])


@persona_input_element()
def elterngeld__betrag_m() -> np.ndarray:
    return np.array([0, 0, 0])


@persona_input_element(end_date="2022-12-31")
def arbeitslosengeld_2__p_id_einstandspartner() -> np.ndarray:
    return np.array([1, 0, -1])


@persona_input_element(start_date="2023-01-01")
def bürgergeld__p_id_einstandspartner() -> np.ndarray:
    return np.array([1, 0, -1])


@persona_input_element(start_date="2023-01-01")
def bürgergeld__bezug_im_vorjahr() -> np.ndarray:
    return np.array([False, False, False])


@persona_input_element()
def kindergeld__betrag_m() -> np.ndarray:
    return np.array([0, 0, 0])


@persona_input_element()
def sozialversicherung__arbeitslosen__betrag_m() -> np.ndarray:
    return np.array([0, 0, 0])


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


@persona_target_element()
def grundsicherung__im_alter__betrag_m_eg() -> None:
    pass


@persona_target_element()
def wohngeld__betrag_m_wthh() -> None:
    pass
