from __future__ import annotations

import sys
from typing import TYPE_CHECKING

import yaml

if TYPE_CHECKING:
    from gettsim_personas.typing import RawPersonaSpec


def collect_errors(files: list[str]) -> int:
    """Hook that validates id vars in persona files.

    We put tight bounds on the specification of ID vars because this allows for robust
    broadcasting.
    """
    collected_errors = []
    for file_path in files:
        with open(file_path) as f:  # noqa: PTH123
            yaml_content = yaml.safe_load(f)
            if (
                faulty_id_vars
                := all_id_vars_start_with_zero_and_are_weakly_consecutive_increasing(
                    yaml_content
                )
            ):
                msg = f"""
                Error: {file_path} contains non-consecutive ID vars.
                They must start from 0 and be weakly consecutive increasing.
                The following ID vars are incorrectly specified:
                {", ".join(faulty_id_vars)}
                """
                collected_errors.append(msg)

    if collected_errors:
        print("\n".join(collected_errors))  # noqa: T201
        return 1
    return 0


def all_id_vars_start_with_zero_and_are_weakly_consecutive_increasing(
    persona: RawPersonaSpec,
) -> list[str]:
    """Returns the names of all ID vars of this persona that are incorrectly specified.

    ID vars are required to:
        - start with 0
        - be weakly consecutive increasing

    OK:
    - 0, 1, 2
    - 0, 0, 0
    - 0, 1, 1
    Not OK:
    - 0, 1, 3
    - 0, 1, 0
    """
    policy_inputs = persona.get("policy_inputs", {})
    all_id_vars = {k: v for k, v in policy_inputs.items() if k.endswith("_id")}
    return [
        k for k, v in all_id_vars.items() if not _is_weakly_consecutive_increasing(v)
    ]


def _is_weakly_consecutive_increasing(id_values: list[int]) -> bool:
    """Check if a list of integers is weakly consecutive increasing starting from 0."""
    if not id_values or id_values[0] != 0:
        return False
    last = 0
    for val in id_values:
        if val < last or val > last + 1:
            return False
        last = val
    return True


if __name__ == "__main__":
    sys.exit(collect_errors(sys.argv[1:]))
