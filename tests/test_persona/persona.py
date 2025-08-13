from dataclasses import dataclass
from pathlib import Path

from gettsim_personas.persona_objects import Persona
from gettsim_personas.typing import DashedISOString


@dataclass(frozen=True)
class TestPerona(Persona):
    specs_file: Path = Path(__file__).parent / "persona_specs.py"


@dataclass(frozen=True)
class TestPersonaWithStartAndEndDate(Persona):
    start_date: DashedISOString = "2015-01-01"
    specs_file: Path = Path(__file__).parent / "persona_specs.py"
    error_if_not_implemented: str = "This Persona is not implemented before 2015."
