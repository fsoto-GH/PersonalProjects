from math import gcd, prod


def lagrange_interpolation_str(points):
    # used to store the entire string
    res = []

    for i, point in enumerate(points):
        # perform denominator multiplication to simplify
        denom = 1
        # this stores the current L_x iterate
        r = []
        # do the L_x if numerator is not 0
        # do not include coefficients of zero
        if point[1] != 0:
            for j in range(len(points)):
                if i != j:
                    # part of denominator simplification
                    denom *= (point[0] - points[j][0])
                    # determine the sign of the difference (flipped)
                    sign = number_sign(-points[j][0])
                    # for the numerator
                    r.append(f"(x{sign}{abs(points[j][0])})")
            # put the coefficient for the current iteration (as reduced fraction)
            coeff, a, _ = reduce_fract(abs(point[1]), abs(denom))
            # compose L_k(x) as a whole
            res.append(f"{number_sign(denom * point[1])}({coeff})" + '*'.join(r))

    return ''.join(res).lstrip('+')


def lagrange_interpolation_latex(points):
    """ This method is the same as 'lagrange_interpolation_str' but compatible with LaTex."""
    res = []
    for i, point in enumerate(points):
        denom = 1
        r = []

        # do not include coefficients of zero
        if point[1] != 0:
            for j in range(len(points)):
                if i != j:
                    sign = number_sign(points[j][0] * -1)
                    r.append(f"\\left(x{sign}{abs(points[j][0])}\\right)")
                    denom *= (point[0]-points[j][0])
            *_, a, b = reduce_fract(abs(point[1]), abs(denom))

            res.append(f"{number_sign(denom * point[1])}\\left(\\frac{{{a}}}{{{b}}}\\right)" + ''.join(r))

    return ''.join(res).lstrip('+')


def lagrange_interpolation_funct(points: list[tuple[int, int]]):
    """ This method is the same as 'lagrange_interpolation_str' but compatible with LaTex."""
    res = []
    for i, point in enumerate(points):
        denom = 1
        r = []
        if point[1] != 0:
            for j in range(len(points)):
                if i != j:
                    # assign variable because not doing so is... well weird... SO MANY HOURS SPENT ON THAT!
                    # that is, it stores the value of j and does reference evaluation.
                    r.append(lambda x, y=points[j][0]: x - y)
                    denom *= (point[0]-points[j][0])

            res.append(lambda x, tr=tuple(r), num=point[1], den=denom: (num / den * prod(map(lambda _r: _r(x), tr))))

    return lambda x: sum(f(x) for f in res)


def reduce_fract(a, b):
    common = gcd(a, b)
    return f"{a // common}/{b // common}", a // common, b // common


def number_sign(exprs):
    return '-' if exprs < 0 else '+'


if __name__ == '__main__':
    points = [(2, 1), (3, 2), (-1, 3), (4, 4), (7, 5), (10, 22), (17, -10), (19, -1), (24, -1), (50, 0)]
    print(lagrange_interpolation_latex(points))
    # print(lagrange_interpolation_latex(points))
    # print(lagrange_interpolation_str(points))

    p = lagrange_interpolation_funct(points)
    print(p(1))

