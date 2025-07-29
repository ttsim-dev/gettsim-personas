from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal

import dags.tree as dt
import numpy as np

from gettsim_personas.upsert import upsert_input_data

if TYPE_CHECKING:
    import datetime

    from gettsim_personas.typing import NestedData, NestedPersonas, NestedTargetDict


MinMaxVariationThresholds = Literal["min", "max"]


@dataclass(frozen=True)
class VariationBounds:
    """Min and max arrays defining a range of values for input data variation."""

    min: list[float | int]
    max: list[float | int]


@dataclass(frozen=True)
class Persona:
    name: str
    description: str
    input_data_range: dict[str, dict[MinMaxVariationThresholds, list[float | int]]]
    constant_input_data: NestedData
    tt_targets_tree: NestedTargetDict
    start_date: datetime.date
    end_date: datetime.date

    def input_data(self, n_points: int | None = None):
        """Input data for this persona.

        Args:
            n_points: Number of points to generate
        """
        input_data_from_variation_bounds: NestedData = {}
        for path, variation_bounds in self.input_data_range.items():
            input_data_from_variation_bounds[path] = np.linspace(
                variation_bounds.min, variation_bounds.max, n_points
            )

        flat_constant_input_data = dt.flatten_to_tree_paths(self.constant_input_data)
        input_data_from_constant_input_data: NestedData = {}
        for path, value in flat_constant_input_data.items():
            input_data_from_constant_input_data[path] = np.array(value)

        return upsert_input_data(
            input_data=dt.unflatten_from_tree_paths(
                input_data_from_constant_input_data
            ),
            data_to_upsert=dt.unflatten_from_tree_paths(
                input_data_from_variation_bounds
            ),
        )


@dataclass
class ActivePersonaCollection:
    """A collection of personas that are active at a specific date.

    This class provides access to personas that are active at a specific date.
    Personas can be accessed by name as attributes.
    """

    active_personas: NestedPersonas
    date: datetime.date

    def __post_init__(self):
        """Set attributes for each persona after initialization."""
        flat_personas = dt.flatten_to_tree_paths(self.active_personas)

        for path, persona in flat_personas.items():
            self._set_nested_attribute(path, persona)

    def _set_nested_attribute(self, path: tuple[str, ...], value: object) -> None:
        """Recursively set persona by path.

        Creates an intermediate object for each path level and sets the persona at the
        last level. Useful for IDE autocompletion.
        """

        def set_nested_attr(obj, path, value):
            if len(path) == 1:
                setattr(obj, path[0], value)
            else:
                if not hasattr(obj, path[0]):
                    intermediate = type(
                        "PersonaLevel", (), {"_set_nested_attribute": set_nested_attr}
                    )()
                    setattr(obj, path[0], intermediate)
                else:
                    intermediate = getattr(obj, path[0])
                intermediate._set_nested_attribute(path[1:], value)  # noqa: SLF001

        set_nested_attr(self, path, value)

    @property
    def all_names(self) -> list[tuple[str, ...]]:
        """All paths in the active personas collection."""
        return dt.tree_paths(self.active_personas)

    def get_persona(self, path: tuple[str, ...]) -> Persona:
        """Get a persona by its path."""
        flat_active_personas = dt.flatten_to_tree_paths(self.active_personas)
        return flat_active_personas[path]
