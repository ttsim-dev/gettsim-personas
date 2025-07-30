"""Personas to use as example data when calling GETTSIM."""

from gettsim_personas.persona_objects import _GETTSIMPersonas
from gettsim_personas.upsert import upsert_input_data

GETTSIMPersonas = _GETTSIMPersonas()

__all__ = ["GETTSIMPersonas", "upsert_input_data"]
