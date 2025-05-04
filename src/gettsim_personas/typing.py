from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Mapping

    GETTSIMScalar = bool | int | float
    RawPersonaSpec = Mapping[str, str | list[GETTSIMScalar]]
