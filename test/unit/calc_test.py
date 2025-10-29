import unittest
from math import pow, sqrt, log10
from unittest.mock import patch
import pytest

from app.calc import Calculator, InvalidPermissions


def mocked_validation(*args, **kwargs):
    return True


def mocked_invalid_validation(*args, **kwargs):
    return False


@pytest.mark.unit
class TestCalculate(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()
        self.validUser = "user1"
        self.invalidUser = "user2"

    def test_add_method_returns_correct_result(self):
        self.assertEqual(4, self.calc.add(2, 2.0))
        self.assertEqual(0, self.calc.add(2, -2))
        self.assertEqual(0, self.calc.add(-2, 2))
        self.assertEqual(1, self.calc.add(1.0, 0))

    def test_add_method_fails_with_nan_parameter(self):
        self.assertRaises(TypeError, self.calc.add, "2", 2)
        self.assertRaises(TypeError, self.calc.add, 2, "2")
        self.assertRaises(TypeError, self.calc.add, "2", "2")
        self.assertRaises(TypeError, self.calc.add, None, 2)
        self.assertRaises(TypeError, self.calc.add, 2, None)
        self.assertRaises(TypeError, self.calc.add, object(), 2)
        self.assertRaises(TypeError, self.calc.add, 2, object())

    def test_substract_method_returns_correct_result(self):
        self.assertEqual(0, self.calc.substract(2.0, 2))
        self.assertEqual(4, self.calc.substract(2, -2))
        self.assertEqual(-4.2, self.calc.substract(-2.1, 2.1))
        self.assertEqual(1, self.calc.substract(1, 0))

    def test_substract_method_fails_with_nan_parameters(self):
        self.assertRaises(TypeError, self.calc.substract, "a", 1)
        self.assertRaises(TypeError, self.calc.substract, 1, None)


    @patch('app.util.validate_permissions', side_effect=mocked_validation, create=True)
    def test_multiply_method_returns_correct_result(self, _validate_permissions):
        self.assertEqual(4, self.calc.multiply(2, 2, self.validUser))
        self.assertEqual(0, self.calc.multiply(1, 0, self.validUser))
        self.assertEqual(0, self.calc.multiply(-1, 0, self.validUser))
        self.assertEqual(-2, self.calc.multiply(-1, 2, self.validUser))
        self.assertEqual(-3, self.calc.multiply(-1.5, 2.0, self.validUser))

    @patch('app.util.validate_permissions', side_effect=mocked_validation, create=True)
    def test_multiply_method_fails_with_nan_parameters(self, _validate_permissions):
        self.assertRaises(TypeError, self.calc.multiply, "2", 2, self.invalidUser)
        self.assertRaises(TypeError, self.calc.multiply, 2, "2", self.invalidUser)
        self.assertRaises(TypeError, self.calc.multiply, None, 2, self.invalidUser)
        self.assertRaises(TypeError, self.calc.multiply, 2, None, self.invalidUser)
        self.assertRaises(TypeError, self.calc.multiply, object(), 2, self.invalidUser)
        self.assertRaises(TypeError, self.calc.multiply, 2, object(), self.invalidUser)

    @patch('app.util.validate_permissions', side_effect=mocked_invalid_validation, create=True)
    def test_multiply_method_raises_invalid_permissions(self, _validate_permissions):
        with self.assertRaises(InvalidPermissions):
            self.calc.multiply(2, 3, self.invalidUser)

    def test_divide_method_returns_correct_result(self):
        self.assertEqual(1, self.calc.divide(2, 2))
        self.assertEqual(1.5, self.calc.divide(3, 2))
        self.assertEqual(3.25, self.calc.divide(6.5, 2))

    def test_divide_method_fails_with_nan_parameter(self):
        self.assertRaises(TypeError, self.calc.divide, "2", 2)
        self.assertRaises(TypeError, self.calc.divide, 2, "2")
        self.assertRaises(TypeError, self.calc.divide, "2", "2")

    def test_divide_method_fails_with_division_by_zero(self):
        self.assertRaises(TypeError, self.calc.divide, 2, 0)
        self.assertRaises(TypeError, self.calc.divide, 2, -0)
        self.assertRaises(TypeError, self.calc.divide, 0.0, 0.0)
        self.assertRaises(TypeError, self.calc.divide, "0", 0)

    def test_power_method_returns_correct_result(self):
        self.assertEqual(8, self.calc.power(2, 3))
        self.assertEqual(1, self.calc.power(5, 0))
        self.assertEqual(0.25, self.calc.power(2, -2))
        self.assertEqual(pow(2, 4.2), self.calc.power(2, 4.2))

    def test_power_method_fails_with_nan_parameter(self):
        self.assertRaises(TypeError, self.calc.power, "2", 2)
        self.assertRaises(TypeError, self.calc.power, 2, None)

    def test_sqrt_method_returns_correct_result(self):
        self.assertEqual(3, self.calc.sqrt(9))
        self.assertEqual(0, self.calc.sqrt(0))
        self.assertEqual(sqrt(5.23), self.calc.sqrt(5.23))

    def test_sqrt_method_fails_with_negative(self):
        self.assertRaises(TypeError, self.calc.sqrt, -9)
        self.assertRaises(TypeError, self.calc.sqrt, -4)

    def test_log10_method_returns_correct_result(self):
        self.assertAlmostEqual(1, self.calc.log10(10))
        self.assertAlmostEqual(2, self.calc.log10(100))
        self.assertAlmostEqual(log10(54.2), self.calc.log10(54.2))

    def test_log10_method_fails_with_nan_parameter(self):
        self.assertRaises(TypeError, self.calc.log10, 0)
        self.assertRaises(TypeError, self.calc.log10, -1)
        self.assertRaises(TypeError, self.calc.log10, "10")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
