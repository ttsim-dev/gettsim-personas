import os

# Register beartype's package claw before any gettsim_personas submodule
# imports so every module loads with runtime type checks installed via
# INTERNAL_CONF. The internal `_gettsim_personas` namespace is covered
# by a sibling claw. User-facing persona constructors stack an explicit
# `@beartype(conf=PERSONA_CONF)` decorator that maps violations to
# `PersonaDefinitionError` (see `_gettsim_personas._beartype_conf`).
#
# Env-var gated: users of a released package leave
# `GETTSIM_PERSONAS_BEARTYPE_CLAW` unset and never see it. The gate stays
# in place until GEP-09's decision on the rollout lands.
if os.environ.get("GETTSIM_PERSONAS_BEARTYPE_CLAW", "0") != "0":
    from beartype.claw import beartype_package

    from _gettsim_personas._beartype_conf import INTERNAL_CONF

    beartype_package("gettsim_personas", conf=INTERNAL_CONF)
    beartype_package("_gettsim_personas", conf=INTERNAL_CONF)

from gettsim_personas import (
    einkommensteuer_sozialabgaben,
    gesetzliche_altersrente,
    grundsicherung_für_erwerbsfähige,
    grundsicherung_im_alter,
)

__all__ = [
    "einkommensteuer_sozialabgaben",
    "gesetzliche_altersrente",
    "grundsicherung_für_erwerbsfähige",
    "grundsicherung_im_alter",
]
