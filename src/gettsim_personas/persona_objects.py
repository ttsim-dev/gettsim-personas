from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import dags.tree as dt

if TYPE_CHECKING:
    from ttsim.typing import NestedDataDict, NestedTargetDict


@dataclass(frozen=True)
class Persona:
    name: str
    description: str
    policy_inputs: NestedDataDict
    inputs_to_override_nodes: NestedDataDict
    targets: NestedTargetDict

    @property
    def input_data(self) -> NestedDataDict:
        flat_policy_inputs = dt.flatten_to_qual_names(self.policy_inputs)
        flat_inputs_to_override_nodes = dt.flatten_to_qual_names(
            self.inputs_to_override_nodes
        )
        return dt.unflatten_from_qual_names(
            {**flat_policy_inputs, **flat_inputs_to_override_nodes}
        )


@dataclass
class PersonaCollection:
    personas: list[Persona]

    @property
    def AllNames(self) -> list[str]:  # noqa: N802
        return [p.name for p in self.personas]

    def get_persona(self, name: str) -> Persona:
        return {p.name: p for p in self.personas}[name]
