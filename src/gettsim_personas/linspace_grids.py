from dataclasses import dataclass


@dataclass(frozen=True)
class LinspaceRange:
    bottom: float
    top: float


@dataclass(frozen=True)
class LinspaceGrid2PIds:
    p0: LinspaceRange
    p1: LinspaceRange
    n_points: int


@dataclass(frozen=True)
class LinspaceGrid3PIds:
    p0: LinspaceRange
    p1: LinspaceRange
    p2: LinspaceRange
    n_points: int
