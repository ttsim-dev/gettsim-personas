import datetime

from gettsim_personas import de
from gettsim_personas.persona_objects import Persona

ALL_PERSONA_SUBMODULES = [
    de.einkommensteuer_sozialabgaben,
    de.grundsicherung_für_erwerbsfähige,
]


def get_all_personas():
    persona_objs = []
    for submodule in ALL_PERSONA_SUBMODULES:
        for name in dir(submodule):
            obj = getattr(submodule, name)
            if isinstance(obj, Persona):
                persona_objs.append(obj)
    return persona_objs


def persona_year_pairs(start=2005, end=2025):
    all_personas = get_all_personas()
    return [
        (year, persona)
        for year in range(start, end)
        for persona in all_personas
        if persona.start_date <= datetime.date(year, 1, 1) <= persona.end_date
    ]
