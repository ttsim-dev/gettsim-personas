import datetime

from _gettsim_personas.persona_objects import Persona
from gettsim_personas import (
    einkommensteuer_sozialabgaben,
    grundsicherung_für_erwerbsfähige,
)

ALL_PERSONA_SUBMODULES = [
    einkommensteuer_sozialabgaben,
    grundsicherung_für_erwerbsfähige,
]

START_YEAR = 1950
END_YEAR = datetime.date.today().year  # noqa: DTZ011


def get_all_personas():
    persona_objs = []
    for submodule in ALL_PERSONA_SUBMODULES:
        for name in dir(submodule):
            obj = getattr(submodule, name)
            if isinstance(obj, Persona):
                persona_objs.append(obj)
    return persona_objs


def persona_year_pairs(start=START_YEAR, end=END_YEAR):
    all_personas = get_all_personas()
    return [
        (year, persona)
        for year in range(start, end)
        for persona in all_personas
        if persona.start_date <= datetime.date(year, 1, 1) <= persona.end_date
    ]
