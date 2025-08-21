# GETTSIM Personas

This repository provides example personas to use with GETTSIM. The personas depict
specific household structures and provide input data and tax-transfer targets for a
given policy date.

Personas are helpful if you are interested in exploring how a specific part of the
tax-transfer system works (e.g. the income tax) using example data. As the input data
provided by a persona can be overriden, you can easily vary GETTSIM's inputs and explore
how this affects the results.

Even if you already have some data at hand, personas are a great way to find out how to
prepare it for using it with GETTSIM. Currently, there are almost 100 input columns
necessary to compute all taxes and transfers covered by GETTSIM, so finding out which of
them are important and which are not is crucial in any application using real data. If a
persona exists that corresponds to your use case, it provides a minimal set of input
data, overriding nodes of the tax-transfer system that are probably not relevant for
your use case (e.g. the calculation of pension benefits when you're interested in the
income tax).

If no existing persona corresponds to your use case, feel free to open an
[issue](https://github.com/ttsim-dev/gettsim-personas/issues) or
[make a contribution](https://gettsim.readthedocs.io/en/stable/gettsim_developer/how-to-contribute.html)!

## Basic example

We first show the simplest case of loading a persona and running GETTSIM on it.

Personas must be instantiated with a `policy_date`, as their content varies depending on
the policy environment at that date.

We start by importing the module with personas relevant to calculating net income for
working-age people who do not take up (or qualify for) any means- or health-tested
transfers:

```python
from gettsim_personas import einkommensteuer_sozialabgaben

example_persona = einkommensteuer_sozialabgaben.Couple1Child(
    policy_date_str="2025-01-01"
)
```

`example_persona` is a `Persona` object with the following attributes:

- `description`: A description of the persona. Use this to check if the persona is
  suitable for your use case. (A proper documentation of the available personas is not
  yet implemented;
  [contributions are welcome!](https://github.com/ttsim-dev/gettsim-personas/issues/9))
- `policy_date`: The policy date of this persona.
- `evaluation_date`: The evaluation date of this persona.
- `input_data_tree`: The input data tree of this persona. This can be passed directly to
  GETTSIM's `main` function.
- `tt_targets_tree`: The targets that can be computed for this persona. This can also be
  passed to GETTSIM's `main` function.

> [!WARNING]
> Be careful when using personas outside their intended context. Many personas overwrite
> GETTSIM's policy functions. Always check whether a persona is suitable for your use
> case. Before using a persona, review its `description` field to ensure it fits your
> needs. For example, the personas in the `einkommensteuer_sozialabgaben` package are
> not suited to compute disposable income of low-income households, because the persona
> inputs are set up in a way that all means- and health-tested transfers are assumed not
> to be taken up (while in reality, some of those transfers have very high take-up rates
> among low-income households).

You can now compute taxes and transfers for the selected persona:

```python
from gettsim import main, MainTarget, InputData, TTTargets

result = main(
    main_target=MainTarget.results.df_with_nested_columns,
    policy_date=example_persona.policy_date,
    input_data=InputData.tree(example_persona.input_data_tree),
    tt_targets=TTTargets.tree(example_persona.tt_targets_tree),
)

print(result)

>>>      einkommensteuer kindergeld    sozialversicherung
>>>          betrag_y_sn   betrag_y          arbeitslosen               kranken                pflege                 rente
>>>                  NaN        NaN               beitrag               beitrag               beitrag               beitrag
>>>                  NaN        NaN betrag_versicherter_y betrag_versicherter_y betrag_versicherter_y betrag_versicherter_y
>>> p_id
>>> 0             7164.0       3060                 468.0                3078.0                 648.0                3348.0
>>> 1             7164.0          0                 468.0                3078.0                 648.0                3348.0
>>> 2                0.0          0                   0.0                   0.0                   0.0                   0.0
```

### Optional Arguments When Instantiating a Persona

You can provide a grid of earnings levels to compute taxes and transfers across
different earnings levels. For example, we may want to look at net income in our example
household where the father earns 4,000 Euro per month. If working full-time, the mother
would earn the same amount. We want to investigate how total net income varies as she
changes her weekly ours between 25% and 75% of full-time work.

To do this, create a `LinspaceGrid` object and specify the earnings range for each
`p_id`:

```python
from gettsim_personas import einkommensteuer_sozialabgaben

persona_with_varying_income_of_secondary_earner = einkommensteuer_sozialabgaben.Couple1Child(
    policy_date_str="2025-01-01",
    bruttolohn_m_linspace_grid=einkommensteuer_sozialabgaben.Couple1Child.LinspaceGrid(
        p0=einkommensteuer_sozialabgaben.Couple1Child.LinspaceRange(
            bottom=4_000, top=4_000
        ),
        p1=einkommensteuer_sozialabgaben.Couple1Child.LinspaceRange(
            bottom=1_000, top=3_000
        ),
        p2=einkommensteuer_sozialabgaben.Couple1Child.LinspaceRange(bottom=0, top=0),
        n_points=100,
    ),
)
```

Personas support different evaluation dates. Personas fix some input columns to constant
values (e.g. age or age at retirement) and calculate the values of other input columns
(e.g. birth year or year of retirement) based on these constant input columns plus an
evaluation date. If no evaluation date is provided, the policy date is used by default.

```python
example_persona_with_evaluation_date = einkommensteuer_sozialabgaben.Couple1Child(
    policy_date_str="2025-01-01",
    evaluation_date_str="2026-01-01",
)
```

### Advanced Usage: Upserting Input Data

You can also vary persona input data across dimensions other than earnings. The
`upsert_input_data` function creates copies of the persona's input data, varying them
over the dimensions you specify, while preserving the household structure of the
original persona.

#### How to Upsert Input Data

Suppose you are interested in households that receive basic subsistence benefits for the
unemployed (Bürgergeld, formerly known as Arbeitslosengeld 2). You want to vary their
benefit entitlement by changing their gross rent excluding dwelling costs (a GETTSIM
input variable).

First, instantiate the base persona:

```python
from gettsim_personas import grundsicherung_für_erwerbsfähige

basic_subsistence_benefit_persona = grundsicherung_für_erwerbsfähige.Couple1Child(
    policy_date_str="2025-01-01"
)
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
            x for i in np.linspace(300, 1800, 601) for x in [i, i, i]
        ],
    }
}
```

> [!WARNING]
> The order of input data matters! GETTSIM uses pointers to `p_id`s in the input data to
> depict household structures and relationships between individuals. In general,
> `[0.0, 0.0, 4000.0, 0.0, 0.0, 6000.0]` will yield completely different results than
> `[4000.0, 0.0, 0.0, 6000.0, 0.0, 0.0]`. Always check the persona's household structure
> carefully before modifying input data. In the example above, inputs are on the
> household level, so every household member should have the same value for
> `bruttokaltmiete_m_hh`.

Now, upsert the input data:

```python
from gettsim_personas import upsert_input_data

upserted_input_data = upsert_input_data(
    input_data=basic_subsistence_benefit_persona.input_data_tree,
    data_to_upsert=rent_to_upsert,
)
```

The modified input data can then be used to compute taxes and transfers:

```python
result = main(
    main_target=MainTarget.results.df_with_nested_columns,
    policy_date=basic_subsistence_benefit_persona.policy_date,
    input_data=InputData.tree(upserted_input_data),
    tt_targets=TTTargets.tree(basic_subsistence_benefit_persona.tt_targets_tree),
)
```

> [!WARNING]
> Upserting input data is only possible when the length of the user-provided data is a
> multiple of the length of the persona's input data.
