import datetime
from pathlib import Path

from _gettsim_personas.persona_objects import OrigPersonaOverTime

Couple1Child = OrigPersonaOverTime(
    path_to_persona_elements=Path(__file__).parent / "couple_1_child.py",
    start_date=datetime.date(2005, 1, 1),
    error_if_not_implemented=(
        "These personas are available from 2005 because basic income support is not "
        "implemented in GETTSIM before 2005."
    ),
)


Couple1ChildInKarenzzeit = OrigPersonaOverTime(
    path_to_persona_elements=Path(__file__).parent / "couple_1_child_in_karenzzeit.py",
    start_date=datetime.date(2023, 1, 1),
    error_if_not_implemented=(
        "Karenzzeit for Bürgergeld is not relevant before 2023. Use the "
        "'grundsicherung_für_erwerbsfähige.Couple1Child' persona instead."
    ),
)

SingleAdult = OrigPersonaOverTime(
    path_to_persona_elements=Path(__file__).parent / "single.py",
    start_date=datetime.date(2005, 1, 1),
    error_if_not_implemented=(
        "These personas are available from 2005 because basic income support is not "
        "implemented in GETTSIM before 2005."
    ),
)

__all__ = ["Couple1Child", "Couple1ChildInKarenzzeit", "single"]
