#!/usr/bin/env python3
"""Independent exact reconstruction for the frozen Q9 proof.

Unlike the submitted checker, this first expands the displayed E in c,s,w,
then performs homogeneous substitution in w. Affine changes use Horner
evaluation, and Bernstein coefficients use rational Pascal addition tables.
No imports of the candidate's polynomial class or arithmetic routines occur.
"""
from collections import defaultdict
from fractions import Fraction
from math import comb
from pathlib import Path
import contextlib
import hashlib
import io
import json
import sys

BASE = Path(__file__).resolve().parents[2]
ONE = {(0, 0, 0): 1}

def plus(*args):
    out = defaultdict(int)
    for p in args:
        for ex, v in p.items():
            out[ex] += v
    return {ex: v for ex, v in out.items() if v}

def scale(p, v):
    return {ex: v * a for ex, a in p.items() if v * a}

def minus(p, q):
    return plus(p, scale(q, -1))

def times(*args):
    out = ONE
    for p in args:
        accum = defaultdict(int)
        for ex, v in out.items():
            for ey, b in p.items():
                accum[tuple(x + y for x, y in zip(ex, ey))] += v * b
        out = {ex: v for ex, v in accum.items() if v}
    return out

def power(p, n):
    return times(*(p for _ in range(n)))

def variable(axis):
    return {tuple(int(i == axis) for i in range(3)): 1}

c, s, w = (variable(i) for i in range(3))
t = times(c, s)
u = times(c, t)
t2, u2, w2 = power(t, 2), power(u, 2), power(w, 2)
J100 = scale(power(plus(ONE, c), 2), 49)
a = times(c, plus(ONE, times(plus(power(c, 2), scale(ONE, 2)), t2)))
b = times(t, plus(ONE, scale(power(c, 2), 2), times(power(c, 2), t2)))

# Direct transcription of 100 E, before rational w substitution.
E100 = minus(
    times(c, minus(ONE, t2), minus(ONE, u2),
          minus(times(minus(ONE, t2), J100, w2),
                scale(times(minus(w2, ONE), power(plus(w, u), 2)), 100))),
    times(minus(a, times(b, w)),
          plus(scale(times(plus(ONE, times(u, w)), power(plus(w, u), 2)), 100),
               times(J100, w, plus(w, times(u, t2))))))
assert all(i > 0 for i, j, k in E100)
E100_over_c = {(i - 1, j, k): v for (i, j, k), v in E100.items()}
assert max(k for i, j, k in E100_over_c) == 4

alpha = plus(ONE, times(plus(power(c, 4), scale(power(c, 2), 2)), power(s, 2)))
beta = times(s, plus(ONE, scale(power(c, 2), 2), times(power(c, 4), power(s, 2))))
delta = minus(alpha, beta)
assert delta == times(minus(ONE, s), power(minus(ONE, times(power(c, 2), s)), 2))
assert a == times(c, alpha)
assert b == times(c, beta)
W = plus(beta, times(delta, w))  # Third coordinate is now zeta.

# beta**4 * (100 E / c)(c,s,W/beta), termwise homogenization.
parts = []
for k in range(5):
    ck = {(i, j, 0): v for (i, j, p), v in E100_over_c.items() if p == k}
    parts.append(times(ck, power(W, k), power(beta, 4 - k)))
F = plus(*parts)
assert tuple(max(e[axis] for e in F) for axis in range(3)) == (26, 18, 4)

def affine_horner(p, axis, n, offset, divisor):
    """Return divisor**n p(...,(offset+x_axis)/divisor,...)."""
    linear = plus(variable(axis), scale(ONE, offset))
    out = {}
    for degree in range(n, -1, -1):
        section = {}
        for ex, value in p.items():
            if ex[axis] == degree:
                e = list(ex)
                e[axis] = 0
                section[tuple(e)] = value * divisor ** (n - degree)
        out = plus(times(out, linear), section)
    return out

G = affine_horner(affine_horner(F, 0, 26, 2, 3), 1, 18, 1, 2)
N = (26, 18, 4)
indices = [(i, j, k) for i in range(27) for j in range(19) for k in range(5)]

# Rational Bernstein transform: divide by degree binomials, then use
# binomial transforms computed only through adjacent additions.
B = {e: Fraction(G.get(e, 0), comb(26, e[0]) * comb(18, e[1]) * comb(4, e[2]))
     for e in indices}
for axis, n in enumerate(N):
    updated = {}
    for e in indices:
        if e[axis] != 0:
            continue
        row = []
        for j in range(n + 1):
            pos = list(e)
            pos[axis] = j
            row.append(B[tuple(pos)])
        for j in range(n + 1):
            pos = list(e)
            pos[axis] = j
            updated[tuple(pos)] = row[0]
            row = [row[k] + row[k + 1] for k in range(len(row) - 1)]
    B = updated
assert len(B) == 2565
assert sum(x > 0 for x in B.values()) == 2535
assert sum(x == 0 for x in B.values()) == 30
assert all(x >= 0 for x in B.values())
assert all(B[e] > 0 for e in indices if e[0] == 0)
assert all((B[e] == 0) == (e[0] + e[1] >= 42) for e in indices)

# Only after the independent reconstruction, execute the frozen certificate
# and compare every F, G and Bernstein coefficient with its output.
answer = (BASE / 'answer.md').read_text()
assert hashlib.sha256(answer.encode()).hexdigest() == '51b01295406d1899e3492bd8498731b9f5aac81635c9450bdbc21cf332745776'
source = answer.split('```python\n', 1)[1].split('```', 1)[0]
namespace = {'__name__': '__certificate__'}
captured = io.StringIO()
with contextlib.redirect_stdout(captured):
    exec(compile(source, '<frozen answer certificate>', 'exec'), namespace)
assert F == namespace['F']
assert G == namespace['G']
assert all(B[e] == Fraction(namespace['C'].get(e, 0), namespace['L']) for e in indices)

result = {
    'status': 'PASS',
    'python': sys.version,
    'independent_F_terms': len(F),
    'independent_G_terms': len(G),
    'degrees': N,
    'bernstein_positive': sum(v > 0 for v in B.values()),
    'bernstein_zero': sum(v == 0 for v in B.values()),
    'all_i_zero_positive': all(B[e] > 0 for e in indices if e[0] == 0),
    'every_coefficient_matches_frozen_checker': True,
    'checker_stdout': captured.getvalue().strip(),
    'methods': [
        'Direct integer expansion of displayed E before homogeneous w substitution',
        'Horner affine substitution for c and s',
        'Fraction-valued Bernstein transform by Pascal adjacent addition tables'
    ]
}
print(json.dumps(result, indent=2))
