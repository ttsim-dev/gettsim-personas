# GETTSIM Personas

This repository provides example personas to use as input data for GETTSIM. Personas
depict typical households, which GETTSIM's users might be interested in.

Personas are date-specific and provide targets and input data for GETTSIM. Each persona
has the following structure:

- `name`: the name of the persona
- `description`: a description of the persona constellation
- `purpose`: the purpose of this persona, i.e. what exactly it is trying to depict
- `start_date`: (Optional) the date from which the persona is valid
- `end_date`: (Optional) the date until which the persona is valid
- `policy_inputs`: the policy inputs that are used to calculate the targets
- `policy_inputs_overriding_functions`: a dictionary of functions that are used to
  override GETTSIM's policy functions
- `targets_tree`: the targets that can be computed for this persona

> [!WARNING]
> Be careful when using personas in a different context than intended. Many personas
> overwrite GETTSIM's policy functions via `policy_inputs_overriding_functions` or
> represent specific household structures. Always check whether a persona is suitable
> for your use case.

## Usage

The following example shows how to use a persona to calculate taxes and transfers for a
household.

### Load personas for a specific date

As personas are date-specific, we first need to load the personas for the date we are
interested in.

```python
from gettsim_personas import get_personas

jan_01_2025 = "2025-01-01"
personas = get_personas(jan_01_2025)

couple_1_child_no_means_tested_transfers = (
    personas.couple_1_child_no_means_tested_transfers
)
```

The `personas` objects contains all available personas for the given date. We selected
the `couple_1_child_no_means_tested_transfers` persona to compute taxes and transfers.

### Compute taxes and transfers

Now, we can compute taxes and transfers for the selected persona.

```python
from gettsim import set_up_policy_environment, compute_taxes_and_transfers

environment = set_up_policy_environment(date=jan_01_2025)

result = compute_taxes_and_transfers(
    data_tree=couple_1_child_no_means_tested_transfers.input_data,
    environment=environment,
    targets_tree=couple_1_child_no_means_tested_transfers.targets_tree,
)
```

### Upserting input data

Users may modify the persona by providing their own input data. Users can either add new
inputs or modify existing inputs. The function `upsert_input_data` adds the
user-provided input data to the persona's input data and broadcasts the persona's data
to match the length of the user-provided data.

```python
from gettsim_personas import upsert_input_data

bruttolohn_to_upsert = {
    "einkommensteuer": {
        "einkünfte": {
            "aus_nichtselbstständiger_arbeit": {
                "bruttolohn_m": pd.Series([4000.0, 0.0, 0.0, 6000.0, 0.0, 0.0])
            }
        }
    }
}

upserted_input_data = upsert_input_data(
    data_from_persona=personas.couple_1_child_no_means_tested_transfers.input_data,
    data_to_upsert=bruttolohn_to_upsert,
)
```

> [!WARNING]
> Upserting input data is only possible if the length of the user-provided data is a
> multiple of the length of the input data from the persona.
