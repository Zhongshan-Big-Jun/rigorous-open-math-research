#!/usr/bin/env python3
"""Independent exact checks for TASK.md and CANDIDATE.md; standard library only.

This verifies the submitted arguments and certificate. It supplies no repair.
The independent polynomial implementation does not use the candidate's P class.
"""
from collections import defaultdict
from contextlib import redirect_stdout
from fractions import Fraction
from hashlib import sha256
from io import StringIO
from itertools import product
from math import comb
from pathlib import Path
import json
import sys


class Poly:
    def __init__(self, n, terms):
        self.n = n
        self.terms = {e: Fraction(v) for e, v in terms.items() if v}

    def scalar(self, value):
        if isinstance(value, Poly):
            assert value.n == self.n
            return value
        return Poly(self.n, {(0,) * self.n: value})

    def __add__(self, value):
        value = self.scalar(value)
        terms = defaultdict(Fraction, self.terms)
        for e, v in value.terms.items():
            terms[e] += v
        return Poly(self.n, terms)

    __radd__ = __add__

    def __neg__(self):
        return Poly(self.n, {e: -v for e, v in self.terms.items()})

    def __sub__(self, value):
        return self + (-self.scalar(value))

    def __rsub__(self, value):
        return self.scalar(value) - self

    def __mul__(self, value):
        value = self.scalar(value)
        terms = defaultdict(Fraction)
        for a, av in self.terms.items():
            for b, bv in value.terms.items():
                terms[tuple(x + y for x, y in zip(a, b))] += av * bv
        return Poly(self.n, terms)

    __rmul__ = __mul__

    def __pow__(self, degree):
        assert isinstance(degree, int) and degree >= 0
        result, base = self.scalar(1), self
        while degree:
            if degree % 2:
                result = result * base
            degree //= 2
            if degree:
                base = base * base
        return result

    def __eq__(self, value):
        return self.terms == self.scalar(value).terms

    def substitute(self, replacements):
        assert len(replacements) == self.n
        degrees = [max(e[a] for e in self.terms) for a in range(self.n)]
        powers = [[p**i for i in range(d + 1)]
                  for p, d in zip(replacements, degrees)]
        result = replacements[0].scalar(0)
        for e, coefficient in self.terms.items():
            term = result.scalar(coefficient)
            for axis, exponent in enumerate(e):
                term = term * powers[axis][exponent]
            result = result + term
        return result


def variables(n):
    return tuple(Poly(n, {tuple(int(i == j) for j in range(n)): 1})
                 for i in range(n))


def algebra_checks():
    x, _, _ = variables(3)
    assert 3*(2-x)**2 - 2*(1-x)*(2+x)**2 == (3*x-2)**2 + 2*x**3
    ell, w, u = variables(3)
    assert ((ell**2-1)*(1-u*w)**2 - (w**2-1)*(1+u*ell)**2
            == (ell+w)*((1+u**2)*(ell-w)-2*u*(ell*w-1)))

    c, t, w = variables(3)
    u = c*t
    a = c*(1+(c*c+2)*t*t)
    b = t*(1+2*c*c+c*c*t*t)
    d = 1+u*u-2*u*w
    n = (1+u*u)*w-2*u
    assert a-b == (c-t)*(1-c*t)**2
    assert c*d-t*n == a-b*w
    assert d+u*n == (1-u*u)*(1-u*w)

    c5, t5, z5, w5, m5 = variables(5)
    u5 = c5*t5
    original_den = (w5*(1+m5*m5*z5*z5)
                    + u5*(1+z5*z5+(m5*m5-1)*t5*t5*z5*z5))
    transformed_den = (w5*(1+u5*w5+m5*m5*z5*z5)
                       + u5*t5*t5*m5*m5*z5*z5)
    assert original_den-transformed_den == u5*(1+(1-t5*t5)*z5*z5-w5*w5)
    assert (m5*m5-1)*z5*z5 == (m5*z5)**2-z5*z5

    q = Fraction(7, 10)
    assert 5*q-10*q**3+q**5 == Fraction(23807, 100000)
    assert 1-10*q*q+5*q**4 == Fraction(-5399, 2000)

    j100 = 49*(1+c)**2
    j_factor = Fraction(1, 100)*j100
    # Literal equation (11), before either certificate substitution.
    bracket = ((1+u*w)*(w+u)**2+j_factor*w*(w+u*t*t))
    e_poly = (c*(1-t*t)*(1-u*u)
              *((1-t*t)*j_factor*w*w-(w*w-1)*(w+u)**2)
              -(a-b*w)*bracket)
    # Clearing denominators in K(j)-f gives exactly the same numerator.
    k_j_numerator = c*(1-t*t)*((1-t*t)*j_factor*w*w-(w*w-1)*(w+u)**2)
    assert e_poly == (1-u*u)*k_j_numerator-(a-b*w)*bracket
    return e_poly


