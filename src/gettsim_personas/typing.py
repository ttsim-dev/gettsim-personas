from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Mapping

    from dags.tree.typing import NestedTargetDict  # noqa: F401
    from ttsim.typing import NestedDataDict  # noqa: F401

    from gettsim_personas.persona_objects import (  # noqa: F401
        Persona,
        PersonaCollection,
    )

    GETTSIMScalar = bool | int | float
    RawPersonaSpec = Mapping[str, str | list[GETTSIMScalar]]
