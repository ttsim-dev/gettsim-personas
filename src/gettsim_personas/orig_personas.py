from __future__ import annotations

import importlib.util
import inspect
import sys
from pathlib import Path
from typing import TYPE_CHECKING

from gettsim_personas.persona_objects import (
    Persona,
    PersonaCollection,
    PersonaNotImplementedError,
)

if TYPE_CHECKING:
    from types import ModuleType
    from typing import TypeVar

    from gettsim_personas.typing import (
        GETTSIMScalar,
        OrigPersonas,
    )

    T = TypeVar("T", bound=GETTSIMScalar)


PERSONAS_SOURCE_DIR = Path(__file__).parent / "personas"


def orig_personas() -> OrigPersonas:
    """Load all personas from the personas source directory.

    The path of a persona is determined by the path of the file it is defined in, not
    the name of the persona object itself.
    """
    orig_personas: OrigPersonas = {}
    for path in PERSONAS_SOURCE_DIR.rglob("*.py"):
        module = load_module(path=path, root=PERSONAS_SOURCE_DIR)
        personas_in_this_module = persona_collection_from_module(module)
        if personas_in_this_module:
            orig_tree_path = path.relative_to(PERSONAS_SOURCE_DIR).with_suffix("").parts
            orig_personas[orig_tree_path] = personas_in_this_module

    return orig_personas


def persona_collection_from_module(module: ModuleType) -> PersonaCollection | None:
    personas_in_this_module: list[Persona] = []
    not_implemented_error = None
    for _, obj in inspect.getmembers(module):
        if isinstance(obj, Persona):
            personas_in_this_module.append(obj)
        elif isinstance(obj, PersonaNotImplementedError):
            not_implemented_error = obj
    if personas_in_this_module:
        return PersonaCollection(
            personas=personas_in_this_module,
            not_implemented_error=not_implemented_error,
        )
    return None


def load_module(path: Path, root: Path) -> ModuleType:
    name = path.relative_to(root).with_suffix("").as_posix().replace("/", ".")
    spec = importlib.util.spec_from_file_location(name=name, location=path)
    # Assert that spec is not None and spec.loader is not None, required for mypy
    _msg = f"Could not load module spec for {path},  {root}"
    if spec is None:
        raise ImportError(_msg)
    if spec.loader is None:
        raise ImportError(_msg)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module
