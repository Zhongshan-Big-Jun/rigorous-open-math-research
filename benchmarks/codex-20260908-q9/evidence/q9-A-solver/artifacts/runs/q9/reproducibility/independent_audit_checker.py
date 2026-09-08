from fractions import Fraction as R
from math import comb
from functools import lru_cache
import hashlib

@lru_cache(None)
def inverse_basis(degree):
    nodes = [R(i,degree) for i in range(degree+1)]
    a = [[R(comb(degree,j))*x**j*(1-x)**(degree-j)
          for j in range(degree+1)]
         + [R(i==j) for j in range(degree+1)]
         for i,x in enumerate(nodes)]
    for pivot in range(degree+1):
        at = next(i for i in range(pivot,degree+1) if a[i][pivot])
        a[pivot],a[at] = a[at],a[pivot]
        scale = a[pivot][pivot]
        a[pivot] = [x/scale for x in a[pivot]]
        for i in range(degree+1):
            if i == pivot:
                continue
            ratio = a[i][pivot]
            if ratio:
                a[i] = [x-ratio*y for x,y in zip(a[i],a[pivot])]
    assert all(a[i][j] == (i==j)
               for i in range(degree+1) for j in range(degree+1))
    return tuple(tuple(row[degree+1:]) for row in a)

def recover(fn,n,m):
    values = [[fn(R(i,n),R(j,m)) for j in range(m+1)]
              for i in range(n+1)]
    left, right = inverse_basis(n), inverse_basis(m)
    tmp = [[sum(left[i][k]*values[k][j] for k in range(n+1))
            for j in range(m+1)] for i in range(n+1)]
    return [[sum(tmp[i][l]*right[j][l] for l in range(m+1))
             for j in range(m+1)] for i in range(n+1)]

def scalar_polys(c,s):
    p = 1+2*c*c-3*c*s-3*c*c*s*s+c*(2+c*c)*s**3
    j = 1-c*c*s*s
    nw, dw = (c-s)*j, s*p
    nl = j*j*(c*c-s*s)
    dl = s*s*(1-s*s)*(1+2*c*c+c*c*s*s)**2
    nz = nw*dl+(dw+nw)*nl
    dz = dw*dl
    nt = s*s*nz
    dt = dw*(dl+(1-s*s)*nl)
    return nz,dz,nt,dt

def E(c,s):
    p = 1+2*c*c-3*c*s-3*c*c*s*s+c*(2+c*c)*s**3
    return (c+s)*(1-c*s)*p-(1-c*c)*s*(1+c*s)**3

small = recover(lambda u,v:E((2+u)/3,12*v/25),4,5)
N = [
 [1328125000,1243125000,1051925000,765469000,412948680,12607112],
 [1650390625,1534140625,1300215625,966327625,571546705,138478561],
 [2050781250,1891406250,1603781250,1216202250,781848450,330011178],
 [2548828125,2329453125,1972378125,1522315125,1052902845,604001061],
 [3164062500,2860312500,2410762500,1885396500,1387790820,974492532]]
assert all(small[i][j] == R(N[i][j],1054687500) > 0
           for i in range(5) for j in range(6))
rows = [
 (R(2,3),R(7,10),R(12,25),None,R(19,20),R(21,50)),
 (R(7,10),R(3,4),R(12,25),None,R(101,100),R(9,20)),
 (R(3,4),R(1),R(12,25),R(3,5),R(27,25),R(1,2)),
 (R(3,4),R(1),R(3,5),None,R(9,10),R(3,5))]
counts, serial = [], []
for index,(a,b,h,H,z,t) in enumerate(rows):
    for which,bound in enumerate([z,t]):
        def fn(u,v):
            c = a+(b-a)*u
            s = h+((c if H is None else H)-h)*v
            nz,dz,nt,dt = scalar_polys(c,s)
            return bound*bound*(dz if which==0 else dt)-(nz if which==0 else nt)
        n, m = (9 if index==2 else 19), 12+which
        coefficients = recover(fn,n,m)
        flat = [v for row in coefficients for v in row]
        assert min(flat) >= 0
        counts.append((len(flat),sum(v==0 for v in flat)))
        serial.extend(str(v) for v in flat)
assert sum(n for n,z in counts) == 1890
assert sum(z for n,z in counts) == 12
assert counts == [(260,0),(280,0),(260,0),(280,0),
                  (130,0),(140,0),(260,6),(280,6)]
digest = hashlib.sha256(('\n'.join(serial)+'\n').encode()).hexdigest()
assert digest == 'd143cc7132405be4ab147b06982774841f30bf6048078ff0a52ca974a5b2f11c'
print('PASS: independent rational interpolation; 30 positive and 1890 nonnegative coefficients; 12 zeros.')
print(digest)
