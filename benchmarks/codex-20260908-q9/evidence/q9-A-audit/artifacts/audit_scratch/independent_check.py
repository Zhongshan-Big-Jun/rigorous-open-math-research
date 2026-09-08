"""Independent exact check of the certificates printed in CANDIDATE.md.

This does not import or use the submitted polynomial implementation. It
recovers Bernstein coefficients by inverting exact rational collocation
matrices. The degree bounds follow directly from the displayed expressions:
the z polynomial has bidegree <= (9, 12), total degree <= 19; the t polynomial
has bidegree <= (9, 13), total degree <= 19. Substitution s=h+(c-h)v therefore
gives bounds (19, 12) and (19, 13). The rectangular substitution keeps the
original bidegrees. Unisolvence, not sampled positivity, certifies equality.
For (8), both sides have bidegree <= (5, 5), so a 6 by 6 exact grid suffices
to check the supplied identity without assuming its claimed degree.
"""

from fractions import Fraction as F
from math import comb
from pathlib import Path
import hashlib
import json
import sys


def basis(n, i, x):
    return comb(n, i) * x**i * (1-x)**(n-i)


def inverse(matrix):
    n = len(matrix)
    a = [list(row) + [F(i == j) for j in range(n)]
         for i, row in enumerate(matrix)]
    for k in range(n):
        pivot = next(i for i in range(k, n) if a[i][k])
        a[k], a[pivot] = a[pivot], a[k]
        d = a[k][k]
        a[k] = [x/d for x in a[k]]
        for i in range(n):
            if i != k and a[i][k]:
                d = a[i][k]
                a[i] = [x-d*y for x, y in zip(a[i], a[k])]
    assert all(a[i][j] == F(i == j) for i in range(n) for j in range(n))
    return [row[n:] for row in a]


def mm(a, b):
    return [[sum((x*y for x, y in zip(row, col)), F(0))
             for col in zip(*b)] for row in a]


_inverses = {}


def inv_collocation(n):
    if n not in _inverses:
        _inverses[n] = inverse([[basis(n, j, F(i, n)) for j in range(n+1)]
                               for i in range(n+1)])
    return _inverses[n]


def coefficients(evaluate, n, m):
    values = [[evaluate(F(i, n), F(j, m)) for j in range(m+1)]
              for i in range(n+1)]
    return mm(mm(inv_collocation(n), values), list(zip(*inv_collocation(m))))


def poly_p(c, s):
    return 1+2*c*c-3*c*s-3*c*c*s*s+c*(2+c*c)*s**3


def poly_e(c, s):
    return (c+s)*(1-c*s)*poly_p(c, s)-(1-c*c)*s*(1+c*s)**3


SMALL_N = [
    [1328125000,1243125000,1051925000,765469000,412948680,12607112],
    [1650390625,1534140625,1300215625,966327625,571546705,138478561],
    [2050781250,1891406250,1603781250,1216202250,781848450,330011178],
    [2548828125,2329453125,1972378125,1522315125,1052902845,604001061],
    [3164062500,2860312500,2410762500,1885396500,1387790820,974492532],
]


def check_small_identity():
    for i in range(6):
        for j in range(6):
            u, v = F(i, 5), F(j, 5)
            rhs = sum((F(SMALL_N[a][b], 1054687500)
                       * basis(4, a, u) * basis(5, b, v)
                       for a in range(5) for b in range(6)), F(0))
            assert poly_e((2+u)/3, 12*v/25) == rhs
    assert all(x > 0 for row in SMALL_N for x in row)
    return {"status": "PASS", "exact_identity_grid": [6, 6],
            "degree_bound_for_identity_difference": [5, 5],
            "positive_coefficients": 30,
            "minimum_coefficient": str(F(min(map(min, SMALL_N)), 1054687500))}


