"""`BeartypeConf` instances for gettsim-personas' perimeter and internal claws.

`INTERNAL_CONF` is the default conf for the package-wide claw registered
in `gettsim_personas/__init__.py` and `_gettsim_personas/__init__.py`.
Violations under that claw surface as beartype's own
`BeartypeCallHintViolation`, marking them as internal personas bugs
rather than user error.

`PERSONA_CONF` is used by explicit `@beartype(conf=...)` decorators on
the user-facing persona constructors. It re-raises type violations as
`gettsim_personas.exceptions.PersonaDefinitionError`, preserving a
single documented exception hierarchy at the user boundary.
"""

from ttsim._beartype_conf import INTERNAL_CONF, project_conf

from _gettsim_personas.exceptions import PersonaDefinitionError

PERSONA_CONF = project_conf(PersonaDefinitionError)

__all__ = ["INTERNAL_CONF", "PERSONA_CONF"]
