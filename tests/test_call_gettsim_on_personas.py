import pytest
from _gettsim.config import RESOURCE_DIR
from gettsim import compute_taxes_and_transfers, set_up_policy_environment

from gettsim_personas import get_personas


@pytest.mark.parametrize("date_str", [f"{year}-01-01" for year in range(2006, 2025)])
def test_call_gettsim_on_personas(date_str):
    environment = set_up_policy_environment(date=date_str, resource_dir=RESOURCE_DIR)
    all_personas = get_personas(date_str)
    for persona_name in all_personas.all_names:
        persona = all_personas.get_persona(persona_name)
        compute_taxes_and_transfers(
            environment=environment,
            data_tree=persona.input_data,
            targets_tree=persona.targets_tree,
        )
