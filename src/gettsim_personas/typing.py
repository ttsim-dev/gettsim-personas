from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ttsim.typing import DashedISOString, NestedData, NestedStrings  # noqa: F401


from gettsim_personas.persona_elements import (
    PersonaPIDElement,
    TimeDependentPersonaElement,
)

PersonaElement = TimeDependentPersonaElement | PersonaPIDElement
