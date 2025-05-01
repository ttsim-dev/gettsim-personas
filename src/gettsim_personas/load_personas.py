from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

import yaml

from gettsim_personas.config import (
    DEFAULT_PERSONA_END_DATE,
    DEFAULT_PERSONA_START_DATE,
    PERSONAS_DIR,
)
from gettsim_personas.persona_objects import Persona, PersonaCollection

if TYPE_CHECKING:
    from pathlib import Path
    from typing import Any


def load_personas() -> PersonaCollection:
    """Load all personas from YAML files and create a collection for the given date.

    Args:
        date: The date for which to create the persona collection

    Returns:
        PersonaCollection containing all personas, filtered by the given date
    """
    personas: list[Persona] = []
    for persona_path in PERSONAS_DIR.glob("*.yaml"):
        raw_persona_dict = read_persona_yaml(persona_path)
        _fail_if_invalid_persona_dict(raw_persona_dict, persona_path=persona_path)
        persona = build_persona_object(
            raw_persona_dict=raw_persona_dict, persona_path=persona_path
        )
        personas.append(persona)
    return PersonaCollection(personas)


def read_persona_yaml(persona_file: Path) -> dict[str, Any]:
    with persona_file.open("r") as f:
        persona_dict = yaml.safe_load(f)
    return persona_dict


def build_persona_object(
    raw_persona_dict: dict[str, Any], persona_path: Path
) -> Persona:
    """Build a Persona object from a raw dictionary.

    Args:
        raw_persona_dict: Dictionary containing persona data from YAML file.
            Expected keys: name, description, policy_inputs, inputs_to_override_nodes,
            targets_tree, start_date (optional), end_date (optional)
        persona_path: Path to the persona file
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
    _fail_if_invalid_date_range(start_date, end_date, persona_path=persona_path)

    persona_dict = {
        "name": raw_persona_dict["name"],
        "description": raw_persona_dict["description"],
        "policy_inputs": raw_persona_dict["policy_inputs"],
        "inputs_to_override_nodes": raw_persona_dict["inputs_to_override_nodes"],
        "targets_tree": raw_persona_dict["targets_tree"],
        "start_date": start_date,
        "end_date": end_date,
    }
    return Persona(**persona_dict)


def _fail_if_invalid_persona_dict(
    persona_dict: dict[str, Any], persona_path: Path
) -> None:
    """Validate the structure and content of a persona dictionary.

    Args:
        persona_dict: Dictionary to validate
        persona_path: Path to the persona file

    Raises:
        TypeError: If input is not a dictionary
        ValueError: If required keys are missing or have invalid types
    """
    required_keys = [
        "name",
        "description",
        "policy_inputs",
        "inputs_to_override_nodes",
        "targets_tree",
    ]
    for key in required_keys:
        if key not in persona_dict:
            msg = f"The file {persona_path} must contain a '{key}' key."
            raise ValueError(msg)


def _fail_if_invalid_date_range(
    start_date: datetime.date, end_date: datetime.date, persona_path: Path
) -> None:
    """Validate the date range of a persona.

    Args:
        start_date: Start date of the persona
        end_date: End date of the persona
        persona_path: Path to the persona file

    Raises:
        ValueError: If start_date is after end_date
    """
    if start_date > end_date:
        msg = f"""
        Invalid date range: start_date ({start_date}) must be before end_date
        ({end_date}) in the file {persona_path}.
        """
        raise ValueError(msg)
