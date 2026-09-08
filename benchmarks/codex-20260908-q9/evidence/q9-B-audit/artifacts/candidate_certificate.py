#!/usr/bin/env python3
# Exact certificate for E >= 0. Standard library; integer arithmetic only.
from collections import defaultdict
from math import comb, lcm

class P(dict):
    def __add__(a, b):
        if not isinstance(b, P): b = P({(0, 0, 0): b})
        d = P(a)
        for k, v in b.items(): d[k] = d.get(k, 0) + v
        return P({k: v for k, v in d.items() if v})
    __radd__ = __add__
    def __neg__(a): return P({k: -v for k, v in a.items()})
    def __sub__(a, b): return a + -b
    def __rsub__(a, b): return -a + b
    def __mul__(a, b):
        if not isinstance(b, P):
            return P({k: v*b for k, v in a.items() if v*b})
        d = defaultdict(int)
        for (i,j,k), v in a.items():
            for (l,m,n), w in b.items(): d[i+l,j+m,k+n] += v*w
        return P({k: v for k, v in d.items() if v})
    __rmul__ = __mul__
    def __pow__(a, n):
        r = P({(0, 0, 0): 1})
        while n:
            if n & 1: r = r*a
            a = a*a
            n //= 2
        return r

c, s, z = (P({e: 1}) for e in ((1,0,0),(0,1,0),(0,0,1)))
t2, u = c*c*s*s, c*c*s
A = 1 + (c**4 + 2*c*c)*s*s
B = s*(1 + 2*c*c + c**4*s*s)
D = (1-s)*(1-u)**2
assert A-B == D
W, J100 = B + D*z, 49*(1+c)**2
V = W + u*B
F = ((1-t2)*(1-u*u)*((1-t2)*J100*W*W*B*B
     - 100*(W*W-B*B)*V*V)
     - D*(1-z)*(100*B*(B+u*W)*V*V
     + J100*W*(W+u*t2*B)*B*B))
N = (26,18,4)
assert tuple(max(e[a] for e in F) for a in range(3)) == N
assert len(F) == 637

# G(x,y,z) = 3**26 * 2**18 * F((2+x)/3,(1+y)/2,z).
G = defaultdict(int)
for (a,b,k), v in F.items():
    for i in range(a+1):
        vi = v*comb(a,i)*2**(a-i)*3**(26-a)
        for j in range(b+1): G[i,j,k] += vi*comb(b,j)*2**(18-b)
G = {e: v for e, v in G.items() if v}
assert len(G) == 2103

# Convert power coefficients to Bernstein coefficients, with positive
# common scale L = product_a lcm_{0<=i<=N[a]} binom(N[a],i).
C, L = G, 1
for axis, n in enumerate(N):
    ell = lcm(*(comb(n,i) for i in range(n+1)))
    L *= ell
    out = defaultdict(int)
    for e, v in C.items():
        i = e[axis]
        for k in range(i,n+1):
            f = list(e); f[axis] = k
            out[tuple(f)] += v*comb(k,i)*(ell//comb(n,i))
    C = dict(out)
index = [(i,j,k) for i in range(27) for j in range(19) for k in range(5)]
values = [C.get(e,0) for e in index]
assert len(values) == 2565
assert sum(v > 0 for v in values) == 2535
assert sum(v == 0 for v in values) == 30
assert all(v >= 0 for v in values)
assert all(C[i,j,k] > 0 for i,j,k in index if i == 0)
assert all((C.get((i,j,k),0) == 0) == (i+j >= 42) for i,j,k in index)

# Independently invert the basis change and check the exact identity.
back = C
for axis, n in enumerate(N):
    out = defaultdict(int)
    for e, v in back.items():
        k = e[axis]
        for i in range(k,n+1):
            f = list(e); f[axis] = i
            out[tuple(f)] += v*comb(n,k)*comb(n-k,i-k)*(-1)**(i-k)
    back = {e: v for e, v in out.items() if v}
assert back == {e: v*L for e, v in G.items()}
print('PASS: exact Bernstein identity; 2535 positive, 30 zero; E > 0 for c < 1.')
