# GETTSIM Personas

This repository provides example personas to use with GETTSIM. The personas depict
specific household structures and provide input data and tax-transfer targets for a
given policy date.

Personas are helpful if you are interested in exploring how a specific part of the
tax-transfer system works (e.g. the income tax) using example data. As the input data
provided by a persona can be overridden, you can easily vary GETTSIM's inputs and
explore how this affects the results.

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

## Defining your own personas

You can build a persona of your own from persona elements, either from scratch or by
extending an existing persona. Pass an existing persona as `base` and your own elements
via `elements`. Where one of your elements and one of the base's elements target the
same `tt_qname` and are active on the same policy date, yours wins. The members of the
base are fixed: for a different household, define a new persona without a `base`.

```python
import numpy as np
from gettsim_personas import (
    OrigPersonaOverTime,
    persona_input_element,
    persona_target_element,
)
from gettsim_personas.einkommensteuer_sozialabgaben import Couple1Child


@persona_input_element(
    tt_qname="einnahmen__bruttolohn_m",
    start_date="2020-01-01",
    end_date="2029-12-31",
)
def bruttolohn_m_in_the_2020s() -> np.ndarray:
    return np.array([4000, 2000, 0])


@persona_target_element()
def einkommensteuer__betrag_y_sn() -> None:
    pass


MyCouple1Child = OrigPersonaOverTime(
    elements=(bruttolohn_m_in_the_2020s, einkommensteuer__betrag_y_sn),
    base=Couple1Child,
)

persona = MyCouple1Child(policy_date_str="2025-01-01")
```

Without a `base`, your elements must form a complete persona: a `@persona_description`,
a `@persona_pid_element` returning the `p_id` array, a `hh_id` input element, all other
required input elements, and at least one `@persona_target_element`.

You can find a tutorial on how to use the personas in
[GETTSIM's documentation](https://gettsim.readthedocs.io/en/stable/tutorials/personas.html).
