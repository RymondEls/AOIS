from converters import *
from globals import *

def add_binary(bin1, bin2, bits=BIT_LENGTH_DEFAULT):
    carry = 0
    result = ""
    bin1 = "0" * (bits - len(bin1)) + bin1
    bin2 = "0" * (bits - len(bin2)) + bin2
    
    for i in range(bits - 1, -1, -1):
        bit_sum = carry
        bit_sum += 1 if bin1[i] == "1" else 0
        bit_sum += 1 if bin2[i] == "1" else 0
        result = ("1" if (bit_sum & 1) else "0") + result
        carry = bit_sum >> 1
    return result

def add_2s_complement(num1, num2, bits=BIT_LENGTH_DEFAULT):
    bin1 = (decimal_to_binary(num1) if num1 >= 0 else decimal_to_2s_complement(num1, bits))
    bin1 = "0" * (bits - len(bin1)) + bin1
    bin2 = (decimal_to_binary(num2) if num2 >= 0 else decimal_to_2s_complement(num2, bits))
    bin2 = "0" * (bits - len(bin2)) + bin2
    result_binary = add_binary(bin1, bin2, bits)
    result_decimal = binary_to_decimal_2s_complement(result_binary)
    return result_binary, result_decimal

def subtract_2s_complement(num1, num2, bits=BIT_LENGTH_DEFAULT):
    bin1 = decimal_to_2s_complement(num1, bits)
    bin2 = decimal_to_2s_complement(-num2, bits)
    result_binary = add_binary(bin1, bin2, bits)
    result_decimal = binary_to_decimal_2s_complement(result_binary)
    return result_binary, result_decimal

def multiply_signed_magnitude(num1, num2, bits=BIT_LENGTH_DEFAULT):
    sign = 1 if (num1 >= 0) == (num2 >= 0) else -1

    abs_num1 = abs(num1)
    abs_num2 = abs(num2)

    bin1 = decimal_to_binary(abs_num1)
    bin1 = "0" * (bits - len(bin1)) + bin1
    bin2 = decimal_to_binary(abs_num2)
    bin2 = "0" * (bits - len(bin2)) + bin2

    result = 0
    for i in range(bits - 1, -1, -1):
        if bin2[i] == "1":
            shifted = binary_to_decimal(bin1) << (bits - 1 - i)
            result += shifted

    result_binary = decimal_to_binary(result)

    if len(result_binary) > bits:
        result_binary = result_binary[-bits:]
    else:
        result_binary = "0" * (bits - len(result_binary)) + result_binary

    if sign == -1:
        result_binary = "1" + result_binary[1:] 
    else:
        result_binary = "0" + result_binary[1:] 

    result_decimal = result if sign == 1 else -result
    return result_binary, result_decimal

def divide_signed_magnitude(num1, num2, bits=BIT_LENGTH_DEFAULT, precision=FRACTIONAL_PRECISION):
    if num2 == 0:
        return "Division by zero", None
        
    sign = 1 if (num1 >= 0) == (num2 >= 0) else -1
    abs_num1 = num1 if num1 >= 0 else -num1
    abs_num2 = num2 if num2 >= 0 else -num2
    
    quotient = 0
    while abs_num1 >= abs_num2:
        abs_num1 -= abs_num2
        quotient += 1
    
    bin_integer = decimal_to_binary(quotient)
    bin_fraction = ""
    remainder = abs_num1
    for _ in range(precision):
        remainder <<= 1
        bit = 1 if remainder >= abs_num2 else 0
        bin_fraction = bin_fraction + ("1" if bit else "0")
        if bit:
            remainder -= abs_num2
            
    result_binary = bin_integer + "." + bin_fraction
    result_decimal = quotient
    fractional = 0
    fraction_power = -1
    for bit in bin_fraction:
        if bit == "1":
            fractional += 2 ** fraction_power
        fraction_power -= 1
    result_decimal += fractional
    if sign == -1:
        result_decimal = -result_decimal
        
    return result_binary, result_decimal

def add_ieee754(num1, num2):
    if num1 == 0 and num2 == 0:
        return IEEE754_ZERO

    ieee1 = decimal_to_ieee754(num1)
    ieee2 = decimal_to_ieee754(num2)

    sign1 = -1 if ieee1[0] == "1" else 1
    exponent1 = 0
    for i in range(IEEE754_EXPONENT_LENGTH):
        exponent1 += (1 if ieee1[1 + i] == "1" else 0) * (1 << (IEEE754_EXPONENT_LENGTH - 1 - i))
    exponent1 -= IEEE754_BIAS
    
    mantissa1 = 1.0
    for i in range(IEEE754_SIGNIFICAND_LENGTH):
        mantissa1 += (1 if ieee1[9 + i] == "1" else 0) * (1.0 / (1 << (i + 1)))
    
    sign2 = -1 if ieee2[0] == "1" else 1
    exponent2 = 0
    for i in range(IEEE754_EXPONENT_LENGTH):
        exponent2 += (1 if ieee2[1 + i] == "1" else 0) * (1 << (IEEE754_EXPONENT_LENGTH - 1 - i))
    exponent2 -= IEEE754_BIAS
    
    mantissa2 = 1.0
    for i in range(IEEE754_SIGNIFICAND_LENGTH):
        mantissa2 += (1 if ieee2[9 + i] == "1" else 0) * (1.0 / (1 << (i + 1)))

    if exponent1 > exponent2:
        mantissa2 /= (1 << (exponent1 - exponent2))
        exponent2 = exponent1
    else:
        mantissa1 /= (1 << (exponent2 - exponent1))
        exponent1 = exponent2

    result_mantissa = sign1 * mantissa1 + sign2 * mantissa2
    result_sign = "1" if result_mantissa < 0 else "0"
    result_mantissa = abs(result_mantissa)

    if result_mantissa == 0:
        return IEEE754_ZERO

    while result_mantissa >= 2.0:
        result_mantissa /= 2.0
        exponent1 += 1
    while result_mantissa < 1.0:
        result_mantissa *= 2.0
        exponent1 -= 1

    exponent_binary = ""
    exponent1 += IEEE754_BIAS
    for _ in range(IEEE754_EXPONENT_LENGTH):
        exponent_binary = ("1" if exponent1 & 1 else "0") + exponent_binary
        exponent1 = exponent1 >> 1
    
    mantissa_binary = ""
    result_mantissa -= 1.0
    for _ in range(IEEE754_SIGNIFICAND_LENGTH):
        result_mantissa *= 2
        bit = 1 if result_mantissa >= 1 else 0
        mantissa_binary += "1" if bit else "0"
        result_mantissa -= bit

    result_ieee754 = result_sign + exponent_binary + mantissa_binary
    return result_ieee754


