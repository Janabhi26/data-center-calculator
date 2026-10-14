
"""Basic functions for the Data Center Calculator.

These functions provide preliminary calculations only.
Engineering assumptions must be reviewed before production use.
"""

import math


def _get_inputs(args, kwargs, names):
    """Read inputs supplied positionally or by keyword."""
    if args and kwargs:
        raise ValueError(
            "Use positional arguments or keyword arguments, not both."
        )

    if args:
        if len(args) != len(names):
            raise ValueError(f"Expected {len(names)} arguments: {names}.")
        return args

    expected_names = set(names)
    provided_names = set(kwargs)

    unexpected = provided_names - expected_names
    if unexpected:
        raise ValueError(
            f"Unexpected keyword arguments: {sorted(unexpected)}."
        )

    missing = expected_names - provided_names
    if missing:
        raise ValueError(
            f"Missing required keyword arguments: {sorted(missing)}."
        )

    return tuple(kwargs[name] for name in names)


def _positive_number(name, value):
    """Validate a finite positive number."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a number.")

    try:
        valid = math.isfinite(value) and value > 0
    except OverflowError:
        valid = False

    if not valid:
        raise ValueError(f"{name} must be finite and greater than zero.")


def _finite_result(name, result):
    """Reject calculation results that are not finite numbers."""
    if isinstance(result, bool) or not isinstance(result, (int, float)):
        raise ValueError(f"{name} must be a finite number.")

    try:
        valid = math.isfinite(result)
    except OverflowError:
        valid = False

    if not valid:
        raise ValueError(f"{name} must be a finite number.")

    return result


def _calculate_finite(name, calculation):
    """Run a calculation and normalize arithmetic overflow to ValueError."""
    try:
        result = calculation()
    except (OverflowError, ZeroDivisionError):
        raise ValueError(f"{name} is outside the supported numeric range.") from None

    return _finite_result(name, result)


def calculate_total_rack_load(*args, **kwargs):
    """Return total rack load in the same unit as load_per_rack."""
    rack_count, load_per_rack = _get_inputs(
        args, kwargs, ("rack_count", "load_per_rack")
    )

    if isinstance(rack_count, bool) or not isinstance(rack_count, int):
        raise ValueError("rack_count must be an integer.")
    if rack_count <= 0:
        raise ValueError("rack_count must be greater than zero.")

    _positive_number("load_per_rack", load_per_rack)
    return _calculate_finite(
        "total_rack_load", lambda: rack_count * load_per_rack
    )


def calculate_nominal_circuit_capacity(*args, **kwargs):
    """Return nominal circuit capacity in kVA.

    phase must be 'single_phase' or 'three_phase'.
    """
    voltage, breaker_rating, phase = _get_inputs(
        args, kwargs, ("voltage", "breaker_rating", "phase")
    )

    _positive_number("voltage", voltage)
    _positive_number("breaker_rating", breaker_rating)

    if phase == "single_phase":
        return _calculate_finite(
            "nominal_circuit_capacity",
            lambda: voltage * breaker_rating / 1000,
        )

    if phase == "three_phase":
        return _calculate_finite(
            "nominal_circuit_capacity",
            lambda: math.sqrt(3) * voltage * breaker_rating / 1000,
        )

    raise ValueError("phase must be 'single_phase' or 'three_phase'.")


def calculate_usable_circuit_capacity(*args, **kwargs):
    """Apply a supplied loading factor to nominal capacity."""
    nominal_capacity, loading_factor = _get_inputs(
        args, kwargs, ("nominal_capacity", "loading_factor")
    )

    _positive_number("nominal_capacity", nominal_capacity)
    _positive_number("loading_factor", loading_factor)

    if loading_factor > 1:
        raise ValueError("loading_factor must not exceed 1.")

    return _calculate_finite(
        "usable_circuit_capacity",
        lambda: nominal_capacity * loading_factor,
    )


def calculate_required_circuits(*args, **kwargs):
    """Return the estimated number of circuits, rounded up."""
    total_load, usable_capacity = _get_inputs(
        args, kwargs, ("total_load", "usable_capacity")
    )

    _positive_number("total_load", total_load)
    _positive_number("usable_capacity", usable_capacity)

    ratio = _calculate_finite(
        "required_circuits_ratio",
        lambda: total_load / usable_capacity,
    )

    try:
        return math.ceil(ratio)
    except (OverflowError, ValueError):
        raise ValueError(
            "required circuit count is outside the supported numeric range."
        ) from None


def calculate_base_conductor_footage(*args, **kwargs):
    """Return conductor footage before waste allowance, in feet."""
    circuit_count, average_run_length, conductors_per_circuit = _get_inputs(
        args,
        kwargs,
        ("circuit_count", "average_run_length", "conductors_per_circuit"),
    )

    if (
        isinstance(circuit_count, bool)
        or not isinstance(circuit_count, int)
        or circuit_count <= 0
    ):
        raise ValueError("circuit_count must be a positive integer.")

    _positive_number("average_run_length", average_run_length)

    if (
        isinstance(conductors_per_circuit, bool)
        or not isinstance(conductors_per_circuit, int)
        or conductors_per_circuit <= 0
    ):
        raise ValueError("conductors_per_circuit must be a positive integer.")

    return _calculate_finite(
        "base_conductor_footage",
        lambda: circuit_count * average_run_length * conductors_per_circuit,
    )


def calculate_total_conductor_footage(*args, **kwargs):
    """Return conductor footage including a waste allowance.

    A waste_allowance of 0.10 represents 10%.
    """
    base_footage, waste_allowance = _get_inputs(
        args, kwargs, ("base_footage", "waste_allowance")
    )

    if (
        isinstance(base_footage, bool)
        or not isinstance(base_footage, (int, float))
        or base_footage < 0
    ):
        raise ValueError("base_footage must be finite and non-negative.")

    try:
        finite_base = math.isfinite(base_footage)
    except OverflowError:
        finite_base = False

    if not finite_base:
        raise ValueError("base_footage must be finite and non-negative.")

    if (
        isinstance(waste_allowance, bool)
        or not isinstance(waste_allowance, (int, float))
    ):
        raise ValueError("waste_allowance must be between 0 and 1.")

    try:
        valid_waste = (
            math.isfinite(waste_allowance)
            and 0 <= waste_allowance <= 1
        )
    except OverflowError:
        valid_waste = False

    if not valid_waste:
        raise ValueError("waste_allowance must be between 0 and 1.")

    return _calculate_finite(
        "total_conductor_footage",
        lambda: base_footage * (1 + waste_allowance),
    )
