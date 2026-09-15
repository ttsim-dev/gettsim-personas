from __future__ import annotations

import datetime
from pathlib import Path

from _gettsim_personas.persona_objects import (
    OrigPersonaOverTime,
    load_persona_elements,
)

SamplePersona = OrigPersonaOverTime(
    elements=load_persona_elements(Path(__file__).parent / "persona_elements.py")
)
SamplePersonaWithStartAndEndDate = OrigPersonaOverTime(
    start_date=datetime.date(2015, 1, 1),
    elements=load_persona_elements(Path(__file__).parent / "persona_elements.py"),
    error_if_not_implemented="This Persona is not implemented before 2015.",
)
SamplePersonaWithOverlappingElements = OrigPersonaOverTime(
    elements=load_persona_elements(
        Path(__file__).parent / "persona_elements_with_overlapping_dates.py"
    )
)
SamplePersonaWithInvalidLengthOfInputData = OrigPersonaOverTime(
    elements=load_persona_elements(
        Path(__file__).parent / "persona_elements_with_invalid_length_of_input_data.py"
    )
)


__all__ = [
    "SamplePersona",
    "SamplePersonaWithOverlappingElements",
    "SamplePersonaWithStartAndEndDate",
]
