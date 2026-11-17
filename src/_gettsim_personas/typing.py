from __future__ import annotations

from ttsim.typing import DashedISOString, NestedData, NestedTargetDict

from _gettsim_personas.persona_elements import (
    PersonaDescription,
    PersonaInputElement,
    PersonaPIDElement,
    PersonaTargetElement,
)

PersonaElement = (
    PersonaInputElement | PersonaTargetElement | PersonaDescription | PersonaPIDElement
)

__all__ = [
    "DashedISOString",
    "NestedData",
    "NestedTargetDict",
    "PersonaElement",
]
