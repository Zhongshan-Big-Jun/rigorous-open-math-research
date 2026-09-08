"""Q9 certificate: exact rational arithmetic, no numerical sampling."""
from fractions import Fraction as F
from math import comb

# Sparse polynomials: (degree in c, degree in s) -> rational coefficient.
def add(*ps):
    q = {}
    for p in ps:
        for ij, a in p.items():
            q[ij] = q.get(ij, F(0)) + a
    return {ij: a for ij, a in q.items() if a}

def scale(p, a):
    return {ij: a*b for ij, b in p.items() if a*b}

def sub(p, q):
    return add(p, scale(q, -1))

def mul(p, q):
    r = {}
    for (i, j), a in p.items():
        for (k, l), b in q.items():
            ij = (i+k, j+l)
            r[ij] = r.get(ij, F(0)) + a*b
    return {ij: a for ij, a in r.items() if a}

def power(p, n):
    q = {(0, 0): F(1)}
    for _ in range(n):
        q = mul(q, p)
    return q

def substitute(p, C, S):
    cp = [power(C, i) for i in range(max(i for i,j in p)+1)]
    sp = [power(S, j) for j in range(max(j for i,j in p)+1)]
    return add(*(scale(mul(cp[i], sp[j]), a)
                 for (i, j), a in p.items()))

def bernstein(p):
    n = max(i for i,j in p)
    m = max(j for i,j in p)
    b = [[sum((a*F(comb(i,k),comb(n,k))*F(comb(j,l),comb(m,l))
               for (k,l),a in p.items() if k<=i and l<=j), F(0))
          for j in range(m+1)] for i in range(n+1)]
    return n, m, b

one = {(0,0): F(1)}
c = {(1,0): F(1)}
s = {(0,1): F(1)}
c2, s2 = power(c,2), power(s,2)
cs = mul(c,s)
P = add(one, scale(c2,2), scale(cs,-3),
        scale(mul(c2,s2),-3), mul(mul(c,add(scale(one,2),c2)),power(s,3)))
E = sub(mul(mul(add(c,s),sub(one,cs)),P),
        mul(mul(sub(one,c2),s),power(add(one,cs),3)))

# Small-s certificate, equation (8).
C = add(scale(one,F(2,3)),scale(c,F(1,3)))
S = scale(s,F(12,25))
n,m,b = bernstein(substitute(E,C,S))
N = [
 [1328125000,1243125000,1051925000,765469000,412948680,12607112],
 [1650390625,1534140625,1300215625,966327625,571546705,138478561],
 [2050781250,1891406250,1603781250,1216202250,781848450,330011178],
 [2548828125,2329453125,1972378125,1522315125,1052902845,604001061],
 [3164062500,2860312500,2410762500,1885396500,1387790820,974492532]]
assert (n,m)==(4,5)
assert all(b[i][j]==F(N[i][j],1054687500)>0
           for i in range(5) for j in range(6))

# Complementary certificate, equations (13)-(14).
J = sub(one,mul(c2,s2))
Nw, Dw = mul(sub(c,s),J), mul(s,P)
Nl = mul(power(J,2),sub(c2,s2))
Dl = mul(mul(s2,sub(one,s2)),
         power(add(one,scale(c2,2),mul(c2,s2)),2))
Nz = add(mul(Nw,Dl),mul(add(Dw,Nw),Nl))
Dz = mul(Dw,Dl)
Nd = mul(s2,Nz)
Dd = mul(Dw,add(Dl,mul(sub(one,s2),Nl)))
# (c lower, c upper, s lower, s upper or None meaning c, z bound, d bound).
rows = [
 (F(2,3),F(7,10),F(12,25),None,F(19,20),F(21,50)),
 (F(7,10),F(3,4),F(12,25),None,F(101,100),F(9,20)),
 (F(3,4),F(1),F(12,25),F(3,5),F(27,25),F(1,2)),
 (F(3,4),F(1),F(3,5),None,F(9,10),F(3,5))]
expected = [((19,12),(19,13)),((19,12),(19,13)),
            ((9,12),(9,13)),((19,12),(19,13))]
count = zero_count = 0
for row_number,(a,b,t,h,z,d) in enumerate(rows):
    C = add(scale(one,a),scale(c,b-a))
    S = (add(scale(one,t),mul(sub(C,scale(one,t)),s)) if h is None
         else add(scale(one,t),scale(s,h-t)))
    for which,p in enumerate((sub(scale(Dz,z*z),Nz),sub(scale(Dd,d*d),Nd))):
        n,m,bb = bernstein(substitute(p,C,S))
        assert (n,m)==expected[row_number][which]
        values = [v for rr in bb for v in rr]
        assert all(v>=0 for v in values)
        count += len(values)
        zero_count += sum(v==0 for v in values)
assert (count,zero_count)==(1890,12)

# Rational comparisons used in the final trigonometric contradiction.
def atan_upper(t):
    return t-t**3/F(3)+t**5/F(5)
assert atan_upper(F(9,20)) < F(43,100)
assert atan_upper(F(1,2)) == F(223,480)
assert atan_upper(F(3,5)) < F(11,20)
pi_lower = 4*(F(1,2)-F(1,24)+F(1,160)-F(1,896)+F(1,3)-F(1,81))
assert pi_lower == F(284663,90720) > F(25,8)
assert all(F(25,8)>v for v in [F(153,50),F(1243,400),F(29,10)])
print('PASS: 30 positive small-s coefficients; 1890 nonnegative')
print('complementary coefficients (12 zero); all rational angle bounds.')
