from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import dags.tree as dt

if TYPE_CHECKING:
    import datetime

    from gettsim_personas.typing import NestedDataDict, NestedTargetDict


@dataclass(frozen=True)
class Persona:
    name: str
    description: str
    policy_inputs: NestedDataDict
    policy_inputs_overriding_functions: NestedDataDict
    targets_tree: NestedTargetDict
    start_date: datetime.date
    end_date: datetime.date

    @property
    def input_data(self) -> NestedDataDict:
        flat_policy_inputs = dt.flatten_to_tree_paths(self.policy_inputs)
        flat_policy_inputs_overriding_functions = dt.flatten_to_tree_paths(
            self.policy_inputs_overriding_functions
        )
        return dt.unflatten_from_tree_paths(
            {**flat_policy_inputs, **flat_policy_inputs_overriding_functions}
        )


@dataclass
class PersonaCollection:
    """A collection of personas that are active at a specific date.

    This class provides access to personas that are active at a specific date.
    Personas can be accessed by name as attributes.
    """

    personas: dict[str, Persona]
    date: datetime.date

    def __post_init__(self):
        """Set attributes for each persona after initialization."""
        for name, persona in self.personas.items():
            setattr(self, name, persona)

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
        """
        return self.personas[name]
