"""Exact standard-library checks for worker_stronger_bound.md."""
from fractions import Fraction as F
from math import comb


def add(*polys):
    out = {}
    for poly in polys:
        for ab, val in poly.items():
            out[ab] = out.get(ab, F(0)) + val
    return {ab: val for ab, val in out.items() if val}


def scale(poly, value):
    return {ab: val * value for ab, val in poly.items()}


def mul(p, q):
    out = {}
    for (a, b), val in p.items():
        for (i, j), other in q.items():
            ab = a + i, b + j
            out[ab] = out.get(ab, F(0)) + val * other
    return {ab: val for ab, val in out.items() if val}


def power(poly, n):
    out = {(0, 0): F(1)}
    for _ in range(n):
        out = mul(out, poly)
    return out


one = {(0, 0): F(1)}
c = {(1, 0): F(1)}
s = {(0, 1): F(1)}
P = add(one, scale(power(c, 2), 2), scale(mul(c, s), -3),
        scale(mul(power(c, 2), power(s, 2)), -3),
        mul(mul(c, add(scale(one, 2), power(c, 2))), power(s, 3)))
E = add(mul(mul(add(c, s), add(one, scale(mul(c, s), -1))), P),
        scale(mul(mul(add(one, scale(power(c, 2), -1)), s),
                  power(add(one, mul(c, s)), 3)), -1))
assert E == {(1, 0): 1, (1, 2): -7, (1, 4): 2,
             (2, 1): -1, (2, 3): -1, (2, 5): -2,
             (3, 0): 2, (3, 2): 1, (3, 4): 1,
             (4, 1): -2, (4, 3): 7, (4, 5): -1}

# Substitute c=(2+u)/3 and s=12v/25 in the power basis.
q = {}
for (a, b), val in E.items():
    for i in range(a + 1):
        q[i, b] = q.get((i, b), F(0)) + (
            val * comb(a, i) * F(2, 3) ** (a-i)
            * F(1, 3) ** i * F(12, 25) ** b)

# Power-to-Bernstein identity: t^a=sum_i>=a C(i,a)/C(n,a) b_i^n(t).
bernstein = {(i, j): sum(val * F(comb(i, a), comb(4, a))
                        * F(comb(j, b), comb(5, b))
                        for (a, b), val in q.items() if a <= i and b <= j)
             for i in range(5) for j in range(6)}
denominator = 1054687500
table = [
    [1328125000, 1243125000, 1051925000, 765469000, 412948680, 12607112],
    [1650390625, 1534140625, 1300215625, 966327625, 571546705, 138478561],
    [2050781250, 1891406250, 1603781250, 1216202250, 781848450, 330011178],
    [2548828125, 2329453125, 1972378125, 1522315125, 1052902845, 604001061],
    [3164062500, 2860312500, 2410762500, 1885396500, 1387790820, 974492532],
]
for (i, j), val in bernstein.items():
    assert val == F(table[i][j], denominator)
    assert val > 0
assert min(bernstein.values()) == F(3151778, 263671875)

# Re-expand the Bernstein certificate independently and compare power coefficients.
expanded = {}
for (i, j), val in bernstein.items():
    for a in range(5-i):
        for b in range(6-j):
            ab = i+a, j+b
            expanded[ab] = expanded.get(ab, F(0)) + (
                val * comb(4, i) * comb(5, j) * comb(4-i, a)
                * comb(5-j, b) * (-1) ** (a+b))
assert {ab: val for ab, val in expanded.items() if val} == q

# Exact C2-only obstruction: all comparisons are rational after squaring.
assert F(7939, 1000) ** 2 < F(68900, 1093)
assert F(4624, 1000) ** 2 > F(2116707500, 99026893)
assert F(1732, 1000) ** 2 < 3
q_lower = (F(3, 4) * F(7939, 1000) - F(4624, 1000)
           - F(29700000, 9150701) /
           (F(200, 101) + F(100, 301) * F(1732, 1000)))
assert q_lower > F(3, 50)
print('PASS: polynomial identities, 30 positive Bernstein coefficients,')
print('      independent certificate expansion, and C2-only obstruction.')
print('Minimum Bernstein coefficient:', min(bernstein.values()))
print('Exact lower bound for witness Q:', q_lower)
