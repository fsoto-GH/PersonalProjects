def false_position(f, a, b, t=10**-4, i=1_000):
    if a >= b:
        raise ValueError(f"{a} < {b} is not valid.")

    iters = {}
    m = (a * f(b) - b * f(a)) / (f(b) - f(a))
    c = 1
    iters[c] = {'L': a,
                'U': b,
                'M': m}
    while not(f(m) == 0 or -t <= f(m) <= t) and c != i:
        if f(a)*f(m) < 0:
            b = m
        elif f(m)*f(b) < 0:
            a = m
        m = (a * f(b) - b * f(a)) / (f(b) - f(a))
        c += 1
        iters[c] = {'L': a,
                    'U': b,
                    'M': m}

    return m, iters


if __name__ == '__main__':
    f = lambda x: x**3 - 0.165*x**2 + 3.993*10**-4
    a, b, = 0, 0.11

    res, iters = false_position(f, a, b, t=0.00001)

    for k, v in iters.items():
        print(k, v)
