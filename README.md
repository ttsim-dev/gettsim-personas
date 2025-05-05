# GETTSIM Personas

Personas to use as example data when calling GETTSIM.

```python
import pandas as pd

from gettsim_personas import personas_for_date, upsert_input_data
from gettsim import set_up_policy_environment, compute_taxes_and_transfers

personas = personas_for_date("2025-01-01")

environment = set_up_policy_environment(date="2025-01-01")

bruttolohn_to_upsert = {
    "einkommensteuer": {
        "einkünfte": {
            "aus_nichtselbstständiger_arbeit": {
                "bruttolohn_m": {pd.Series([4000.0, 0.0, 0.0, 6000.0, 0.0, 0.0])}
            }
        }
    }
}

upserted_input_data = upsert_input_data(
    data_from_persona=personas.couple_1_child.input_data,
    data_to_upsert=bruttolohn_to_upsert,
)

result = compute_taxes_and_transfers(
    data_tree=upserted_input_data,
    environment=environment,
    targets_tree=personas.couple_1_child.targets_tree,
)
```
