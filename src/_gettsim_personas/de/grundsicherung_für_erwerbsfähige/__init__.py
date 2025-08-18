import datetime
from pathlib import Path

from _gettsim_personas.persona_objects import Persona

Couple1Child = Persona(
    path_to_persona_elements=Path(__file__).parent / "_couple_1_child.py",
    start_date=datetime.date(2005, 1, 1),
    error_if_not_implemented=(
        "Personas are available from 2005. Basic income support is not implemented in "
        "GETTSIM before 2005."
    ),
)


Couple1ChildInKarenzzeit = Persona(
    path_to_persona_elements=Path(__file__).parent / "_couple_1_child_in_karenzzeit.py",
    start_date=datetime.date(2023, 1, 1),
    error_if_not_implemented=(
        "Karenzzeit for Bürgergeld is not relevant before 2023. Use the "
        "'grundsicherung_für_erwerbsfähige.Couple1Child' persona instead."
    ),
)


__all__ = ["Couple1Child", "Couple1ChildInKarenzzeit"]
