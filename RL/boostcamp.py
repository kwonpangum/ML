import sympy as sym
from sympy.abc import x, y

g = x**2 + 2*x*y + 3*y**2
f = sym.diff(sym.poly(g), x)
f_1 = sym.diff(sym.poly(g), y)
print(f)
print(f_1)


