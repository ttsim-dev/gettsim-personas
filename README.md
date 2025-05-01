# GETTSIM Personas

Personas to use as example data when calling GETTSIM.

```python
from gettsim_personas import personas_for_date
from gettsim import set_up_policy_environment, compute_taxes_and_transfers

personas = personas_for_date("2025-01-01")

policy_environment = set_up_policy_environment("2025-01-01")

result = compute_taxes_and_transfers(
    data_tree=personas.couple_1_child.input_data,
    environment=environment,
    targets_tree=personas.couple_1_child.targets_tree,
)
```
