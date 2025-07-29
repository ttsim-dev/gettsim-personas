import pytest
from gettsim import InputData, MainTarget, TTTargets, main

from gettsim_personas import get_personas


@pytest.mark.parametrize("date_str", [f"{year}-01-01" for year in range(2006, 2025)])
def test_call_gettsim_on_personas(date_str):
    environment = main(
        main_target=MainTarget.policy_environment,
        policy_date_str=date_str,
        backend="numpy",
    )
    all_personas = get_personas(date_str)
    for persona_name in all_personas.all_names:
        persona = all_personas.get_persona(persona_name)
        main(
            main_target=MainTarget.results.df_with_nested_columns,
            policy_environment=environment,
            policy_date_str=date_str,
            input_data=InputData.tree(persona.constant_input_data),
            tt_targets=TTTargets(tree=persona.tt_targets_tree),
            backend="numpy",
            include_warn_nodes=False,
        )
