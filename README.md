# Data Center Calculator

## Overview

A preliminary Python calculator for basic data-center planning calculations. It provides functions for rack load, nominal and usable circuit capacity, required circuit counts, and conductor footage.

**Important:** These calculations are preliminary. Engineering assumptions and formulas must be reviewed and approved before production use.

## Requirements

- Python 3.13 or a compatible Python version
- No third-party packages are required by the current calculator and tests.

## Setup

Clone or open the project directory, then activate the virtual environment.

On macOS:

```bash
source .venv/bin/activate
```

## Run the Tests

From the project root, run:

```bash
python -m unittest discover -s tests -v
```

The test suite checks expected calculation results, invalid inputs, boundary conditions, and a workflow using multiple functions together.

## Available Functions

| Function | Purpose | Output |
|---|---|---|
| `calculate_total_rack_load` | Calculates rack count × load per rack | Same unit as rack load input |
| `calculate_nominal_circuit_capacity` | Estimates single-phase or three-phase capacity | kVA |
| `calculate_usable_circuit_capacity` | Applies a loading factor | Same unit as nominal capacity |
| `calculate_required_circuits` | Estimates the number of circuits, rounded up | Circuit count |
| `calculate_base_conductor_footage` | Calculates conductor length before waste | Same length unit as average run length |
| `calculate_total_conductor_footage` | Adds a waste allowance to base footage | Same length unit as base footage |

## Input Expectations

- Use consistent units for all inputs to a calculation.
- `phase` must be `single_phase` or `three_phase`.
- `loading_factor` must be greater than zero and no greater than 1.
- `waste_allowance` must be between 0 and 1; for example, `0.10` represents 10%.
- Circuit counts and conductors per circuit must be positive integers.

## Engineering Assumptions

The calculator does not independently verify electrical code compliance, redundancy requirements, power factor, cable sizing, or site-specific design constraints.

Confirm the formulas, units, and design assumptions with the responsible engineering reviewer before using results for actual installations.

## Project Structure

```text
data-center-calculator/
├── src/
│   ├── __init__.py
│   └── calculator.py
├── tests/
│   ├── __init__.py
│   └── test_calculator.py
├── .gitignore
└── README.md
```
