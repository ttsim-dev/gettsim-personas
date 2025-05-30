# GETTSIM Personas

This repository provides example personas to use as input data for GETTSIM. Personas
depict typical households, which GETTSIM's users might be interested in.

Personas are date-specific and provide targets and input data for GETTSIM. Each persona
has the following attributes:

- `name`: the name of the persona
- `description`: a description of the persona constellation
- `purpose`: the purpose of this persona, i.e. what exactly it is trying to depict
- `start_date`: (Optional) the date from which the persona is valid
- `end_date`: (Optional) the date until which the persona is valid
- `policy_inputs`: the policy inputs that are used to calculate the targets
- `policy_inputs_overriding_functions`: a dictionary of functions that are used to
  override GETTSIM's policy functions
- `targets_tree`: the targets that can be computed for this persona

The input data to compute taxes and transfers is stored in the `input_data` attribute,
which combines the `policy_inputs` and the `policy_inputs_overriding_functions` into a
single nested input data dictionary.

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

persona = personas.couple_1_child_no_means_tested_transfers
```

The `personas` objects contains all available personas for the given date. We selected
the `couple_1_child_no_means_tested_transfers` persona to compute taxes and transfers.

### Compute taxes and transfers

Now, we can compute taxes and transfers for the selected persona.

```python
from gettsim import set_up_policy_environment, compute_taxes_and_transfers

environment = set_up_policy_environment(date=jan_01_2025)

result = compute_taxes_and_transfers(
    data_tree=persona.input_data,
    environment=environment,
    targets_tree=persona.targets_tree,
)
```

### Upserting input data

Users may modify the persona by providing their own input data. Users can either modify
existing inputs (**up**date) or add new inputs (in**sert**).

**Why upserting input data?**

The persona `couple_1_child_no_means_tested_transfers`, for example, depicts a single
houshold with a specific earnings structure:

```python
print(
    persona.input_data["einkommensteuer"]["einkünfte"][
        "aus_nichtselbstständiger_arbeit"
    ]["bruttolohn_m"]
)
# 0    5000.0
# 1    4000.0
# 2    0.0
```

Suppose we want to create two single-earner households where the earner of household one
earns 5000 EUR and the earner of household two earns 6000 EUR. For this, we want to use
the persona's input data as a base and modify it. Just repeating the input data (e.g.
via a `np.tile`) would not work because the persona depicts specific household
structures and interpersonal relations that we want to preserve.

For example, GETTSIM requires pointer to the individual's parents. In the persona
`couple_1_child_no_means_tested_transfers`, the individuals with `p_id` 0 and 1 are
parents of the individual with `p_id` 2:

```python
print(persona.input_data["p_id"])
# 0    0
# 1    1
# 2    2

print(persona.input_data["familie"]["p_id_elternteil_1"])
# 0    -1
# 1    -1
# 2    0

print(persona.input_data["familie"]["p_id_elternteil_2"])
# 0    -1
# 1    -1
# 2    1
```

We want to update these pointers when we extend the input data by more than one
household.

**How to upsert input data**

First, we define the input data to upsert:

```python
bruttolohn_to_upsert = {
    "einkommensteuer": {
        "einkünfte": {
            "aus_nichtselbstständiger_arbeit": {
                "bruttolohn_m": [4000.0, 0.0, 0.0, 6000.0, 0.0, 0.0],
            }
        }
    }
}
```

Alternatively, we can specify a range of income levels via a standard `linspace`:

```python
import numpy as np

bruttolohn_to_upsert = {
    "einkommensteuer": {
        "einkünfte": {
            "aus_nichtselbstständiger_arbeit": {
                "bruttolohn_m": [
                    x for i in np.linspace(4000, 10000, 601) for x in [i, 0.0, 0.0]
                ],
            }
        }
    }
}
```

In general, the order of input data matters. This is because GETTSIM uses pointers to
`p_id`s in the input data to depict household structures and relations between
individuals as described above. In this example, `[0.0, 0.0, 4000.0, 0.0, 0.0, 6000.0]`
will return completely different results than `[4000.0, 0.0, 0.0, 6000.0, 0.0, 0.0]`. To
make sure you understand the persona's household structure, we recommend to carefully
check the provided input data.

Now, we can upsert the input data:

```python
from gettsim_personas import upsert_input_data

upserted_input_data = upsert_input_data(
    data_from_persona=personas.couple_1_child_no_means_tested_transfers.input_data,
    data_to_upsert=bruttolohn_to_upsert,
)
```

The function `upsert_input_data` adds the user-provided input data to the persona's
input data. It creates an additional household and broadcasts the persona's original
input data to the new households. In particular, it specifies the pointers of the new
household to point to the correct individuals.

The new input data can then be used to compute taxes and transfers:

```python
result = compute_taxes_and_transfers(
    data_tree=upserted_input_data,
    environment=environment,
    targets_tree=persona.targets_tree,
)
```

> [!WARNING]
> Upserting input data is only possible if the length of the user-provided data is a
> multiple of the length of the persona's input data.
