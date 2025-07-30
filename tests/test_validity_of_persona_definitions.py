"""Test that all persona definitions are valid."""

import dags.tree as dt
import pytest
from gettsim import InputData, MainTarget, TTTargets, main

from gettsim_personas import GETTSIMPersonas
from gettsim_personas.orig_personas import orig_personas


def is_weakly_consecutive_increasing(id_values) -> bool:
    """Check if a list of integers is weakly consecutive increasing starting from 0."""
    if id_values[0] != 0:
        return False
    last = 0
    for val in id_values:
        if val < last or val > last + 1:
            return False
        last = val
    return True


def test_p_ids_are_consecutive():
    """Test that all p_ids in persona files are weakly consecutive increasing."""
    all_personas = orig_personas()

    for path, persona_collection in all_personas.items():
        for persona in persona_collection.personas:
            p_id_array = persona.input_data_tree.get("p_id")
            if not is_weakly_consecutive_increasing(p_id_array):
                msg = (
                    f"'p_id's in at least one persona at '{path}' are not weakly "
                    f"consecutive increasing: {p_id_array}"
                )
                raise ValueError(msg)


@pytest.mark.parametrize(
    "policy_date_str", [f"{year}-01-01" for year in range(2015, 2025)]
)
def test_persona_inputs_does_not_contain_unnecessary_inputs(policy_date_str):
    environment = main(
        main_target=MainTarget.policy_environment,
        policy_date_str=policy_date_str,
        backend="numpy",
    )
    personas_active_at_date = GETTSIMPersonas.personas_active_at_date(policy_date_str)
    for path, persona in personas_active_at_date.items():
        root_nodes = main(
            main_target=MainTarget.labels.root_nodes,
            policy_environment=environment,
            policy_date_str=policy_date_str,
            input_data=InputData.tree(persona.input_data_tree),
            tt_targets=TTTargets(tree=persona.tt_targets_tree),
            backend="numpy",
            include_warn_nodes=False,
        )
        input_qnames = dt.flatten_to_qnames(persona.input_data_tree)
        unnecessary_inputs = set(input_qnames) - set(root_nodes)
        if unnecessary_inputs:
            msg = (
                f"The following inputs are not used in one persona with path "
                f"'{path}': \n\n"
                f"{unnecessary_inputs}"
            )
            raise ValueError(msg)
