"""Exception hierarchy for gettsim-personas.

Defined inside the private `_gettsim_personas` namespace to avoid an
import cycle: `_gettsim_personas._beartype_conf` needs
`PersonaDefinitionError` while the public `gettsim_personas` package
imports submodules that themselves depend on `_beartype_conf`.

`gettsim_personas.exceptions` re-exports these names so users see them
under the public namespace.
"""

from ttsim.exceptions import TTSIMError


class PersonaDefinitionError(TTSIMError):
    """Raised when a persona definition violates the user-facing contract."""


__all__ = ["PersonaDefinitionError", "TTSIMError"]
