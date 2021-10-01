import math
from BisectionMethod import bisection_method
from FalsePosition import false_position
from NewtonMethod import newton_method

print('1A')
f = lambda x: math.sin(x) - 0.25
fp = lambda x: math.cos(x)
a = 0
b = math.pi / 2
x_0 = 0
t = 10**-4
max_iters = 5_000

print(f"\tf(x)=sin(x) - 0.25")
print("\t0 <= x <= pi/2")
print('\tBisection Method')

sol, iters = bisection_method(f, a, b, t=t, max_iters=max_iters)
for k, v in iters.items():
    print(f"{k:4}\t\t\n"
          f"\t\tL: {v['L']:<10.8f} ({f(v['L']):11.8f})\t\n"
          f"\t\tU: {v['U']:<10.8f} ({f(v['U']):11.8f})\t\n"
          f"\t\tM: {v['M']:<10.8f} ({f(v['M']):11.8f})")

sol, iters = false_position(f, a, b, t=t, max_iters=max_iters)
print('False Position')
for k, v in iters.items():
    print(f"{k:4}\t\t\n"
          f"\t\tL: {v['L']:<10.8f} ({f(v['L']):11.8f})\t\n"
          f"\t\tU: {v['U']:<10.8f} ({f(v['U']):11.8f})\t\n"
          f"\t\tM: {v['M']:<10.8f} ({f(v['M']):11.8f})")

print("Newton's Method")
sol, iters = newton_method(f, fp, x_0=x_0, t=t, max_iters=max_iters)
for k, v in iters.items():
    print(f"{k:4}\t\t\n"
          f"\t\tx: {v:10.8f} ({f(v):11.8f})\t")
