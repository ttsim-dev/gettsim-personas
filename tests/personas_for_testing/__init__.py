from __future__ import annotations

from pathlib import Path

from gettsim_personas.persona_objects import Persona

SamplePersona = Persona(
    path_to_persona_elements=Path(__file__).parent / "persona_elements.py"
)
SamplePersonaWithStartAndEndDate = Persona(
    start_date="2015-01-01",
    path_to_persona_elements=Path(__file__).parent / "persona_specs.py",
    error_if_not_implemented="This Persona is not implemented before 2015.",
)
SamplePersonaWithOverlappingElements = Persona(
    path_to_persona_elements=Path(__file__).parent
    / "persona_elements_with_overlapping_dates.py"
)


__all__ = [
    "SamplePersona",
    "SamplePersonaWithOverlappingElements",
    "SamplePersonaWithStartAndEndDate",
]
