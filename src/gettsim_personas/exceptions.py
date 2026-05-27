"""Exception hierarchy for `gettsim_personas`.

User-facing errors raised by persona machinery inherit from
`ttsim.exceptions.TTSIMError` so callers can catch any GETTSIM-ecosystem
failure with a single `except TTSIMError`. Beartype runtime type-check
violations on persona constructors are re-raised as
`PersonaDefinitionError` via `violation_door_type` in
`_gettsim_personas._beartype_conf`.

Re-exports definitions from the private `_gettsim_personas.exceptions`
module; the split avoids an import cycle between the package claw and
the per-component conf.
"""

from _gettsim_personas.exceptions import PersonaDefinitionError, TTSIMError

__all__ = ["PersonaDefinitionError", "TTSIMError"]
