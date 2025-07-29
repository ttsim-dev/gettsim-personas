from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal

import dags.tree as dt

if TYPE_CHECKING:
    import datetime

    from gettsim_personas.typing import NestedDataDict, NestedPersonas, NestedTargetDict


MinMaxVariationThresholds = Literal["min", "max"]


@dataclass(frozen=True)
class Persona:
    name: str
    description: str
    varies_by: dict[str, dict[MinMaxVariationThresholds, list[float | int]]]
    input_data_tree: NestedDataDict
    tt_targets_tree: NestedTargetDict
    start_date: datetime.date
    end_date: datetime.date


@dataclass(frozen=True)
class PersonaSpec(Persona):
    varies_by: dict[str, dict[MinMaxVariationThresholds, list[float | int]]]


@dataclass
class ActivePersonaCollection:
    """A collection of personas that are active at a specific date.

    This class provides access to personas that are active at a specific date.
    Personas can be accessed by name as attributes.
    """

    nested_personas: NestedPersonas
    date: datetime.date

    def __post_init__(self):
        """Set attributes for each persona after initialization."""
        flat_personas = dt.flatten_to_tree_paths(self.nested_personas)

        for path, persona in flat_personas.items():
            self._set_nested_attribute(path, persona)

    def _set_nested_attribute(self, path: tuple[str, ...], value: object) -> None:
        """Recursively set nested attributes for a path."""
        if len(path) == 1:
            setattr(self, path[0], value)
        else:
            if not hasattr(self, path[0]):
                intermediate = type("PersonaLevel", (), {})()
                setattr(self, path[0], intermediate)
            else:
                intermediate = getattr(self, path[0])

            intermediate._set_nested_attribute(path[1:], value)

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
