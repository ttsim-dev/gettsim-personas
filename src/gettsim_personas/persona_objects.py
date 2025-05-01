from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import dags.tree as dt

if TYPE_CHECKING:
    import datetime

    from ttsim.typing import NestedDataDict, NestedTargetDict


@dataclass(frozen=True)
class Persona:
    name: str
    description: str
    policy_inputs: NestedDataDict
    inputs_to_override_nodes: NestedDataDict
    targets_tree: NestedTargetDict
    start_date: datetime.date
    end_date: datetime.date

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
        """Return names of personas that are active at the collection's date."""
        return [p.name for p in self.active_personas]

    def active_personas(self, date: datetime.date) -> list[Persona]:
        """Return personas that are active at the collection's date."""
        return [p for p in self.personas if p.start_date <= date <= p.end_date]
