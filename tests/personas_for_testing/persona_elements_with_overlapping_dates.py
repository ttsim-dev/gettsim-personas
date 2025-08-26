import numpy as np

from _gettsim_personas.persona_elements import (
    persona_description,
    persona_input_element,
    persona_pid_element,
)


@persona_description(
    description=(
        "This persona should throw an error if it is called because the active dates "
        "of qnames 'input_1', and 'input_2' overlap."
    )
)
def description_for_persona_with_overlapping_dates():
    pass


@persona_pid_element()
def p_id() -> np.ndarray:
    return np.array([0])


@persona_input_element()
def input_1() -> np.ndarray:
    return np.array([1])


@persona_input_element(start_date="2010-01-01", tt_qname="input_1")
def input_2() -> np.ndarray:
    return np.array([1])
