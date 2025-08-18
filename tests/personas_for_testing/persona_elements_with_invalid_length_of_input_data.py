import numpy as np

from gettsim_personas.persona_elements import (
    persona_description,
    persona_input_element,
    persona_pid_element,
)


@persona_description(
    description=(
        "When called, this persona should throw an error because the input data for "
        "qname 'input_1' has a different length than the p_id array."
    )
)
def description_for_persona_with_invalid_length_of_input_data():
    pass


@persona_pid_element()
def p_id() -> np.ndarray:
    return np.array([0])


@persona_input_element()
def input_1() -> np.ndarray:
    return np.array([1, 2])
