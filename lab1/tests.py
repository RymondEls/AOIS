import unittest
from converters import *
from binary_operations import *

class TestConverters(unittest.TestCase):

    def test_decimal_to_binary(self):
        self.assertEqual(decimal_to_binary(0), "0")
        self.assertEqual(decimal_to_binary(5), "101")
        self.assertEqual(decimal_to_binary(10), "1010")
        self.assertEqual(decimal_to_binary(255), "11111111")

    def test_binary_to_decimal(self):
        self.assertEqual(binary_to_decimal("0"), 0)
        self.assertEqual(binary_to_decimal("101"), 5)
        self.assertEqual(binary_to_decimal("1010"), 10)
        self.assertEqual(binary_to_decimal("11111111"), 255)

    def test_decimal_to_signed_magnitude(self):
        self.assertEqual(decimal_to_signed_magnitude(5), "0000000000000101")
        self.assertEqual(decimal_to_signed_magnitude(-5), "1000000000000101")
        self.assertEqual(decimal_to_signed_magnitude(0), "0000000000000000")

    def test_decimal_to_1s_complement(self):
        self.assertEqual(decimal_to_1s_complement(5), "0000000000000101")
        self.assertEqual(decimal_to_1s_complement(-5), "1111111111111010")
        self.assertEqual(decimal_to_1s_complement(0), "0000000000000000")

    def test_decimal_to_2s_complement(self):
        self.assertEqual(decimal_to_2s_complement(5), "0000000000000101")
        self.assertEqual(decimal_to_2s_complement(-5), "1111111111111011")
        self.assertEqual(decimal_to_2s_complement(0), "0000000000000000")

    def test_binary_to_decimal_2s_complement(self):
        self.assertEqual(binary_to_decimal_2s_complement("00000101"), 5)
        self.assertEqual(binary_to_decimal_2s_complement("11111011"), -5)
        self.assertEqual(binary_to_decimal_2s_complement("00000000"), 0)

    def test_decimal_to_ieee754(self):
        self.assertEqual(decimal_to_ieee754(0), IEEE754_ZERO)
        self.assertEqual(decimal_to_ieee754(1.0), "00111111100000000000000000000000")
        self.assertEqual(decimal_to_ieee754(-2.5), "11000000001000000000000000000000")

    def test_ieee754_to_decimal(self):
        self.assertEqual(ieee754_to_decimal(IEEE754_ZERO), 0.0)
        self.assertEqual(ieee754_to_decimal("00111111100000000000000000000000"), 1.0)
        self.assertEqual(ieee754_to_decimal("11000000001000000000000000000000"), -2.5)

class TestBinaryOperations(unittest.TestCase):

    def test_add_binary(self):
        self.assertEqual(add_binary("1010", "1100"), "0000000000010110")
        self.assertEqual(add_binary("1111", "0001"), "0000000000010000")
        self.assertEqual(add_binary("0000", "0000"), "0000000000000000")

    def test_add_2s_complement(self):
        self.assertEqual(add_2s_complement(5, 3), ("0000000000001000", 8))
        self.assertEqual(add_2s_complement(-5, -3), ("1111111111111000", -8))
        self.assertEqual(add_2s_complement(5, -3), ("0000000000000010", 2))

    def test_subtract_2s_complement(self):
        self.assertEqual(subtract_2s_complement(5, 3), ("0000000000000010", 2))
        self.assertEqual(subtract_2s_complement(-5, -3), ("1111111111111110", -2))
        self.assertEqual(subtract_2s_complement(5, -3), ("0000000000001000", 8))

    def test_multiply_signed_magnitude(self):
        self.assertEqual(multiply_signed_magnitude(5, 3), ("0000000000001111", 15))
        self.assertEqual(multiply_signed_magnitude(-5, 3), ("1000000000001111", -15))
        self.assertEqual(multiply_signed_magnitude(5, -3), ("1000000000001111", -15))

    def test_divide_signed_magnitude(self):
        self.assertEqual(divide_signed_magnitude(10, 2), ("101.00000", 5.0))
        self.assertEqual(divide_signed_magnitude(-10, 2), ("101.00000", -5.0))
        self.assertEqual(divide_signed_magnitude(10, 3), ("11.01010", 3.3125))

    def test_add_ieee754(self):
        self.assertEqual(add_ieee754(1.5, 2.5), "01000000100000000000000000000000")  # 4.0
        self.assertEqual(add_ieee754(-1.5, 2.5), "00111111100000000000000000000000")  # 1.0
        self.assertEqual(add_ieee754(0, 0), IEEE754_ZERO)  # 0.0

    def test_divide_by_zero(self):
        self.assertEqual(divide_signed_magnitude(10, 0), ("Division by zero", None))

    def test_ieee754_to_decimal_invalid_input(self):
        self.assertEqual(ieee754_to_decimal("0000000000000000000000000000000"), 0.0)  # Неправильная длина
        self.assertEqual(ieee754_to_decimal("invalid_input"), 0.0)  # Неправильный формат

if __name__ == "__main__":
    unittest.main()