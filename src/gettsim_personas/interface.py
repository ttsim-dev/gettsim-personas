"""Public interface for gettsim_personas."""

from datetime import date

from gettsim_personas.load_personas import load_personas
from gettsim_personas.persona_objects import PersonaCollection


def personas_for_date(date_str: str) -> PersonaCollection:
    """Get personas that are active at a given date.

    Args:
        date_str: Date in ISO format (YYYY-MM-DD)

    Returns:
        PersonaCollection containing only personas active at the given date
    """
    collection = load_personas()
    target_date = date.fromisoformat(date_str)

    for persona in collection.active_personas(target_date):
        setattr(collection, persona.name, persona)

    return collection
