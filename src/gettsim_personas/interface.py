"""Public interface for gettsim_personas."""

from datetime import date

from gettsim_personas.load_personas import load_personas
from gettsim_personas.persona_objects import PersonaCollection


def personas_for_date(date_str: str) -> PersonaCollection:
    """Collection of personas that are active at a given date.

    Args:
        date_str: Date in ISO format (YYYY-MM-DD)

    Returns:
        PersonaCollection containing only personas active at the given date
    """
    all_personas = load_personas()
    target_date = date.fromisoformat(date_str)

    active_personas = {
        p.name: p for p in all_personas if p.start_date <= target_date <= p.end_date
    }

    collection = PersonaCollection(personas=active_personas, date=target_date)

    for name, persona in active_personas.items():
        setattr(collection, name, persona)

    return collection
