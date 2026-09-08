CANDIDATE_COMPLETE_PROOF

# O7 exact algebraic certificate

## Exact theorem and scope

Let `2/3<=c<1`, `c/2<=t<=c`, `u=ct`,

`a=c(1+(c^2+2)t^2)`, `b=t(1+2c^2+c^2t^2)`,
`J=(49/100)(1+c)^2`, and `1<=w<=a/b`.

Then the polynomial expression in `runs/q9/jensen_algebra_task.md`, namely

```
E = c(1-t^2)(1-u^2)[(1-t^2)Jw^2-(w^2-1)(w+u)^2]
    -(a-bw)[(1+uw)(w+u)^2+Jw(w+ut^2)],
```

is strictly positive. The endpoint `t=c` is included here as an extension; the parent's assigned domain had `t<c`.

This settles O7 only. The parent retains responsibility for the analytic reductions from C1--C3 and Q positivity and for the full Q9 audit. No global completion is claimed by this worker.

## Exact change of variables

Put `s=t/c`, so `1/2<=s<=1`, and introduce the normalized polynomials

```
a0 = a/c = 1+(c^4+2c^2)s^2,
b0 = b/c = s(1+2c^2+c^4s^2),
D = a0-b0 = (1-s)(1-c^2s)^2,
u = c^2s.
```

Here `b0>0` and `D>=0`. If `D>0`, let `z=b0(w-1)/D`; the prescribed w interval gives `0<=z<=1`. If `D=0`, the interval consists of w=1 and choose z=0. Thus in all cases

`W=b0+Dz`, `w=W/b0`, `V=W+u b0`, and `a-bw=cD(1-z)`.

Define the following integer polynomial, with `t2=c^2s^2` and `J100=49(1+c)^2`:

```
F(c,s,z) = (1-t2)(1-u^2)[(1-t2)J100 W^2 b0^2
                           -100(W^2-b0^2)V^2]
           -D(1-z)[100 b0(b0+uW)V^2
                     +J100 W(W+u t2 b0)b0^2].
```

Direct substitution and multiplication by positive denominators give the exact identity

`F(c,s,z) = 100 b0^4 E/c`.

The code below builds this displayed polynomial directly; its degree in `(c,s,z)` is `(26,18,4)`.

Set `x=3c-2` and `y=2s-1`. Then `0<=x<1`, `0<=y<=1`, `0<=z<=1`. The scaled affine substitution

`G(x,y,z)=3^26 2^18 F((2+x)/3,(1+y)/2,z)`

has integer coefficients. The factor `3^26 2^18=666334875701477376` is positive.

## Bernstein certificate and strictness

For `0<=i<=n`, write `B[n,i](x)=binom(n,i)x^i(1-x)^(n-i)`. These basis polynomials are nonnegative on `[0,1]` and sum to one.

Let `g[p,q,r]` be G's integer power coefficients and

`L=product_(n in {26,18,4}) lcm_(0<=i<=n) binom(n,i)
 =437341981684608000`.

Define the integer coefficients

```
C[i,j,k] = L sum_(p<=i,q<=j,r<=k)
  g[p,q,r] binom(i,p)/binom(26,p)
             binom(j,q)/binom(18,q)
             binom(k,r)/binom(4,r).
```

The power-to-Bernstein identity is

```
L G(x,y,z) = sum_(i=0..26,j=0..18,k=0..4)
  C[i,j,k] B[26,i](x) B[18,j](y) B[4,k](z).
```

The exact finite checker below computes every coefficient with integers only and proves:

- There are 2,565 coefficients: 2,535 positive and 30 zero, with none negative.
- More precisely, a coefficient is zero exactly when `i+j>=42`.
- In particular, every `C[0,j,k]` is positive.
- Inverting the basis transformation reproduces exactly `L G`, coefficient by coefficient.

Consequently `L G` is at least

`(1-x)^26 min_(j,k) C[0,j,k]`,

which is strictly positive because x<1. Thus G>0, F>0, and E>0 by the positive scaling identities. This is a universal polynomial certificate, not an inference from sampled evaluations.

## Standalone exact checker

Replay with Python 3.9 or newer. It uses only the standard library, performs no I/O except the final result line, and uses no floating-point arithmetic. The following code is identical to `runs/q9/worker_jensen_certificate.py`.

```python
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
```

Observed checker output:

```
PASS: exact Bernstein identity; 2535 positive, 30 zero; E > 0 for c < 1.
```

## Verification, provenance, and decision delta

- Input: the exact parent task `runs/q9/jensen_algebra_task.md`; no external sources or literature were accessed.
- Discovery used exact sparse integer expansion and a single Bernstein conversion. It required no domain subdivision, optimizer, or numerical guessing.
- A separate checker reconstructed the power polynomial from the saved Bernstein coefficients and verified direct equality with the original E at 64 rational tuples as a supplementary transcription check. The finite tuple checks do not carry the universal conclusion; the exact basis identity does.
- The parent independently inspected the denominator-clearing identity and the affine map and reported that they appeared correct. A full fresh package audit remains the parent's responsibility.
- Supporting artifacts: `worker_jensen_poly.py`, `worker_jensen_initial.json`, and `worker_jensen_verify.py`. The standalone checker above contains everything necessary to reproduce and verify this O7 certificate.
- Status is `CANDIDATE_COMPLETE_PROOF` pending the parent's independent acceptance. No unresolved obligation remains within the exact O7 polynomial statement.
- Decision delta: close O7 after independent audit; stop further algebraic research and integrate this certificate with the parent's analytic prerequisites.
