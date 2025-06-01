from datetime import date

import pytest

from gettsim_personas.get_personas import (
    _fail_if_multiple_personas_with_same_name_active_at_same_date,
)
from gettsim_personas.persona_objects import Persona

_GENERIC_PERSONA_SPEC = {
    "name": "persona_1",
    "description": "",
    "policy_inputs": {},
    "policy_inputs_overriding_functions": {},
    "targets_tree": {},
}


@pytest.mark.parametrize(
    ("personas", "match"),
    [
        (
            [
                Persona(
                    start_date=date(2000, 1, 1),
                    end_date=date(2000, 12, 31),
                    **_GENERIC_PERSONA_SPEC,
                ),
                Persona(
                    start_date=date(2000, 1, 1),
                    end_date=date(2000, 12, 31),
                    **_GENERIC_PERSONA_SPEC,
                ),
            ],
            "Overlapping periods: 2000-01-01 - 2000-12-31 and 2000-01-01 - 2000-12-31.",
        ),
        (
            [
                Persona(
                    start_date=date(2000, 1, 1),
                    end_date=date(2000, 12, 31),
                    **_GENERIC_PERSONA_SPEC,
                ),
                Persona(
                    start_date=date(2000, 12, 31),
                    end_date=date(2001, 1, 1),
                    **_GENERIC_PERSONA_SPEC,
                ),
            ],
            "Overlapping periods: 2000-01-01 - 2000-12-31 and 2000-12-31 - 2001-01-01.",
        ),
    ],
)
def test_fail_if_multiple_personas_with_same_name_active_at_same_date(personas, match):
    with pytest.raises(ValueError, match=match):
        _fail_if_multiple_personas_with_same_name_active_at_same_date(personas)
