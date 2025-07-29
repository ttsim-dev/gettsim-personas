"""Get personas and upsert input data."""

from __future__ import annotations

import datetime
import itertools
from typing import TYPE_CHECKING

import dags.tree as dt

from gettsim_personas.orig_personas import orig_personas
from gettsim_personas.persona_objects import ActivePersonaCollection

if TYPE_CHECKING:
    from gettsim_personas.typing import NestedPersonas


def get_personas(date_str: str) -> ActivePersonaCollection:
    """Collection of personas that are active at a given date.

    Args:
        date_str: Date in ISO format (YYYY-MM-DD)

    Returns:
        ActivePersonaCollection containing only personas active at the given date
    """
    date = datetime.date.fromisoformat(date_str)
    all_personas: NestedPersonas = orig_personas()
    _fail_if_multiple_personas_with_same_path_active_at_same_date(all_personas)

    # Build tree of active personas.
    # To do this, we use persona names as last path element instead of file names.
    flat_all_personas = dt.flatten_to_tree_paths(all_personas)
    active_personas: NestedPersonas = {}
    for orig_path, persona in flat_all_personas.items():
        if persona.start_date <= date <= persona.end_date:
            new_path = (*orig_path[:-1], persona.name)
            active_personas[new_path] = persona
    return ActivePersonaCollection(
        active_personas=dt.unflatten_from_tree_paths(active_personas), date=date
    )


def _fail_if_multiple_personas_with_same_path_active_at_same_date(
    all_personas: NestedPersonas,
) -> None:
    """Fail if multiple personas with the same path are active at the same date."""
    persona_path_to_active_periods: dict[
        tuple[str, ...], list[tuple[datetime.date, datetime.date]]
    ] = {}
    flat_all_personas = dt.flatten_to_tree_paths(all_personas)
    for orig_path, persona in flat_all_personas.items():
        persona_path = (*orig_path[:-1], persona.name)
        if persona_path not in persona_path_to_active_periods:
            persona_path_to_active_periods[persona_path] = []
        persona_path_to_active_periods[persona_path].append(
            (persona.start_date, persona.end_date)
        )
    for persona_path, all_active_periods in persona_path_to_active_periods.items():
        if len(all_active_periods) > 1:
            for (start1, end1), (start2, end2) in itertools.combinations(
                all_active_periods, 2
            ):
                if start1 <= end2 and start2 <= end1:
                    msg = (
                        f"Multiple personas with the path '{persona_path}' are active "
                        f"at the same date. Overlapping periods: {start1} - {end1} and "
                        f"{start2} - {end2}."
                    )
                    raise ValueError(msg)
