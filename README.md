# GETTSIM Personas

This repository provides example personas to use as input data for GETTSIM. Personas
depict typical households, which GETTSIM's users might be interested in.

Personas are date-specific, as their input data and targets reflect the policy
environment at a given date.

## Usage Guide

### Loading Personas

Personas must be instantiated with a `policy_date`, as their content varies depending on
the policy environment at that date.

```python
from gettsim_personas.einkommensteuer_sozialabgaben import Couple1Child

jan_2025 = "2025-01-01"

persona_jan_2025 = Couple1Child(policy_date=jan_2025)
```

`persona_jan_2025` is a `PersonaForDate` object with the following attributes:

- `description`: A description of the persona. Use this to check if the persona is
  suitable for your use case.
- `input_data_tree`: The input data tree of this persona. This can be passed directly to
  GETTSIM's `main` function.
- `tt_targets_tree`: The targets that can be computed for this persona. This can also be
  passed to GETTSIM's `main` function.

> [!WARNING]
> Be careful when using personas outside their intended context. Many personas overwrite
> GETTSIM's policy functions. Always check whether a persona is suitable for your use
> case. Before using a persona, review its `description` field to ensure it fits your
> needs.

### Optional Arguments When Instantiating a Persona

Personas support different evaluation dates. If no evaluation date is provided, the
policy date is used by default. Evaluation dates are required to set time-dependent
input variables, such as birth years or the calendar year of retirement.

```python
persona_jan_2025_with_evaluation_date = Couple1Child(
    policy_date=jan_2025,
    evaluation_date="2026-01-01",
)
```

You can also provide a grid of earnings levels to compute taxes and transfers across
different earnings levels. To do this, create a `LinspaceGrid` object and specify the
earnings range for each `p_id`:

```python
from gettsim_personas.einkommensteuer_sozialabgaben import Couple1Child

persona_jan_2025 = Couple1Child(
    policy_date="2025-01-01",
    bruttolohn_m_linspace_grid=Couple1Child.LinspaceGrid(
        p0=Couple1Child.LinspaceRange(bottom=0, top=10000),
        p1=Couple1Child.LinspaceRange(bottom=0, top=10000),
        p2=Couple1Child.LinspaceRange(bottom=0, top=0),
        n_points=100,
    ),
)
```

### Computing Taxes and Transfers

You can now compute taxes and transfers for the selected persona:

```python
from gettsim import main, MainTarget, InputData, TTTargets

result = main(
    main_target=MainTarget.results.df_with_nested_columns,
    policy_date_str=jan_2025,
    input_data=InputData.tree(persona_jan_2025.input_data_tree),
    tt_targets=TTTargets.tree(persona_jan_2025.tt_targets_tree),
)
```

### Advanced Usage: Upserting Input Data

You can also vary persona input data across dimensions other than earnings. The
`upsert_input_data` function creates copies of the persona's input data, varying them
over the dimensions you specify, while preserving the household structure of the
original persona.

#### How to Upsert Input Data

Suppose you are interested in households that receive basic subsistence benefits for the
unemployed (citizen's income). You want to vary their benefit entitlement by changing
their gross rent excluding dwelling costs (a GETTSIM input variable).

First, instantiate the base persona:

```python
from gettsim_personas.grundsicherung_für_erwerbsfähige import Couple1Child

basic_subsistence_benefit_persona = Couple1Child(policy_date="2025-01-01")
```

Next, define the input data to upsert:

```python
rent_to_upsert = {
    "wohnen": {"bruttokaltmiete_m_hh": [600.0, 600.0, 600.0, 800.0, 800.0, 800.0]}
}
```

Alternatively, you can generate a range of rent levels using `numpy.linspace`:

```python
import numpy as np

rent_to_upsert = {
    "wohnen": {
        "bruttokaltmiete_m_hh": [
            x for i in np.linspace(300, 1800, 601) for x in [i, 0.0, 0.0]
        ],
    }
}
```

> [!WARNING]
> The order of input data matters! GETTSIM uses pointers to `p_id`s in the input data to
> depict household structures and relationships between individuals. In general,
> `[0.0, 0.0, 4000.0, 0.0, 0.0, 6000.0]` will yield completely different results than
> `[4000.0, 0.0, 0.0, 6000.0, 0.0, 0.0]`. Always check the persona's household structure
> carefully before modifying input data.

Now, upsert the input data:

```python
from gettsim_personas import upsert_input_data

upserted_input_data = upsert_input_data(
    input_data=persona.input_data_tree,
    data_to_upsert=rent_to_upsert,
)
```

The modified input data can then be used to compute taxes and transfers:

```python
result = main(
    main_target=MainTarget.results.df_with_nested_columns,
    policy_date_str=jan_2025,
    input_data=InputData.tree(upserted_input_data),
    tt_targets=TTTargets.tree(persona.tt_targets_tree),
)
```

> [!WARNING]
> Upserting input data is only possible when the length of the user-provided data is a
> multiple of the length of the persona's input data.
