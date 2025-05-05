from __future__ import annotations

import sys
from typing import TYPE_CHECKING

import yaml

if TYPE_CHECKING:
    from gettsim_personas.typing import RawPersonaSpec


def validate_policy_ids(yaml_content: RawPersonaSpec) -> bool:
    p_id_list = yaml_content.get("policy_inputs", {}).get("p_id", [])
    if p_id_list:
        return p_id_list == list(range(len(p_id_list)))
    return True


def collect_errors(files: list[str]) -> int:
    collected_errors = []
    for file_path in files:
        with open(file_path) as f:  # noqa: PTH123
            yaml_content = yaml.safe_load(f)
            if not validate_policy_ids(yaml_content):
                msg = f"""
                Error: {file_path} contains non-consecutive p_ids.
                They must start from 0 and be consecutive.
                """
                collected_errors.append(msg)

    if collected_errors:
        print("\n".join(collected_errors))  # noqa: T201
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(collect_errors(sys.argv[1:]))
