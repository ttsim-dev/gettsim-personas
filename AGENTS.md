@.ai-instructions/profiles/tier-a.md @.ai-instructions/modules/pandas.md

# gettsim-personas

## Overview

**gettsim-personas** provides example household personas for GETTSIM, the German Taxes
and Transfers Simulator. Personas define specific household structures with input data
and tax-transfer targets for a given policy date, enabling exploration and testing of
the tax-transfer system without real data.

Part of the [dev-gettsim workspace](../CLAUDE.md) alongside **ttsim** (computation
engine), **gettsim** (German policy implementations), and **soep-preparation** (SOEP
data pipeline). This project depends on both `ttsim-backend` and `gettsim`.

## Commands

```bash
# Run tests
pixi run -e py314 tests
pixi run -e py314 tests -n 7          # parallel

# Run a single test
pixi run -e py314 tests -k "test_end_to_end"
pixi run -e py314 tests tests/infrastructure/test_persona_objects.py

# Type checking (runs as the ty pre-commit hook)
prek run ty --all-files

# Quality checks
pixi run prek run --all-files

# Available environments: py311, py312, py313, py314
```

Before finishing any task that modifies code, always run these two verification steps in
order:

1. `pixi run prek run --all-files` (quality checks incl. ty type checking)
1. `pixi run -e py314 tests -n 7` (full test suite)

## Architecture

### Two Packages

- **`src/_gettsim_personas/`** -- Internal implementation (private package). Contains
  the core dataclasses, decorators, and persona logic.
- **`src/gettsim_personas/`** -- Public API. Re-exports persona objects organized by
  policy area (e.g., `einkommensteuer_sozialabgaben`,
  `grundsicherung_für_erwerbsfähige`).

### Core Abstractions (`_gettsim_personas/`)

**Persona elements** (`persona_elements.py`) -- Frozen dataclasses created via
decorators, used to define persona data:

- `@persona_pid_element()` -- Defines the `p_id` array (person identifiers)
- `@persona_input_element(tt_qname=..., start_date=..., end_date=...)` -- Defines one
  input column, optionally date-bounded
- `@persona_target_element(start_date=..., end_date=...)` -- Declares a TT target qname
- `@persona_description(description=...)` -- Human-readable description

**`OrigPersonaOverTime`** (`persona_objects.py`) -- Built from a tuple of persona
elements (`elements=`). Filters them by policy date and produces a `Persona` instance.
Supports `LinspaceGrid` for evaluating over a range of earnings.
`upsert_elements(*elements)` derives a new persona: each passed element replaces the
existing elements with the same `tt_qname` (descriptions: the existing descriptions)
only within its own date range; later elements take precedence.

**`load_persona_elements`** (`persona_objects.py`, private) -- Collects the persona
elements defined in an elements module on disk.

**`Persona`** (`persona_objects.py`) -- Frozen dataclass holding resolved
`input_data_tree`, `tt_targets_tree`, `policy_date`, and `description`. Has
`upsert_input_data()` for creating modified copies with different input values and
`input_data_df` for the input data as a DataFrame with qname columns (incl. `p_id`).

**`upsert_input_data`** (`upsert.py`) -- Broadcasts persona data when upserting arrays
of different length, correctly handling `p_id`, foreign keys (`p_id_*`), group IDs
(`*_id`), and regular columns.

### Persona Definition Pattern

Each persona is defined in two layers:

1. **Elements file** (e.g., `de/einkommensteuer_sozialabgaben/couple_1_child.py`) --
   Module with decorated functions returning numpy arrays for each input column, plus
   target declarations.
1. **`__init__.py`** -- Creates an `OrigPersonaOverTime` instance from the elements
   file's elements (via `load_persona_elements`), with optional `start_date`/`end_date`
   constraints.

### Usage with GETTSIM

```python
from gettsim_personas import einkommensteuer_sozialabgaben

persona = einkommensteuer_sozialabgaben.Couple1Child(policy_date_str="2025-01-01")
# persona.input_data_tree  -> nested dict of numpy arrays
# persona.tt_targets_tree  -> nested dict of target qnames
# Pass these to gettsim.main() via InputData and TTTargets
```

### Test Structure

- `tests/infrastructure/` -- Tests for core persona machinery (elements, objects,
  upsert)
- `tests/de/` -- Tests that call GETTSIM on all personas and validate persona
  definitions
- `tests/personas_for_testing/` -- Fixture persona elements (not test files)
- `tests/test_end_to_end.py` -- End-to-end test calling `gettsim.main()` with a persona
