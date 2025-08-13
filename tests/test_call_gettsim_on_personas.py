# @pytest.mark.parametrize(
#     "policy_date_str", [f"{year}-01-01" for year in range(2005, 2025)]
# )
# def test_call_gettsim_on_personas(policy_date_str):
#     environment = main(
#         main_target=MainTarget.policy_environment,
#         policy_date_str=policy_date_str,
#         backend="numpy",
#     )
#     personas_active_at_date = GETTSIMPersonas.personas_active_at_date(policy_date_str)
#     for persona in personas_active_at_date.values():
#         main(
#             main_target=MainTarget.results.df_with_nested_columns,
#             policy_environment=environment,
#             policy_date_str=policy_date_str,
#             input_data=InputData.tree(persona.input_data_tree),
#             tt_targets=PersonaTargetElements(tree=persona.tt_targets_tree),
#             backend="numpy",
#             include_warn_nodes=False,
#         )
