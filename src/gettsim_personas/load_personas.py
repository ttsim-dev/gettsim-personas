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
    from pathlib import Path
    from typing import Any


def load_personas() -> list[Persona]:
    """Load all personas from YAML files.

    Returns:
        List of all personas found in YAML files
    """
    personas: list[Persona] = []
    for persona_path in PERSONAS_DIR.glob("*.yaml"):
        raw_persona_dict = read_persona_yaml(persona_path)
        persona = build_persona_object(raw_persona_dict)
        personas.append(persona)
    return personas


def read_persona_yaml(persona_file: Path) -> dict[str, Any]:
    with persona_file.open("r", encoding="utf-8") as f:
        persona_dict = yaml.safe_load(f)
    return persona_dict


def build_persona_object(raw_persona_dict: dict[str, Any]) -> Persona:
    """Build a Persona object from a raw dictionary.

    Args:
        raw_persona_dict: Dictionary containing persona data from YAML file.
            Expected keys: name, description, policy_inputs, inputs_to_override_nodes,
            targets_tree, start_date (optional), end_date (optional)

    Returns:
        Persona object with validated data

    Raises:
        ValueError: If dates are invalid or start_date is after end_date
    """
    start_date = datetime.date.fromisoformat(
        raw_persona_dict.get("start_date", DEFAULT_PERSONA_START_DATE)
    )
    end_date = datetime.date.fromisoformat(
        raw_persona_dict.get("end_date", DEFAULT_PERSONA_END_DATE)
    )

    persona_dict = {
        "name": raw_persona_dict["name"],
        "description": raw_persona_dict["description"],
        "policy_inputs": convert_leaf_to_series(raw_persona_dict["policy_inputs"]),
        "inputs_to_override_nodes": convert_leaf_to_series(
            raw_persona_dict["inputs_to_override_nodes"]
        ),
        "targets_tree": raw_persona_dict["targets_tree"],
        "start_date": start_date,
        "end_date": end_date,
    }

    return Persona(**persona_dict)


def convert_leaf_to_series(data: dict[str, Any]) -> dict[str, Any]:
    """Convert leaf nodes to pandas Series.

    Args:
        data: Dictionary to convert

    Returns:
        Dictionary with leaf nodes converted to pandas Series
    """
    flat_data = dt.flatten_to_qual_names(data)
    for key, value in flat_data.items():
        if isinstance(value, list):
            flat_data[key] = pd.Series(value)
    return dt.unflatten_from_qual_names(flat_data)
