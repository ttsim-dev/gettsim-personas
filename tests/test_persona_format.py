import datetime

import pytest

from gettsim_personas.load_personas import PERSONAS_DIR, read_persona_yaml

REQUIRED_KEYS = [
    "name",
    "description",
    "policy_inputs",
    "inputs_to_override_nodes",
    "targets_tree",
]


@pytest.mark.parametrize("persona_path", PERSONAS_DIR.glob("*.yaml"))
def test_persona_yamls_have_expected_format(persona_path):
    raw_persona_dict = read_persona_yaml(persona_path)
    assert all(key in raw_persona_dict for key in REQUIRED_KEYS)


@pytest.mark.parametrize("persona_path", PERSONAS_DIR.glob("*.yaml"))
def test_persona_dates_are_valid(persona_path):
    raw_persona_dict = read_persona_yaml(persona_path)
    if "start_date" and "end_date" in raw_persona_dict:
        start_date = datetime.date.fromisoformat(raw_persona_dict["start_date"])
        end_date = datetime.date.fromisoformat(raw_persona_dict["end_date"])
        assert start_date <= end_date
