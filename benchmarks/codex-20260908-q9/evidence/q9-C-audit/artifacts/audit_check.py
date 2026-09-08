"""Independent exact checks of the mathematics submitted in CANDIDATE.md.

Run with python3 audit_check.py. Only Python's standard library is required.
This verifies existing submitted arguments; it supplies no repair or new lemma.
Polynomials use three exponent coordinates (c, s, v).
"""

from fractions import Fraction as F
from math import comb
from pathlib import Path
import contextlib
import hashlib
import io
import json


def constant(q):
    return {} if not q else {(0, 0, 0): F(q)}


def add(*ps):
    out = {}
    for p in ps:
        for key, value in p.items():
            out[key] = out.get(key, F(0)) + value
    return {key: value for key, value in out.items() if value}


def scale(p, q):
    return {key: value * q for key, value in p.items() if value * q}


def mul(*ps):
    out = constant(1)
    for p in ps:
        product = {}
        for key, value in out.items():
            for key2, value2 in p.items():
                exponent = tuple(a + b for a, b in zip(key, key2))
                product[exponent] = product.get(exponent, F(0)) + value * value2
        out = {key: value for key, value in product.items() if value}
    return out


def power(p, exponent):
    out = constant(1)
    for _ in range(exponent):
        out = mul(out, p)
    return out


def coefficient_v(p, exponent):
    return {(i, j, 0): q for (i, j, k), q in p.items() if k == exponent}


def derivative_v(p):
    return {(i, j, k - 1): q * k for (i, j, k), q in p.items() if k}


def at_v_one(p):
    return add(*[{(i, j, 0): q} for (i, j, _), q in p.items()])


def affine_rectangle(p):
    """Direct binomial expansion at c=(2+X)/3, s=(1+2Y)/3."""
    out = {}
    for (i, j, k), value in p.items():
        assert k == 0
        for pwr_x in range(i + 1):
            for pwr_y in range(j + 1):
                term = (value * comb(i, pwr_x) * comb(j, pwr_y)
                        * F(2 ** (i - pwr_x + pwr_y), 3 ** (i + j)))
                key = (pwr_x, pwr_y)
                out[key] = out.get(key, F(0)) + term
    return {key: value for key, value in out.items() if value}


def power_to_bernstein_vector(a):
    """Triangular basis solve, independent of the submission's formula (21)."""
    n = len(a) - 1
    b = []
    for p in range(n + 1):
        lower = sum(b[i] * comb(n, i) * comb(n - i, p - i)
                    * (-1) ** (p - i) for i in range(p))
        b.append((a[p] - lower) / comb(n, p))
    return b


def bernstein(p):
    n = max(i for i, _ in p)
    m = max(j for _, j in p)
    columns = [power_to_bernstein_vector([p.get((i, j), F(0))
                                         for i in range(n + 1)])
               for j in range(m + 1)]
    b = [power_to_bernstein_vector([columns[j][i] for j in range(m + 1)])
         for i in range(n + 1)]
    # Reconstruct every power coefficient, proving a polynomial identity.
    for pwr_x in range(n + 1):
        for pwr_y in range(m + 1):
            actual = sum(
                b[i][j] * comb(n, i) * comb(n - i, pwr_x - i)
                * comb(m, j) * comb(m - j, pwr_y - j)
                * (-1) ** (pwr_x - i + pwr_y - j)
                for i in range(pwr_x + 1) for j in range(pwr_y + 1))
            assert actual == p.get((pwr_x, pwr_y), 0)
    return (n, m), b


one = constant(1)
c = {(1, 0, 0): F(1)}
s = {(0, 1, 0): F(1)}
v = {(0, 0, 1): F(1)}
r = power(s, 2)
h = add(one, scale(r, -1))
a = mul(c, s)
delta = add(one, scale(power(a, 2), -1))
W = add(one, scale(s, 6), scale(r, 3))
Z = add(constant(3), scale(s, 2))
C = mul(c, add(one, mul(add(power(c, 2), constant(2)), r)))
D = mul(s, add(one, scale(power(c, 2), 2), mul(power(c, 2), r)))

