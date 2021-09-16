def dec_bin_int_s(a: float, terms=50, do_print=False):
    """
    This takes a decimal (fractal) number and converts it into binary.
    To avoid floating-point inaccuracy, the decimal is converted into an integer
    according to the decimal places.

    :param float a: the fractal number
    :param int terms: number of bits to compute (if enough)
    :param  bool do_print: whether to display the computations
    :return: a dictionary that contains:
                whether the binary repeats itself within the given terms,
                the actual binary representation as a string, and
                details about the period--period, start index, end index
    :rtype: dict
    """
    _t = terms
    repeats = False
    per_d = {'period': 0,
             'start': 0,
             'end': 0}
    seen = {}
    bits = []

    # num of decimal places
    ex = len(str(a)) - 2

    # initialize the adjusted value
    b = a * 10**ex
    b *= 2

    # for the initial decimal and skip first stage
    if terms is not None:
        terms -= 2

    while b > 0:
        if b >= 10**ex:
            bits.append(1)
            if do_print:
                print(f"{(b / 10**ex)} 1")
        else:
            bits.append(0)
            if do_print:
                print(f"{(b / 10**ex)} 0")

        # check if value has been seen before
        # if it has, then the value repeats
        if b in seen and not repeats:
            repeats = True
            per_d.update({'period': seen[b] - terms,
                          'start': _t - seen[b] - 1,
                         'end': _t - 1 - terms})
        else:
            seen[b] = terms

        b = b % 10**ex
        b *= 2

        if terms is not None:
            if terms < 0:
                break
            else:
                terms -= 1

    return {'repeats': repeats,
            'binary': '0.'+''.join(str(bit) for bit in bits),
            'period': per_d}


if __name__ == '__main__':
    does_repeat, in_binary, rep_period = dec_bin_int_s(0.6667, terms=505, do_print=True).values()

    print(f'Repeats: {does_repeat}')
    print(f'Period Details: {rep_period}')
    print(f'Binary: {in_binary}')
