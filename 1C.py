import math
from BisectionMethod import bisection_method

print('1B')
f = lambda x: math.log(x) - 10

sol, iters = bisection_method(f, 0, math.pi / 2)

for k, v in iters.items():
    print(f"{k:4}\t\n"
          f"\tL: {v['L']:<10.8f} ({f(v['L']):10.8f})\t\n"
          f"\tU: {v['U']:<10.8f} ({f(v['U']):10.8f})\t\n"
          f"\tM: {v['M']:<10.8f} ({f(v['M']):10.8f})")