# Form delta*W*N directly from (18), before using coefficient formulas (19).
P = add(
    mul(c, h, delta, v, add(W, mul(Z, h), scale(mul(W, power(v, 2)), -1))),
    scale(mul(add(C, scale(mul(D, v), -1)),
              add(mul(v, add(W, Z)), mul(a, add(mul(W, power(v, 2)), mul(r, Z))))), -1))
assert max(key[2] for key in P) == 3
n = [coefficient_v(P, i) for i in range(4)]
stated_n = [
    scale(mul(C, a, r, Z), -1),
    add(mul(c, h, add(W, mul(Z, h)), delta),
        scale(mul(C, add(W, Z)), -1), mul(D, a, r, Z)),
    add(mul(D, add(W, Z)), scale(mul(C, a, W), -1)),
    mul(W, add(mul(D, a), scale(mul(c, h, delta), -1))),
]
assert n == stated_n
assert add(C, scale(D, -1)) == mul(add(c, scale(s, -1)), power(add(one, scale(a, -1)), 2))
assert add(power(W, 2), scale(mul(r, Z), -4)) == add(
    one, scale(s, 12), scale(r, 30), scale(power(s, 3), 28), scale(power(s, 4), 9))

# Independent construction of E0, E1 and the denominator-cleared derivative E3.
E = [at_v_one(P), at_v_one(derivative_v(P)), n[2],
     add(*[scale(mul(n[k], power(C, k - 1), power(D, 3 - k)), k)
           for k in range(1, 4)])]
expected = [((4, 6), F(0)), ((4, 6), F(9382, 6561)),
            ((4, 5), F(25553, 6561)), ((9, 12), F(134561396, 387420489))]
report = []
for index, poly in enumerate(E):
    degree, coeffs = bernstein(affine_rectangle(poly))
    values = [value for row in coeffs for value in row]
    assert (degree, min(values)) == expected[index]
    assert all(value >= 0 for value in values)
    if index == 0:
        assert coeffs[0][0] == F(15169, 59049)
    else:
        assert all(value > 0 for value in values)
    report.append({'polynomial': f'E{index}', 'degrees': degree,
                   'coefficient_count': len(values), 'minimum': str(min(values)),
                   'zero_count': values.count(F(0)), 'b00': str(coeffs[0][0])})

# Check the denominator reductions in (22) after x^2=h/(v^2-1).
q = add(power(v, 2), scale(one, -1))
L = add(mul(Z, h), scale(mul(W, q), -1))
assert add(mul(W, q), mul(W, h), L) == mul(h, add(W, Z))
assert add(mul(W, q), mul(W, h), mul(r, L)) == mul(h, add(mul(W, power(v, 2)), mul(r, Z)))

# Re-run the original embedded certificate unchanged, without external files.
source = Path('CANDIDATE.md').read_text()
blocks = source.split('```python\n')
assert len(blocks) == 2
code = blocks[1].split('```')[0]
captured = io.StringIO()
with contextlib.redirect_stdout(captured):
    exec(compile(code, 'CANDIDATE.md:certificate', 'exec'), {'__name__': '__main__'})

output = {
    'inputs_sha256': {name: hashlib.sha256(Path(name).read_bytes()).hexdigest()
                      for name in ('TASK.md', 'CANDIDATE.md')},
    'method': 'Exact Fraction arithmetic; direct expansion of (18); independent triangular Bernstein basis conversion and full polynomial reconstruction.',
    'independent_certificate': report,
    'checked_symbolic_identities': ['(15)', '(19)', 'discriminant in section 2',
                                    'E0 and E1 as value and derivative at 1',
                                    'E3 as D^2 times derivative at C/D',
                                    'denominator simplifications for (22)'],
    'original_certificate_stdout': captured.getvalue(),
    'all_checks_passed': True,
}
print(json.dumps(output, indent=2))
