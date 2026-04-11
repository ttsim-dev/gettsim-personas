import datetime
from pathlib import Path

from _gettsim_personas.persona_objects import OrigPersonaOverTime

_START_DATE = datetime.date(2005, 1, 1)
_ERROR = (
    "These personas are available from 2005 because income tax computation is "
    "not implemented in GETTSIM before 2005."
)

Couple = OrigPersonaOverTime(
    path_to_persona_elements=Path(__file__).parent / "couple.py",
    start_date=_START_DATE,
    error_if_not_implemented=_ERROR,
)

Single = OrigPersonaOverTime(
    path_to_persona_elements=Path(__file__).parent / "single.py",
    start_date=_START_DATE,
    error_if_not_implemented=_ERROR,
)

__all__ = ["Couple", "Single"]