def rebuild_f(e_poly):
    c, s, zeta = variables(3)
    alpha = 1+(c**4+2*c*c)*s*s
    beta = s*(1+2*c*c+c**4*s*s)
    delta = (1-s)*(1-c*c*s)**2
    assert alpha-beta == delta
    w_num = beta+delta*zeta
    # Substitute each monomial c^i t^j w^k in the independently expanded E:
    # (100 beta^4/c) c^i (c s)^j (w_num/beta)^k.
    assert all(i+j >= 1 and k <= 4 for i, j, k in e_poly.terms)
    max_c = max(i+j-1 for i, j, k in e_poly.terms)
    max_s = max(j for i, j, k in e_poly.terms)
    c_powers = [c**i for i in range(max_c+1)]
    s_powers = [s**j for j in range(max_s+1)]
    w_powers = [w_num**k for k in range(5)]
    b_powers = [beta**k for k in range(5)]
    f = c.scalar(0)
    for (i, j, k), coefficient in e_poly.terms.items():
        f += (100*coefficient*c_powers[i+j-1]*s_powers[j]
              *w_powers[k]*b_powers[4-k])
    assert all(v.denominator == 1 for v in f.terms.values())
    return f


def rational_bernstein(power, degrees):
    """Use rational coefficients and reverse axis order; no common-scale trick."""
    current = power
    for axis in reversed(range(3)):
        n = degrees[axis]
        other_axes = [a for a in range(3) if a != axis]
        result = {}
        for other_indices in product(*(range(degrees[a]+1) for a in other_axes)):
            base = [0, 0, 0]
            for a, index in zip(other_axes, other_indices):
                base[a] = index
            source = []
            for p in range(n+1):
                base[axis] = p
                source.append(current.get(tuple(base), Fraction(0)))
            for i in range(n+1):
                base[axis] = i
                result[tuple(base)] = sum(
                    (source[p]*Fraction(comb(i, p), comb(n, p)) for p in range(i+1)),
                    Fraction(0))
        current = result
    return current


def main():
    base = Path(__file__).resolve().parent
    candidate_bytes = (base/'CANDIDATE.md').read_bytes()
    task_bytes = (base/'TASK.md').read_bytes()
    candidate = candidate_bytes.decode()
    code = candidate.split('```python\n', 1)[1].split('\n```', 1)[0]
    namespace = {'__name__': '__main__'}
    captured = StringIO()
    with redirect_stdout(captured):
        exec(compile(code, 'CANDIDATE.md:certificate', 'exec'), namespace)

    e_poly = algebra_checks()
    f = rebuild_f(e_poly)
    assert f.terms == namespace['F']
    degrees = tuple(max(e[a] for e in f.terms) for a in range(3))
    assert degrees == (26, 18, 4) and len(f.terms) == 637

    xi, eta, zeta = variables(3)
    g = (3**26*2**18)*f.substitute(((2+xi)*Fraction(1, 3),
                                   (1+eta)*Fraction(1, 2), zeta))
    assert g.terms == namespace['G']
    assert len(g.terms) == 2103
    coefficients = rational_bernstein(g.terms, degrees)
    assert all(coefficients[e]*namespace['L'] == namespace['C'].get(e, 0)
               for e in coefficients)
    positive = sum(v > 0 for v in coefficients.values())
    zero = sum(v == 0 for v in coefficients.values())
    negative = sum(v < 0 for v in coefficients.values())
    assert (positive, zero, negative) == (2535, 30, 0)
    assert all(v > 0 for (i, j, k), v in coefficients.items() if i == 0)
    assert all((v == 0) == (i+j >= 42) for (i, j, k), v in coefficients.items())

    output = {
        'python_version': sys.version.split()[0],
        'task_sha256': sha256(task_bytes).hexdigest(),
        'candidate_sha256': sha256(candidate_bytes).hexdigest(),
        'certificate_sha256': sha256((code+'\n').encode()).hexdigest(),
        'submitted_certificate_output': captured.getvalue().strip(),
        'independent_algebra_checks': 'PASS',
        'equation_14_reconstruction': 'PASS: independent expansion of equation (11)',
        'equation_15_reconstruction': 'PASS: exact rational affine substitution',
        'independent_bernstein_conversion': 'PASS: rational arithmetic, reversed axes',
        'degrees': degrees,
        'f_terms': len(f.terms),
        'g_terms': len(g.terms),
        'coefficient_count': len(coefficients),
        'positive_coefficients': positive,
        'zero_coefficients': zero,
        'negative_coefficients': negative,
        'common_integer_scale': namespace['L'],
        'first_index_zero_coefficients_all_positive': True,
        'zero_locus_in_coefficient_indices': 'i+j >= 42, for all k in 0..4',
        'repairs_supplied': False,
    }
    print(json.dumps(output, indent=2))


if __name__ == '__main__':
    main()
