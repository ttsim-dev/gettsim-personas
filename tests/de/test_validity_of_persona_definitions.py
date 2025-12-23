"""Test that all persona definitions are valid."""

import dags.tree as dt
import pytest
from gettsim import InputData, MainTarget, TTTargets, main

from tests.de.all_personas import persona_year_pairs


@pytest.mark.parametrize(
    (
        "year",
        "persona_class",
    ),
    persona_year_pairs(start=2015),
)
def test_persona_inputs_does_not_contain_unnecessary_inputs(year, persona_class):
    policy_date_str = f"{year}-01-01"
    persona = persona_class(policy_date_str=policy_date_str)
    root_nodes = main(
        main_target=MainTarget.labels.root_nodes,
        policy_date_str=policy_date_str,
        input_data=InputData.tree(persona.input_data_tree),
        tt_targets=TTTargets.tree(persona.tt_targets_tree),
        include_warn_nodes=False,
    )
    input_qnames = dt.flatten_to_qnames(persona.input_data_tree)
    unnecessary_inputs = set(input_qnames) - set(root_nodes) - {"hh_id", "p_id"}
    assert not unnecessary_inputs


@pytest.mark.parametrize(
    (
        "year",
        "persona_class",
    ),
    persona_year_pairs(start=2015),
)
def test_persona_contains_minimal_id_inputs(year, persona_class):
    policy_date_str = f"{year}-01-01"
    persona = persona_class(policy_date_str=policy_date_str)
    assert "hh_id" in persona.input_data_tree
    assert "p_id" in persona.input_data_tree
