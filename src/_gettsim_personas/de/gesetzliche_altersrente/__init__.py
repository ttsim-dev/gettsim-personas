import datetime
from pathlib import Path

from _gettsim_personas.persona_objects import (
    OrigPersonaOverTime,
    load_persona_elements,
)

_START_DATE = datetime.date(2005, 1, 1)
_ERROR = (
    "These personas are available from 2005 because income tax computation is "
    "not implemented in GETTSIM before 2005."
)

CoupleWithFixedPublicPension = OrigPersonaOverTime(
    elements=load_persona_elements(
        Path(__file__).parent / "couple_with_fixed_public_pension.py"
    ),
    start_date=_START_DATE,
    error_if_not_implemented=_ERROR,
)

SingleWithFixedPublicPension = OrigPersonaOverTime(
    elements=load_persona_elements(
        Path(__file__).parent / "single_with_fixed_public_pension.py"
    ),
    start_date=_START_DATE,
    error_if_not_implemented=_ERROR,
)

__all__ = ["CoupleWithFixedPublicPension", "SingleWithFixedPublicPension"]
