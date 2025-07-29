"""Personas to use as example data when calling GETTSIM."""

from pathlib import Path

from gettsim_personas.active_personas import get_personas, upsert_input_data

__all__ = ["get_personas", "upsert_input_data"]


PERSONAS_SOURCE_DIR = Path(__file__).parent / "personas"
