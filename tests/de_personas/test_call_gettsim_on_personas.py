import pytest
from gettsim import InputData, MainTarget, TTTargets, main

from tests.de_personas.all_personas import persona_year_pairs


@pytest.mark.parametrize(
    (
        "year",
        "persona_class",
    ),
    persona_year_pairs(),
)
def test_call_gettsim_on_personas(year, persona_class):
    policy_date_str = f"{year}-01-01"
    persona = persona_class(policy_date=policy_date_str)
    main(
        main_target=MainTarget.results.df_with_nested_columns,
        policy_date_str=policy_date_str,
        input_data=InputData.tree(persona.input_data_tree),
        tt_targets=TTTargets(tree=persona.tt_targets_tree),
        include_warn_nodes=False,
    )
