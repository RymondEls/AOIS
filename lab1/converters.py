from globals import *

def decimal_to_binary(decimal_number):
    if decimal_number == 0:
        return "0"
    decimal_number = -decimal_number if decimal_number < 0 else decimal_number
    binary = ""
    while decimal_number != 0:
        binary = ("1" if (decimal_number & 1) else "0") + binary
        decimal_number >>= 1
    return binary

def binary_to_decimal(binary):
    result = 0
    power = 0
    for bit in reversed(binary):
        if bit == "1":
            result += 1 << power
        power += 1
    return result

def decimal_to_signed_magnitude(decimal_number, bits=BIT_LENGTH_DEFAULT):
    if decimal_number >= 0:
        binary = decimal_to_binary(decimal_number)
        return "0" * (bits - len(binary)) + binary
    else:
        binary = decimal_to_binary(-decimal_number)
        binary = "0" * (bits - 1 - len(binary)) + binary
        return "1" + binary

def decimal_to_1s_complement(decimal_number, bits=BIT_LENGTH_DEFAULT):
    if decimal_number >= 0:
        binary = decimal_to_binary(decimal_number)
        return "0" * (bits - len(binary)) + binary
    else:
        binary = decimal_to_binary(-decimal_number)
        binary = "0" * (bits - 1 - len(binary)) + binary
        complement = ""
        for bit in binary:
            complement += "1" if bit == "0" else "0"
        return "1" + complement

def decimal_to_2s_complement(decimal_number, bits=BIT_LENGTH_DEFAULT):
    if decimal_number >= 0:
        binary = decimal_to_binary(decimal_number)
        return "0" * (bits - len(binary)) + binary
    else:
        binary = decimal_to_binary(-decimal_number)
        binary = "0" * (bits - len(binary)) + binary

        complement = ""
        for bit in binary:
            complement += "1" if bit == "0" else "0"

        result = ""
        carry = 1
        for bit in reversed(complement):
            total = carry + (1 if bit == "1" else 0)
            result = ("1" if total & 1 else "0") + result
            carry = total >> 1
        return result
    
def binary_to_decimal_2s_complement(binary):
    if binary[0] == "0": 
        return binary_to_decimal(binary)
    else:  
        inverted = ""
        for bit in binary:
            inverted += "1" if bit == "0" else "0"

        result = ""
        carry = 1
        for bit in reversed(inverted):
            total = carry + (1 if bit == "1" else 0)
            result = ("1" if (total & 1) else "0") + result
            carry = total >> 1
        return -binary_to_decimal(result)

def binary_to_decimal_signed_magnitude(binary):
    if binary[0] == "0": 
        return binary_to_decimal(binary[1:])
    else: 
        return -binary_to_decimal(binary[1:])
    
def decimal_to_ieee754(number):
    if number == 0:
        return IEEE754_ZERO

    sign = "0" if number > 0 else "1"
    number = -number if number < 0 else number

    int_part = number // 1 
    if int_part != number: 
        int_part = int_part - (int_part % 1) 
    frac_part = number - int_part

    int_binary = ""
    if int_part == 0:
        int_binary = "0"
    else:
        while int_part > 0:
            int_binary = ("1" if int_part % 2 == 1 else "0") + int_binary
            int_part = int_part // 2

    frac_binary = ""
    while frac_part != 0:
        frac_part *= 2
        bit = 1 if frac_part >= 1 else 0
        frac_binary += "1" if bit else "0"
        frac_part -= bit

    if int_binary != "0":
        exponent = len(int_binary) - 1
        mantissa = int_binary[1:] + frac_binary
    else:
        first_one = -1
        for i in range(len(frac_binary)):
            if frac_binary[i] == "1":
                first_one = i
                break
        if first_one == -1:
            return IEEE754_ZERO
        exponent = -(first_one + 1)
        mantissa = frac_binary[first_one + 1:]

    exponent += IEEE754_BIAS
    exponent_binary = ""
    for _ in range(IEEE754_EXPONENT_LENGTH):
        exponent_binary = ("1" if exponent % 2 == 1 else "0") + exponent_binary
        exponent = exponent // 2

    mantissa = mantissa[:IEEE754_SIGNIFICAND_LENGTH]
    mantissa = mantissa + "0" * (IEEE754_SIGNIFICAND_LENGTH - len(mantissa))

    ieee754 = sign + exponent_binary + mantissa
    return ieee754

def ieee754_to_decimal(ieee754):
    if len(ieee754) != IEEE754_TOTAL_BITS:
        return 0.0
    if ieee754 == IEEE754_ZERO:
        return 0.0
    
    sign = -1 if ieee754[0] == "1" else 1
    exponent_binary = ieee754[1:IEEE754_EXPONENT_LENGTH + 1]
    mantissa_binary = ieee754[IEEE754_EXPONENT_LENGTH + 1:IEEE754_TOTAL_BITS]

    exponent = 0
    for i in range(IEEE754_EXPONENT_LENGTH):
        exponent += (1 if exponent_binary[i] == "1" else 0) * (1 << (IEEE754_EXPONENT_LENGTH - 1 - i))
    exponent -= IEEE754_BIAS
    
    mantissa = 1.0
    for i in range(IEEE754_SIGNIFICAND_LENGTH):
        mantissa += (1 if mantissa_binary[i] == "1" else 0) * (1.0 / (1 << (i + 1)))
    
    # Используем возведение в степень вместо сдвига
    number = sign * mantissa * (2 ** exponent)
    return number