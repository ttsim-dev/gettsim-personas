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
    """A collection of personas that are active at a specific date.

    This class provides access to personas that are active at a specific date.
    Personas can be accessed by name as attributes.
    """

    personas: dict[str, Persona]
    date: datetime.date

    @property
    def all_names(self) -> list[str]:
        """Return names of all personas in the collection."""
        return list(self.personas.keys())

    def get_persona(self, name: str) -> Persona:
        """Get a persona by name.

        Args:
            name: Name of the persona to retrieve

        Returns:
            The requested persona

        Raises:
            KeyError: If no persona with the given name exists
        """
        return self.personas[name]
