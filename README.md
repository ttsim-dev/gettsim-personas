# GETTSIM Personas

This repository provides example personas to use as input data for GETTSIM. Personas
depict typical households, which GETTSIM's users might be interested in.

## Basic Concepts

### Persona Attributes

Each persona has the following attributes:

- `name`: Unique identifier of the persona
- `description`: a description of the persona
- `start_date`: (Optional) the date from which the persona is valid
- `end_date`: (Optional) the date until which the persona is valid
- `constant_input_data`: the input data used to compute the targets
- `tt_targets_tree`: the targets that can be computed for this persona

> [!WARNING]
> Be careful when using personas in a different context than intended. Many personas
> overwrite GETTSIM's policy functions. Always check whether a persona is suitable for
> your use case.

## Usage Guide

### Loading Personas

Since personas are date-specific, we first need to load the personas for our target
date.

```python
from gettsim_personas import get_personas

jan_2025 = "2025-01-01"

personas = get_personas(jan_2025)

persona = personas.couple_1_child_no_means_tested_transfers
```

The `personas` object contains all available personas for the specified date. In this
example, we selected the `couple_1_child_no_means_tested_transfers` persona for
computing taxes and transfers.

### Computing Taxes and Transfers

We can now compute taxes and transfers for the selected persona.

```python
from gettsim import main, MainTarget, InputData, TTTargets

result = main(
    main_target=MainTarget.results.df_with_nested_columns,
    policy_date_str=jan_2025,
    input_data=InputData.tree(persona.input_data),
    tt_targets=TTTargets(tree=persona.tt_targets_tree),
)
```

### Advanced Usage: Upserting Input Data

Users can modify personas by providing their own input data. This can be done by either
modifying existing inputs (**up**date) or adding new inputs (in**sert**).

#### Why Upsert Input Data?

Consider the `couple_1_child_no_means_tested_transfers` persona, which represents a
household with a specific earnings structure:

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

Let's say we want to create two single-earner households: one where the earner makes
5000 EUR and another where the earner makes 6000 EUR. We could use the persona's input
data as a base and modify it. However, simply repeating the input data (e.g., using
`np.tile`) wouldn't work because the persona represents specific household structures
and interpersonal relationships that we need to preserve.

For instance, GETTSIM requires pointers to individuals' parents. In the
`couple_1_child_no_means_tested_transfers` persona, individuals with `p_id` 0 and 1 are
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

We need to update these pointers when extending the input data to include additional
households.

#### How to Upsert Input Data

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

Alternatively, we can generate a range of income levels using `numpy.linspace`:

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

> [!WARNING]
> The order of input data matters! GETTSIM uses pointers to `p_id`s in the input data to
> depict household structures and relations between individuals. In this example,
> `[0.0, 0.0, 4000.0, 0.0, 0.0, 6000.0]` will return completely different results than
> `[4000.0, 0.0, 0.0, 6000.0, 0.0, 0.0]`. Always check the persona's household structure
> carefully before modifying input data.

Now, we can upsert the input data:

```python
from gettsim_personas import upsert_input_data

upserted_input_data = upsert_input_data(
    data_from_persona=personas.couple_1_child_no_means_tested_transfers.input_data,
    data_to_upsert=bruttolohn_to_upsert,
)
```

The `upsert_input_data` function adds the user-provided input data to the persona's
input data. It creates additional households and broadcasts the persona's original input
data to these new households. Importantly, it ensures that the pointers in the new
households correctly reference the appropriate individuals.

The modified input data can then be used to compute taxes and transfers:

```python
result = main(
    main_target=MainTarget.results.df_with_nested_columns,
    policy_date_str=jan_2025,
    input_data=InputData.tree(upserted_input_data),
    tt_targets=TTTargets(tree=persona.tt_targets_tree),
    backend="numpy",
)
```

> [!WARNING]
> Upserting input data is only possible when the length of the user-provided data is a
> multiple of the length of the persona's input data.
