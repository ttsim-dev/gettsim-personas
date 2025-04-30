from __future__ import annotations

from typing import TYPE_CHECKING

import yaml

from gettsim_personas.config import PERSONAS_DIR
from gettsim_personas.persona_objects import Persona, PersonaCollection

if TYPE_CHECKING:
    from pathlib import Path
    from typing import Any


def load_personas() -> PersonaCollection:
    personas: list[Persona] = []
    for persona_file in PERSONAS_DIR.glob("*.yaml"):
        persona_dict = read_persona_yaml(persona_file)
        _fail_if_invalid_persona_dict(persona_dict)
        persona = Persona(**persona_dict)
        personas.append(persona)
    return PersonaCollection(personas)


def read_persona_yaml(persona_file: Path) -> dict[str, Any]:
    with persona_file.open("r") as f:
        persona_dict = yaml.safe_load(f)
    return persona_dict


def _fail_if_invalid_persona_dict(persona_dict: dict[str, Any]) -> None:
    if not isinstance(persona_dict, dict):
        msg = "Persona dict must be a dictionary."
        raise TypeError(msg)
    required_keys = [
        "name",
        "description",
        "policy_inputs",
        "inputs_to_override_nodes",
        "targets",
    ]
    for key in required_keys:
        if key not in persona_dict:
            msg = f"Persona dict must contain a '{key}' key."
            raise ValueError(msg)
