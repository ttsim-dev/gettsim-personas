import datetime
from pathlib import Path

from _gettsim_personas.persona_objects import OrigPersonaOverTime

_START_DATE = datetime.date(2011, 1, 1)
_ERROR = (
    "These personas are available from 2011 because several Grundsicherung im Alter "
    "policy functions in GETTSIM start only in 2011."
)

Couple1Child = OrigPersonaOverTime(
    path_to_persona_elements=Path(__file__).parent / "couple_1_child.py",
    start_date=_START_DATE,
    error_if_not_implemented=_ERROR,
)

CoupleNoChild = OrigPersonaOverTime(
    path_to_persona_elements=Path(__file__).parent / "couple_no_child.py",
    start_date=_START_DATE,
    error_if_not_implemented=_ERROR,
)

Single1Child = OrigPersonaOverTime(
    path_to_persona_elements=Path(__file__).parent / "single_1_child.py",
    start_date=_START_DATE,
    error_if_not_implemented=_ERROR,
)

SingleNoChild = OrigPersonaOverTime(
    path_to_persona_elements=Path(__file__).parent / "single_no_child.py",
    start_date=_START_DATE,
    error_if_not_implemented=_ERROR,
)

__all__ = [
    "Couple1Child",
    "CoupleNoChild",
    "Single1Child",
    "SingleNoChild",
]
