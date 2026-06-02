import os

# GEP 9 (Option A): runtime type checking is on by default. gettsim-personas
# reuses gettsim's switch rather than a dedicated one — set
# `GETTSIM_BEARTYPE_CLAW=0` to opt out. Propagate that opt-out to ttsim before
# any ttsim import, so the perimeter `@beartype(conf=PERSONA_CONF)` decorators
# — whose strategy follows `TTSIM_BEARTYPE_CLAW` — go inert too; an explicit
# `TTSIM_BEARTYPE_CLAW` still wins.
if os.environ.get("GETTSIM_BEARTYPE_CLAW", "1") == "0":
    os.environ.setdefault("TTSIM_BEARTYPE_CLAW", "0")

# Register beartype's package claw before any gettsim_personas submodule
# imports so every module loads with runtime type checks installed via
# INTERNAL_CONF. The internal `_gettsim_personas` namespace is covered
# by a sibling claw. User-facing persona constructors stack an explicit
# `@beartype(conf=PERSONA_CONF)` decorator that maps violations to
# `PersonaDefinitionError` (see `_gettsim_personas._beartype_conf`).
if os.environ.get("GETTSIM_BEARTYPE_CLAW", "1") != "0":
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
