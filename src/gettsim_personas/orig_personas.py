from __future__ import annotations

import datetime
from pathlib import Path
from typing import TYPE_CHECKING

import dags.tree as dt
import yaml

from gettsim_personas.persona_objects import Persona, VariationBounds

if TYPE_CHECKING:
    from typing import TypeVar

    from gettsim_personas.typing import (
        GETTSIMScalar,
        NestedData,
        NestedPersonas,
        RawPersonaSpec,
    )

    T = TypeVar("T", bound=GETTSIMScalar)


DEFAULT_PERSONA_START_DATE = "1900-01-01"
DEFAULT_PERSONA_END_DATE = "2100-12-31"
PERSONAS_SOURCE_DIR = Path(__file__).parent / "personas"


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
            Expected keys: name, description, input_data_range, constant_input_data,
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

    # Properly format varying input data
    path_to_variation_bounds = _get_path_to_variation_bounds(
        raw_persona_spec["input_data_range"]
    )

    persona_spec = {
        "name": raw_persona_spec["name"],
        "description": raw_persona_spec["description"],
        "input_data_range": path_to_variation_bounds,
        "constant_input_data": raw_persona_spec["constant_input_data"],
        "tt_targets_tree": raw_persona_spec["tt_targets_tree"],
        "start_date": start_date,
        "end_date": end_date,
    }

    return Persona(**persona_spec)


def _get_path_to_variation_bounds(
    spec: NestedData,
) -> dict[tuple[str, ...], VariationBounds]:
    """Get a dictionary mapping paths to variation bounds."""
    flat_spec = dt.flatten_to_tree_paths(spec)
    # Separate path from min/max specifier
    path_to_variation_bounds_spec = {}
    for key, value in flat_spec.items():
        path = key[:-1]
        if path not in path_to_variation_bounds_spec:
            path_to_variation_bounds_spec[path] = {}
        path_to_variation_bounds_spec[path][key[-1]] = value

    # Create variation bounds objects
    path_to_variation_bounds = {}
    for path, variation_bounds_spec in path_to_variation_bounds_spec.items():
        variation_bounds = VariationBounds(
            min=variation_bounds_spec["min"], max=variation_bounds_spec["max"]
        )
        path_to_variation_bounds[path] = variation_bounds
    return path_to_variation_bounds
