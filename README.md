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

You can find a tutorial on how to use the personas in
[GETTSIM's documentation](https://gettsim.readthedocs.io/en/stable/tutorials/personas.html).
