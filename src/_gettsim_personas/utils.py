from __future__ import annotations

import datetime
import importlib
import re
import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path
    from types import ModuleType

    from _gettsim_personas.typing import DashedISOString


_DASHED_ISO_DATE_REGEX = re.compile(r"\d{4}-\d{2}-\d{2}")


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


def convert_and_validate_dates(
    start_date: datetime.date | DashedISOString,
    end_date: datetime.date | DashedISOString,
) -> tuple[datetime.date, datetime.date]:
    """Convert and validate date strings to datetime.date objects."""
    start_date = to_datetime(start_date)
    end_date = to_datetime(end_date)

    if start_date > end_date:
        msg = f"The start date {start_date} must be before the end date {end_date}."
        raise ValueError(msg)

    return start_date, end_date


def to_datetime(date: datetime.date | DashedISOString) -> datetime.date:
    if isinstance(date, datetime.date):
        return date
    if isinstance(date, str) and _DASHED_ISO_DATE_REGEX.fullmatch(date):
        return datetime.date.fromisoformat(date)
    msg = f"Date {date} neither matches the format YYYY-MM-DD nor is a datetime.date."
    raise ValueError(msg)
