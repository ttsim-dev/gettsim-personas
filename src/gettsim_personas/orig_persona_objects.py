from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

import dags.tree as dt
import yaml

from gettsim_personas.config import (
    DEFAULT_PERSONA_END_DATE,
    DEFAULT_PERSONA_START_DATE,
    PERSONAS_SOURCE_DIR,
)
from gettsim_personas.persona_objects import Persona

if TYPE_CHECKING:
    from pathlib import Path
    from typing import TypeVar

    from gettsim_personas.typing import GETTSIMScalar, NestedPersonas, RawPersonaSpec

    T = TypeVar("T", bound=GETTSIMScalar)


def orig_personas() -> NestedPersonas:
    """Load all personas from the YAML files in the personas source directory."""
    orig_personas: NestedPersonas = {}
    for persona_path in PERSONAS_SOURCE_DIR.rglob("*.yaml"):
        orig_path = persona_path.relative_to(PERSONAS_SOURCE_DIR).parts
        raw_persona_spec = read_persona_yaml(persona_path)
        persona = build_persona_object(raw_persona_spec)
        orig_personas[orig_path] = persona
    return dt.unflatten_from_tree_paths(orig_personas)


def read_persona_yaml(persona_file: Path) -> RawPersonaSpec:
    with persona_file.open("r", encoding="utf-8") as f:
        persona_spec = yaml.safe_load(f)
    return persona_spec


def build_persona_object(raw_persona_spec: RawPersonaSpec) -> Persona:
    """Build a Persona object from a raw dictionary.

    Args:
        raw_persona_spec: Dictionary containing persona data from YAML file.
            Expected keys: name, description, varies_by, input_data_tree,
            tt_targets_tree, start_date (optional), end_date (optional)

    Returns:
        Persona object with validated data
    """
    start_date = datetime.date.fromisoformat(
        raw_persona_spec.get("start_date", DEFAULT_PERSONA_START_DATE)
    )
    end_date = datetime.date.fromisoformat(
        raw_persona_spec.get("end_date", DEFAULT_PERSONA_END_DATE)
    )

    persona_spec = {
        "name": raw_persona_spec["name"],
        "description": raw_persona_spec["description"],
        "varies_by": raw_persona_spec["varies_by"],
        "input_data_tree": raw_persona_spec["input_data_tree"],
        "tt_targets_tree": raw_persona_spec["tt_targets_tree"],
        "start_date": start_date,
        "end_date": end_date,
    }

    return Persona(**persona_spec)
