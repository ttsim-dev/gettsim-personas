import pytest
from gettsim import InputData, MainTarget, TTTargets, main

from gettsim_personas import GETTSIMPersonas


@pytest.mark.parametrize("date_str", [f"{year}-01-01" for year in range(2006, 2025)])
def test_call_gettsim_on_personas(date_str):
    environment = main(
        main_target=MainTarget.policy_environment,
        policy_date_str=date_str,
        backend="numpy",
    )
    personas_active_at_date = GETTSIMPersonas.personas_active_at_date(date_str)
    for persona in personas_active_at_date.personas:
        main(
            main_target=MainTarget.results.df_with_nested_columns,
            policy_environment=environment,
            policy_date_str=date_str,
            input_data=InputData.tree(persona.input_data_tree),
            tt_targets=TTTargets(tree=persona.tt_targets_tree),
            backend="numpy",
            include_warn_nodes=False,
        )
