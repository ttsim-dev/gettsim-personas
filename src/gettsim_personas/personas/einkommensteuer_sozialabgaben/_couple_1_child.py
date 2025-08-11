import datetime

import numpy as np

from gettsim_personas.persona_objects import (
    PersonaDescription,
    input_column,
    target_column,
)

description = PersonaDescription(
    description=(
        """Persona to compute income taxes and social insurance contributions. Jointly
        taxed married couple with one child. All transfers are set to zero; don't use
        this persona for low- to mid-income households, as they may be eligible for
        (means-tested) transfers."""
    ),
)


@input_column()
def alter() -> np.ndarray:
    return np.array([30, 30, 10])


@input_column()
def arbeitsstunden_w() -> np.ndarray:
    return np.array([39, 39, 0])


@input_column()
def behinderungsgrad() -> np.ndarray:
    return np.array([0, 0, 0])


@input_column()
def geburtsjahr(
    evaluation_date: datetime.date,
    alter: np.ndarray,
) -> np.ndarray:
    return evaluation_date.year - alter


@input_column()
def p_id() -> np.ndarray:
    return np.array([0, 1, 2])


@input_column()
def wohnort_ost_hh() -> np.ndarray:
    return np.array([False, False, False])


@input_column()
def einnahmen__bruttolohn_m() -> np.ndarray:
    return np.array([3000, 3000, 0])


@input_column()
def einnahmen__kapitalerträge_y() -> np.ndarray:
    return np.array([500.0, 0.0, 0])


@input_column()
def einnahmen__renten__gesetzliche_m() -> np.ndarray:
    return np.array([0, 0, 0])


@input_column()
def einnahmen__renten__geförderte_private_vorsorge_m() -> np.ndarray:
    return np.array([0, 0, 0])


@input_column()
def einnahmen__renten__sonstige_private_vorsorge_m() -> np.ndarray:
    return np.array([0, 0, 0])


@input_column()
def einnahmen__renten__betriebliche_altersvorsorge_m() -> np.ndarray:
    return np.array([0, 0, 0])


@input_column()
def einkommensteuer__einkünfte__ist_hauptberuflich_selbstständig() -> np.ndarray:
    return np.array([False, False, False])


@input_column()
def einkommensteuer__einkünfte__aus_gewerbebetrieb__betrag_m() -> np.ndarray:
    return np.array([0, 0, 0])


@input_column()
def einkommensteuer__einkünfte__aus_vermietung_und_verpachtung__betrag_m() -> (
    np.ndarray
):
    return np.array([0, 0, 0])


@input_column()
def einkommensteuer__einkünfte__aus_forst_und_landwirtschaft__betrag_m() -> np.ndarray:
    return np.array([0, 0, 0])


@input_column()
def einkommensteuer__einkünfte__aus_selbstständiger_arbeit__betrag_m() -> np.ndarray:
    return np.array([0, 0, 0])


@input_column()
def einkommensteuer__einkünfte__sonstige__alle_weiteren_m() -> np.ndarray:
    return np.array([0, 0, 0])


@input_column()
def einkommensteuer__abzüge__beitrag_private_rentenversicherung_m() -> np.ndarray:
    return np.array([0, 0, 0])


@input_column()
def einkommensteuer__abzüge__kinderbetreuungskosten_m() -> np.ndarray:
    return np.array([0.0, 0.0, 100.0])


@input_column()
def einkommensteuer__abzüge__p_id_kinderbetreuungskostenträger() -> np.ndarray:
    return np.array([-1, -1, 0])


@input_column()
def einkommensteuer__gemeinsam_veranlagt() -> np.ndarray:
    return np.array([True, True, False])


@input_column()
def sozialversicherung__rente__jahr_renteneintritt(
    evaluation_date: datetime.date,
    alter: np.ndarray,
) -> np.ndarray:
    return evaluation_date.year - alter + 65


@input_column()
def sozialversicherung__kranken__beitrag__privat_versichert() -> np.ndarray:
    return np.array([False, False, False])


@input_column()
def sozialversicherung__pflege__beitrag__hat_kinder() -> np.ndarray:
    return np.array([True, True, False])


@input_column()
def familie__alleinerziehend() -> np.ndarray:
    return np.array([False, False, False])


@input_column()
def familie__p_id_ehepartner() -> np.ndarray:
    return np.array([1, 0, -1])


@input_column()
def familie__p_id_elternteil_1() -> np.ndarray:
    return np.array([-1, -1, 0])


@input_column()
def familie__p_id_elternteil_2() -> np.ndarray:
    return np.array([-1, -1, 1])


@input_column()
def kindergeld__in_ausbildung() -> np.ndarray:
    return np.array([False, False, False])


@input_column()
def kindergeld__p_id_empfänger() -> np.ndarray:
    return np.array([-1, -1, 0])


# Target columns
@target_column()
def einkommensteuer__betrag_y_sn() -> None:
    return None


@target_column()
def sozialversicherung__pflege__beitrag__betrag_versicherter_y() -> None:
    return None


@target_column()
def sozialversicherung__kranken__beitrag__betrag_versicherter_y() -> None:
    return None


@target_column()
def sozialversicherung__rente__beitrag__betrag_versicherter_y() -> None:
    return None


@target_column()
def sozialversicherung__arbeitslosen__beitrag__betrag_versicherter_y() -> None:
    return None