def certificate_polynomials(c, s, z0, t0):
    # Written directly from (9) and (13), independently of submitted code.
    w_num = (c-s)*(1-c*c*s*s)
    w_den = s*poly_p(c, s)
    ell_num = (1-c*c*s*s)**2*(c*c-s*s)
    ell_den = s*s*(1-s*s)*(1+2*c*c+c*c*s*s)**2
    z_num = w_num*ell_den+(w_den+w_num)*ell_num
    z_den = w_den*ell_den
    t_den = w_den*(ell_den+(1-s*s)*ell_num)
    return z0*z0*z_den-z_num, t0*t0*t_den-s*s*z_num


ROWS = [
    (F(2,3), F(7,10), F(12,25), None, F(19,20), F(21,50)),
    (F(7,10), F(3,4), F(12,25), None, F(101,100), F(9,20)),
    (F(3,4), F(1), F(12,25), F(3,5), F(27,25), F(1,2)),
    (F(3,4), F(1), F(3,5), None, F(9,10), F(3,5)),
]


def check_table():
    records = []
    for row_id, (a, b, h, top, z0, t0) in enumerate(ROWS, 1):
        for which, m in enumerate((12, 13)):
            n = 19 if top is None else 9

            def evaluate(u, v):
                c = a+(b-a)*u
                s = h+((c if top is None else top)-h)*v
                return certificate_polynomials(c, s, z0, t0)[which]

            beta = coefficients(evaluate, n, m)
            flat = [x for rr in beta for x in rr]
            assert all(x >= 0 for x in flat)
            # Nonzero leading coefficients certify the stated exact degrees.
            assert any(sum(((-1)**(n-i)*comb(n,i)*beta[i][j]
                            for i in range(n+1)), F(0)) for j in range(m+1))
            assert any(sum(((-1)**(m-j)*comb(m,j)*beta[i][j]
                            for j in range(m+1)), F(0)) for i in range(n+1))
            zeros = [[i, j] for i in range(n+1) for j in range(m+1)
                     if beta[i][j] == 0]
            records.append({"row": row_id, "quantity": ["Z", "D_star"][which],
                            "bidegree": [n, m], "coefficient_count": len(flat),
                            "zero_count": len(zeros), "zero_positions": zeros,
                            "minimum_positive_coefficient": str(min(x for x in flat if x > 0))})
    assert sum(r["coefficient_count"] for r in records) == 1890
    assert sum(r["zero_count"] for r in records) == 12
    return records


def check_angles():
    upper = lambda x: x-x**3/3+x**5/5
    assert upper(F(9,20)) < F(43,100)
    assert upper(F(1,2)) == F(223,480)
    assert upper(F(3,5)) < F(11,20)
    pi_lo = 4*(F(1,2)-F(1,24)+F(1,160)-F(1,896)+F(1,3)-F(1,81))
    assert pi_lo == F(284663,90720) > F(25,8)
    bounds = [(F(3,8), F(153,400)), (F(5,14), F(153,350)),
              (F(1,3), F(1243,2400)), (F(1,3), F(29,60))]
    small_angle_upper = [F(21,50), F(43,100), F(223,480), F(11,20)]
    margins = []
    for row, t_bound, (pi_coefficient, constant) in zip(ROWS, small_angle_upper, bounds):
        c_min, _, _, _, z_bound, _ = row
        assert F(1,4)/c_min == pi_coefficient
        assert t_bound+(z_bound-1)/(2*c_min) == constant
        margin = (F(1,2)-pi_coefficient)*F(25,8)-constant
        assert margin > 0
        margins.append(str(margin))
    return {"pi_lower_bound": str(pi_lo), "strict_row_margins_using_pi_gt_25_over_8": margins}


def main():
    result = {
        "status": "PASS",
        "method": "Exact rational polynomial interpolation with proved degree bounds, followed by Bernstein coefficient signs; no floating-point arithmetic or submitted code import.",
        "python": sys.version,
        "input_sha256": {name: hashlib.sha256(Path(name).read_bytes()).hexdigest()
                         for name in ("TASK.md", "CANDIDATE.md")},
        "small_s": check_small_identity(),
        "table": check_table(),
        "angle_checks": check_angles(),
    }
    out = Path(__file__).with_name("independent_results.json")
    out.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
