import datetime

import numpy as np

from _gettsim_personas.persona_elements import (
    persona_description,
    persona_input_element,
    persona_pid_element,
    persona_target_element,
)


@persona_description(
    description=(
        """Persona to compute income taxes and social insurance contributions. Jointly
        taxed married couple with one child. All transfers are set to zero; don't use
        this persona for low- to mid-income households, as they may be eligible for
        (means-tested) transfers."""
    ),
)
def description() -> None:
    pass


@persona_pid_element()
def p_id() -> np.ndarray:
    return np.array([0, 1, 2])


@persona_input_element()
def hh_id() -> np.ndarray:
    return np.array([0, 0, 0])


@persona_input_element()
def alter() -> np.ndarray:
    return np.array([30, 30, 10])


@persona_input_element()
def arbeitsstunden_w() -> np.ndarray:
    return np.array([39, 39, 0])


@persona_input_element()
def behinderungsgrad() -> np.ndarray:
    return np.array([0, 0, 0])


@persona_input_element()
def geburtsjahr(
    evaluation_date: datetime.date,
    alter: np.ndarray,
) -> np.ndarray:
    return evaluation_date.year - alter


@persona_input_element()
def wohnort_ost_hh() -> np.ndarray:
    return np.array([False, False, False])


@persona_input_element()
def einnahmen__bruttolohn_m() -> np.ndarray:
    return np.array([3000, 3000, 0])


@persona_input_element()
def einnahmen__kapitalerträge_y() -> np.ndarray:
    return np.array([500.0, 0.0, 0])


@persona_input_element()
def einkommensteuer__einkünfte__sonstige__rente__betrag_m() -> np.ndarray:
    return np.array([0, 0, 0])


@persona_input_element()
def sozialversicherung__kranken__beitrag__bemessungsgrundlage_rente_m() -> np.ndarray:
    return np.array([0, 0, 0])


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
    return np.array([0.0, 0.0, 100.0])


@persona_input_element()
def einkommensteuer__abzüge__p_id_kinderbetreuungskostenträger() -> np.ndarray:
    return np.array([-1, -1, 0])


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


# Target columns
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
def kindergeld__betrag_y() -> None:
    return None
