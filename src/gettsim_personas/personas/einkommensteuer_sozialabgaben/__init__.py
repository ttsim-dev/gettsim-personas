from pathlib import Path

from gettsim_personas.persona_objects import Persona

Couple1Child = Persona(
    path_to_persona_elements=Path(__file__).parent / "_couple_1_child.py",
)


__all__ = ["Couple1Child"]
