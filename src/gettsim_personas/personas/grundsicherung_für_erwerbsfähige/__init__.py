from dataclasses import dataclass
from pathlib import Path

from gettsim_personas.persona_objects import Persona


@dataclass(frozen=True)
class Couple1Child(Persona):
    path_to_persona_elements: Path = Path(__file__).parent / "_couple_1_child.py"
    start_date: str = "2005-01-01"
    error_if_not_implemented: str = (
        "Personas are available from 2005. Basic income support is not implemented in "
        "GETTSIM before 2005."
    )


# This is just for trying out the new interface, it can probably go
@dataclass(frozen=True)
class Couple1ChildInKarenzzeit(Persona):
    path_to_persona_elements: Path = (
        Path(__file__).parent / "_couple_1_child_in_karenzzeit.py"
    )
    start_date: str = "2023-01-01"
    error_if_not_implemented: str = (
        "Karenzzeit for Bürgergeld is not relevant before 2023. Use the "
        "'grundsicherung_für_erwerbsfähige.Couple1Child' persona instead."
    )


__all__ = ["Couple1Child", "Couple1ChildInKarenzzeit"]
