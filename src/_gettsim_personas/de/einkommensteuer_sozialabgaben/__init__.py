import datetime
from pathlib import Path

from _gettsim_personas.persona_objects import Persona

Couple1Child = Persona(
    path_to_persona_elements=Path(__file__).parent / "couple_1_child.py",
    start_date=datetime.date(2005, 1, 1),
    error_if_not_implemented="""
        Currently, GETTSIM does not support the calculation of income taxes before 2005.
    """,
)


__all__ = ["Couple1Child"]
