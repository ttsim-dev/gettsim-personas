from __future__ import annotations

from ttsim.typing import DashedISOString, NestedData, NestedTargetDict

from _gettsim_personas.persona_elements import (
    PersonaPIDElement,
    TimeDependentPersonaElement,
)

PersonaElement = TimeDependentPersonaElement | PersonaPIDElement

__all__ = [
    "DashedISOString",
    "NestedData",
    "NestedTargetDict",
    "PersonaElement",
]
