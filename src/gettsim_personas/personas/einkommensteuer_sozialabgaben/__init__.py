from dataclasses import dataclass
from pathlib import Path

from gettsim_personas.persona_objects import Persona


@dataclass(frozen=True)
class Couple1Child(Persona):
    specs_file: Path = Path(__file__).parent / "_couple_1_child.py"


__all__ = ["Couple1Child"]
