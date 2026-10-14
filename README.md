# Data Center Calculator

## Overview

A preliminary Python calculator for basic data-center planning calculations. It provides six functions for calculating total rack load, nominal and usable circuit capacity, required circuit counts, and conductor footage.

**Important:** These calculations are preliminary. Engineering assumptions and formulas must be reviewed and approved by a qualified engineering reviewer before production use.

## Requirements

- Python 3.13 or a compatible Python version.
- No third-party packages are required by the current calculator or test suite.

## Setup

From the project root, create and activate a virtual environment if you do not already have one.

On macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## Run the Tests

From the project root, run:

```bash
python -m unittest discover -s tests -v
```

The test suite covers expected calculation results, invalid inputs, boundary conditions, numeric overflow, keyword arguments, and a complete workflow that uses multiple functions together.

## Available Functions

| Function | Purpose | Output |
|---|---|---|
| `calculate_total_rack_load` | Calculates rack count × load per rack | Same unit as the rack load input |
| `calculate_nominal_circuit_capacity` | Estimates single-phase or three-phase nominal capacity | kVA |
| `calculate_usable_circuit_capacity` | Applies a loading factor to nominal capacity | Same unit as nominal capacity |
| `calculate_required_circuits` | Estimates the required number of circuits, rounded up | Circuit count |
| `calculate_base_conductor_footage` | Calculates conductor length before waste allowance | Same length unit as average run length |
| `calculate_total_conductor_footage` | Adds a waste allowance to base conductor footage | Same length unit as base footage |

## Input Expectations

- Use consistent units within each calculation.
- `phase` must be `single_phase` or `three_phase`.
- `loading_factor` must be greater than zero and no greater than `1`.
- `waste_allowance` must be between `0` and `1`; for example, `0.10` represents 10%.
- Rack counts, circuit counts, and conductors per circuit must be positive integers where required.
- Numeric inputs must satisfy the validation rules implemented by each function.

## Engineering Assumptions and Limitations

This calculator does not independently verify electrical code compliance, redundancy requirements, power factor, cable sizing, or site-specific design constraints.

Confirm the formulas, units, electrical assumptions, and design requirements with the responsible engineering reviewer before using results for actual installations.

## Project Structure

```text
data-center-calculator/
├── .gitignore
├── README.md
├── src/
│   ├── __init__.py
│   └── calculator.py
└── tests/
    ├── __init__.py
    └── test_calculator.py
```
