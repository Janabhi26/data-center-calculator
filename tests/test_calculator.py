
import unittest
import math

from src.calculator import (
    calculate_total_rack_load,
    calculate_nominal_circuit_capacity,
    calculate_usable_circuit_capacity,
    calculate_required_circuits,
    calculate_base_conductor_footage,
    calculate_total_conductor_footage,
)


class TestDataCenterCalculator(unittest.TestCase):

    # End-to-end workflow: all six functions used together

    def test_complete_calculation_workflow(self):
        rack_count = 20
        load_per_rack_kva = 10
        voltage_v = 480
        breaker_rating_a = 30
        phase = "three_phase"
        loading_factor = 0.8
        average_run_length_ft = 100
        conductors_per_circuit = 4
        waste_allowance = 0.10

        total_load_kva = calculate_total_rack_load(
            rack_count, load_per_rack_kva
        )
        self.assertEqual(total_load_kva, 200)

        nominal_capacity_kva = calculate_nominal_circuit_capacity(
            voltage_v, breaker_rating_a, phase
        )
        self.assertAlmostEqual(nominal_capacity_kva, 24.94, places=2)

        usable_capacity_kva = calculate_usable_circuit_capacity(
            nominal_capacity_kva, loading_factor
        )
        self.assertAlmostEqual(usable_capacity_kva, 19.95, places=2)

        circuit_count = calculate_required_circuits(
            total_load_kva, usable_capacity_kva
        )
        self.assertEqual(circuit_count, 11)

        base_footage_ft = calculate_base_conductor_footage(
            circuit_count,
            average_run_length_ft,
            conductors_per_circuit,
        )
        self.assertEqual(base_footage_ft, 4400)

        total_footage_ft = calculate_total_conductor_footage(
            base_footage_ft, waste_allowance
        )
        self.assertAlmostEqual(total_footage_ft, 4840)

    # Normal calculation and expected-output tests

    def test_total_rack_load(self):
        self.assertEqual(calculate_total_rack_load(20, 10), 200)

    def test_total_rack_load_with_keywords(self):
        self.assertEqual(
            calculate_total_rack_load(
                rack_count=20,
                load_per_rack=10,
            ),
            200,
        )

    def test_nominal_single_phase_capacity_kva(self):
        result = calculate_nominal_circuit_capacity(
            230, 20, "single_phase"
        )
        self.assertAlmostEqual(result, 4.6, places=2)

    def test_nominal_three_phase_capacity_kva(self):
        result = calculate_nominal_circuit_capacity(
            480, 30, "three_phase"
        )
        self.assertAlmostEqual(result, 24.94, places=2)

    def test_usable_circuit_capacity_kva(self):
        result = calculate_usable_circuit_capacity(24.94, 0.8)
        self.assertAlmostEqual(result, 19.952, places=3)

    def test_required_circuits_exact_boundary(self):
        # Exactly 200 kVA / 20 kVA per circuit requires 10 circuits.
        self.assertEqual(calculate_required_circuits(200, 20), 10)

    def test_required_circuits_rounds_up(self):
        # A small excess over 10 circuits must require 11.
        self.assertEqual(calculate_required_circuits(200.01, 20), 11)

    def test_required_circuits_larger_load(self):
        self.assertEqual(calculate_required_circuits(201, 20), 11)

    def test_base_conductor_footage_in_feet(self):
        result = calculate_base_conductor_footage(11, 100, 4)
        self.assertEqual(result, 4400)

    def test_total_conductor_footage_with_ten_percent_waste(self):
        result = calculate_total_conductor_footage(4400, 0.10)
        self.assertAlmostEqual(result, 4840)

    # Keyword argument tests

    def test_all_remaining_functions_accept_keywords(self):
        self.assertAlmostEqual(
            calculate_nominal_circuit_capacity(
                voltage=480,
                breaker_rating=30,
                phase="three_phase",
            ),
            24.94,
            places=2,
        )

        self.assertAlmostEqual(
            calculate_usable_circuit_capacity(
                nominal_capacity=25,
                loading_factor=0.8,
            ),
            20,
        )

        self.assertEqual(
            calculate_required_circuits(
                total_load=201,
                usable_capacity=20,
            ),
            11,
        )

        self.assertEqual(
            calculate_base_conductor_footage(
                circuit_count=2,
                average_run_length=100,
                conductors_per_circuit=4,
            ),
            800,
        )

        self.assertAlmostEqual(
            calculate_total_conductor_footage(
                base_footage=800,
                waste_allowance=0.10,
            ),
            880,
        )

    # Boundary tests

    def test_loading_factor_at_one(self):
        self.assertAlmostEqual(
            calculate_usable_circuit_capacity(25, 1.0),
            25,
        )

    def test_zero_waste_allowance(self):
        self.assertAlmostEqual(
            calculate_total_conductor_footage(100, 0),
            100,
        )

    def test_maximum_waste_allowance(self):
        # The current implementation permits a waste allowance of 1.0 (100%).
        self.assertAlmostEqual(
            calculate_total_conductor_footage(100, 1.0),
            200,
        )

    def test_zero_base_footage_with_zero_waste(self):
        self.assertEqual(
            calculate_total_conductor_footage(0, 0),
            0,
        )

    # Invalid input tests

    def test_zero_rack_count_is_rejected(self):
        with self.assertRaises(ValueError):
            calculate_total_rack_load(0, 10)

    def test_negative_rack_load_is_rejected(self):
        with self.assertRaises(ValueError):
            calculate_total_rack_load(10, -5)

    def test_zero_rack_load_is_rejected(self):
        with self.assertRaises(ValueError):
            calculate_total_rack_load(10, 0)

    def test_invalid_phase_is_rejected(self):
        with self.assertRaises(ValueError):
            calculate_nominal_circuit_capacity(480, 30, "two_phase")

    def test_zero_voltage_is_rejected(self):
        with self.assertRaises(ValueError):
            calculate_nominal_circuit_capacity(0, 30, "three_phase")

    def test_loading_factor_above_one_is_rejected(self):
        with self.assertRaises(ValueError):
            calculate_usable_circuit_capacity(24.94, 1.2)

    def test_zero_loading_factor_is_rejected(self):
        with self.assertRaises(ValueError):
            calculate_usable_circuit_capacity(24.94, 0)

    def test_zero_usable_capacity_is_rejected(self):
        with self.assertRaises(ValueError):
            calculate_required_circuits(200, 0)

    def test_zero_total_load_is_rejected_for_circuit_count(self):
        with self.assertRaises(ValueError):
            calculate_required_circuits(0, 20)

    def test_zero_circuit_count_is_rejected(self):
        with self.assertRaises(ValueError):
            calculate_base_conductor_footage(0, 100, 4)

    def test_negative_waste_allowance_is_rejected(self):
        with self.assertRaises(ValueError):
            calculate_total_conductor_footage(4400, -0.1)

    def test_waste_allowance_above_one_is_rejected(self):
        with self.assertRaises(ValueError):
            calculate_total_conductor_footage(100, 1.01)

    def test_missing_keyword_arguments_are_rejected(self):
        with self.assertRaises(ValueError):
            calculate_total_rack_load(rack_count=20)

    def test_wrong_number_of_positional_arguments_is_rejected(self):
        with self.assertRaises(ValueError):
            calculate_total_rack_load(20)

    def test_mixed_positional_and_keyword_arguments_are_rejected(self):
        with self.assertRaises(ValueError):
            calculate_total_rack_load(20, load_per_rack=10)

    def test_boolean_rack_count_is_rejected(self):
        with self.assertRaises(ValueError):
            calculate_total_rack_load(True, 10)

    def test_nan_load_is_rejected(self):
        with self.assertRaises(ValueError):
            calculate_total_rack_load(10, math.nan)

    def test_infinite_voltage_is_rejected(self):
        with self.assertRaises(ValueError):
            calculate_nominal_circuit_capacity(
                math.inf, 30, "three_phase"
            )

    def test_boolean_capacity_is_rejected(self):
        with self.assertRaises(ValueError):
            calculate_required_circuits(200, True)

    def test_unexpected_keyword_argument_is_rejected(self):
        with self.assertRaises(ValueError):
            calculate_total_rack_load(
                rack_count=20,
                load_per_rack=10,
                unexpected_input=5,
            )


if __name__ == "__main__":
    unittest.main()
