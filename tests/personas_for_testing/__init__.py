from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from gettsim_personas.persona_objects import Persona

if TYPE_CHECKING:
    from gettsim_personas.typing import DashedISOString


@dataclass(frozen=True)
class SamplePersona(Persona):
    path_to_persona_elements: Path = Path(__file__).parent / "persona_elements.py"


@dataclass(frozen=True)
class SamplePersonaWithStartAndEndDate(Persona):
    start_date: DashedISOString = "2015-01-01"
    path_to_persona_elements: Path = Path(__file__).parent / "persona_specs.py"
    error_if_not_implemented: str = "This Persona is not implemented before 2015."


__all__ = ["SamplePersona", "SamplePersonaWithStartAndEndDate"]
