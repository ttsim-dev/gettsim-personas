from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

import dags.tree as dt
import pandas as pd
import yaml

from gettsim_personas.config import (
    DEFAULT_PERSONA_END_DATE,
    DEFAULT_PERSONA_START_DATE,
    PERSONAS_DIR,
)
from gettsim_personas.persona_objects import Persona

if TYPE_CHECKING:
    from collections.abc import Mapping
    from pathlib import Path
    from typing import TypeVar

    from gettsim_personas.typing import GETTSIMScalar, RawPersonaSpec

    T = TypeVar("T", bound=GETTSIMScalar)


def load_personas() -> list[Persona]:
    """Load all personas from YAML files.

    Returns:
        List of all personas found in YAML files
    """
    personas: list[Persona] = []
    for persona_path in PERSONAS_DIR.rglob("*.yaml"):
        raw_persona_spec = read_persona_yaml(persona_path)
        persona = build_persona_object(raw_persona_spec)
        personas.append(persona)
    return personas


def read_persona_yaml(persona_file: Path) -> RawPersonaSpec:
    with persona_file.open("r", encoding="utf-8") as f:
        persona_spec = yaml.safe_load(f)
    return persona_spec


def build_persona_object(raw_persona_spec: RawPersonaSpec) -> Persona:
    """Build a Persona object from a raw dictionary.

    Args:
        raw_persona_spec: Dictionary containing persona data from YAML file.
            Expected keys: name, description, purpose, policy_inputs,
            policy_inputs_overriding_functions, targets_tree, start_date (optional),
            end_date (optional)

    Returns:
        Persona object with validated data

    Raises:
        ValueError: If dates are invalid or start_date is after end_date
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
        "purpose": raw_persona_spec["purpose"],
        "policy_inputs": convert_lists_to_series(raw_persona_spec["policy_inputs"]),
        "policy_inputs_overriding_functions": convert_lists_to_series(
            raw_persona_spec["policy_inputs_overriding_functions"]
        ),
        "targets_tree": raw_persona_spec["targets_tree"],
        "start_date": start_date,
        "end_date": end_date,
    }

    return Persona(**persona_spec)


def convert_lists_to_series(data: Mapping[str, list[T]]) -> Mapping[str, pd.Series]:
    """Convert leaf nodes to pandas Series.

    Args:
        data: Dictionary to convert

    Returns:
        Dictionary with leaf nodes converted to pandas Series
    """
    flat_data = dt.flatten_to_tree_paths(data)
    for key, value in flat_data.items():
        if isinstance(value, list):
            flat_data[key] = pd.Series(value)
    return dt.unflatten_from_tree_paths(flat_data)
