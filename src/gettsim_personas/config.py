"""All the general configuration of the project."""

from pathlib import Path

SRC = Path(__file__).parent.resolve()
ROOT = SRC.joinpath("..", "..").resolve()

PERSONAS_DIR = SRC / "personas"

DEFAULT_PERSONA_START_DATE = "1800-01-01"
DEFAULT_PERSONA_END_DATE = "2100-12-31"
