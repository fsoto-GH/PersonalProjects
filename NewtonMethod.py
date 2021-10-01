def newton_method(f, f_p, x_0, t=10**-4, max_iters=1_000):
    x_n = x_0
    c = 1

    iters = {c: x_n}
    while not(f(x_n) == 0 or -t <= f(x_n) <= t):
        if f_p(x_n) == 0:
            break
        x_n = x_n - f(x_n) / f_p(x_n)
        c += 1
        iters[c] = x_n
    return x_n, iters


if __name__ == '__main__':
    f = lambda x: x**3 - x**2 - x - 1
    f_p = lambda x: 3*x**2 - 2*x - 1

    x_n, iters = newton_method(f, f_p, x_0=1.75)

    for k, v in iters.items():
        print(k, v)