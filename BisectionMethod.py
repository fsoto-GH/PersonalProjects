def bisection_method(f, a, b, t=10**-4, max_iters=1_000):
    if a >= b:
        raise ValueError(f"{a} < {b} is not valid.")

    iters = {}
    m = (a + b) / 2
    c = 1
    iters[c] = {'L': a,
                'U': b,
                'M': m}
    while not(f(m) == 0 or -t <= f(m) <= t) and c != max_iters:
        if f(m) == 0:
            break
        if f(a)*f(m) < 0:
            b = m
        elif f(m)*f(b) < 0:
            a = m
        m = (a + b) / 2
        c += 1
        iters[c] = {'L': a,
                    'U': b,
                    'M': m}

    return m, iters

