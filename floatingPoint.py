import re


def fp_bin_dict(d):
    return fp_bin(f"{d['exp_sign']}{d['mantissa_sign']}{d['exp_bits']}{d['mantissa_bits']}",
                  exp_sign=0,
                  mantissa_sign=1,
                  exp_bits=(2, 2 + len(d['exp_bits'])),
                  mantissa_bits=(2 + len(d['exp_bits']), 2 + len(d['exp_bits']) + len(d['mantissa_bits'])))


def fp_bin(word, exp_sign, exp_bits, mantissa_sign, mantissa_bits):
    """
    This method converts a floating-point representation into something understandable.

    :param str word: floating-point string representation
    :param int exp_sign: bit index for exponent sign
    :param tuple exp_bits: bit index range which represent the exponent magnitude
    :param int mantissa_sign: bit index for mantissa sign
    :param tuple mantissa_bits: bit index range which represent the mantissa magnitude

    :return: a dictionary containing information about the binary representation:
             exponent sign, exponent binary, mantissa sign, mantissa binary, decimal value
    :rtype: dict
    """
    pattern = re.compile(r"^[01]+$")
    if not pattern.match(word):
        raise ValueError("Word must be composed of 0's and 1's.")

    e_sign = word[exp_sign]
    m_sign = word[mantissa_sign]

    e_bits = word[exp_bits[0]: exp_bits[1]]
    m_bits = word[mantissa_bits[0]: mantissa_bits[1]]

    if e_sign == '1':
        binary = f".{'0'*(bin_val(e_bits) - 1)}1{word[mantissa_bits[0]: mantissa_bits[1]]}"
    else:
        e_dec = bin_val(e_bits)
        binary = f"1{m_bits[0: e_dec]}.{m_bits[e_dec:]}"

    return {'exponent_sign': e_sign,
            'exponent_bits': e_bits,
            'mantissa_sign': m_sign,
            'm_bits': m_bits,
            'binary': binary,
            'decimal_value': bin_dec(binary)}


def bin_val(bits, is_dec=False):
    s = 0

    order = enumerate(bits if is_dec else reversed(bits), 1 if is_dec else 0)

    for i, b in order:
       s += int(b) * 2**(-1*i if is_dec else i)

    return s


def bin_dec(s):
    if '.' in s:
        integer, fractal = s.split('.')
    else:
        integer, fractal = s, '0'

    return bin_val(integer) + bin_val(fractal, is_dec=True)


if __name__ == '__main__':
    word = '010101010101'

    res = fp_bin(word, mantissa_sign=0, exp_sign=1, mantissa_bits=(2, 8), exp_bits=(8, 12))

    print(f"({word})_2 = ({res['decimal_value']})_10")


