import re
from dec_bin import dec_bin_int_s

def fp_bin_dict(d):
    return fp_dec(f"{d['exp_sign']}{d['mantissa_sign']}{d['exp_bits']}{d['mantissa_bits']}",
                  exp_sign=0,
                  mantissa_sign=1,
                  exp_bits=(2, 2 + len(d['exp_bits'])),
                  mantissa_bits=(2 + len(d['exp_bits']), 2 + len(d['exp_bits']) + len(d['mantissa_bits'])))


def fp_dec(word, exp_sign, exp_bits, mantissa_sign, mantissa_bits):
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

    if max(exp_sign, *exp_bits, mantissa_sign, *mantissa_bits) != len(word):
        raise IndexError('The described bits do not match the dimension of the word.')

    e_sign = word[exp_sign]
    m_sign = word[mantissa_sign]

    e_bits = word[exp_bits[0]: exp_bits[1]]
    m_bits = word[mantissa_bits[0]: mantissa_bits[1]]

    if e_sign == '1':
        binary = f".{'0'*(bin_val(e_bits) - 1)}1{word[mantissa_bits[0]: mantissa_bits[1]]}"
    else:
        e_dec = bin_val(e_bits)
        # account for bit len not being enough
        binary = f"1{m_bits[: e_dec]}{'0'*(e_dec - len(m_bits)) if e_dec > len(m_bits) else ''}.{m_bits[e_dec:]}"

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


def dec_bin(s):
    bits = []

    while s > 0:
        bits.append('1' if s % 2 else '0')
        s //= 2

    return ''.join(reversed(bits))


def dec_fp(dec, exp_sign, exp_bits, mantissa_sign, mantissa_bits):
    """
    This method converts a decimal into a corresponding floating point representation.

    :param str dec: p
    :param int exp_sign:
    :param tuple exp_bits:
    :param int mantissa_sign:
    :param tuple mantissa_bits:
    :return:
    """
    pattern = re.compile(r"^(-)?[01]+$")
    is_neg = dec[0] == '-'

    if is_neg:
        dec = dec[1:]

    if '.' in dec:
        d_index = dec.find('.')
        integer, fractal = float(dec[0: d_index]), float(dec[d_index:])
    else:
        integer, fractal = float(dec), 0

    d_bits = dec_bin_int_s(fractal)

    integer_bin = dec_bin(integer)
    fractal_bin = d_bits['binary']
    binary = integer_bin + fractal_bin[1:]

    res = f"{1 if is_neg else 0}"

    return {'integer': integer_bin,
            'fractal': fractal_bin,
            'binary': binary}


if __name__ == '__main__':
    # word = '010101010101'
    #
    # res = fp_dec(word, mantissa_sign=0, exp_sign=1, mantissa_bits=(2, 8), exp_bits=(8, 12))
    # print(res)
    #
    # print(f"({word})_2 = ({res['decimal_value']})_10")

    # word = '0010010000100110'
    #
    # res = fp_dec(word, mantissa_sign=0, exp_sign=1, mantissa_bits=(2, 12), exp_bits=(12, 16))
    # print(res)
    #
    # print(f"({word})_2 = ({res['decimal_value']})_10")

    word = '010101010101'

    res = fp_dec(word, mantissa_sign=0, exp_sign=1, mantissa_bits=(2, 8), exp_bits=(8, 12))
    print(res)

    print(f"({word})_2 = ({res['decimal_value']})_10")

    # print(dec_fp('40', mantissa_sign=0, exp_sign=1, mantissa_bits=(2, 6), exp_bits=(6, 9)))


