PASS — fresh independent package audit

The frozen candidate proves original Q9, with no remaining load-bearing mathematical gap. The stronger inequality `S>0` is proved from the original domain, Q-positive antecedent, C2, and C3. Retaining C1 as an unused hypothesis is logically valid and does not replace the original simultaneous constraints.

## Frozen inputs and reviewer

- Candidate author: `/root`.
- Reviewer: `/root/counterexample`, a separate agent performing this package audit as a first-time submission.
- Candidate: `answer.md`, SHA-256 `386038fcc8e26b44f20a2cf9c8e02ebd1da28de996ccfe62c521999984c8cb2a`.
- Audited manifest: `runs/q9/completion_manifest.json`, SHA-256 `cb11a77dbd5f078f4dfe92b8cd1bdf623f3e7502bb25eb40e33d803e7676e0ef`.
- Manifest freeze timestamp: `2026-09-08T13:44:03.162789+00:00`.
- Authoritative statement: `TASK.md`, SHA-256 `c7133b97e440e90095088927f105c9f88fcdc54f4a4772ee9f85ba5a139e6330`.
- All manifest-listed file hashes matched. Its contract is byte-identical in hash to TASK.md. The embedded verifier is byte-identical to the listed verifier dependency.

Only the frozen package, TASK.md, and installed skill audit instructions were read for this assignment. No other worker's proof reasoning, literature, internet, or prior solution was consulted. The review does not claim that reviewer and author used different model families. The reviewer did not modify any frozen file.

## Definition audit

The candidate preserves all real domains, strict inequalities, definitions, principal branches, and the exact Q formula. In particular, `s=sqrt(r)` implies `0<s<c<1`; `k=m²−1>0`; and `e=1−c²>0`. The denominator in Q is the original denominator, including the order of its two factors. The definitions of U, V, and R agree with TASK.md.

The main logical chain is sufficient for the exact requested target:

1. Q>0 and C3 give a strict upper bound on `w=k sin²g`.
2. If `s<=12/25`, a rational polynomial certificate proves `S>0`.
3. If `s>=12/25`, Q>0, C2, and C3 contradict one another.
4. `R=S V+k e r(V sin²B−U)>0`.

No mass-balance equation is introduced. C1 is not used by the stronger estimate, but remains part of the universal theorem's hypotheses. The proof does not rely on existence of a relaxed-constraint tuple or on approximately satisfied equations.

## Logic and algebra audit

Every load-bearing step was independently rederived.

### Reduction and C3 bounds

Differentiating H gives `H'=m/(1+k sin²z)`, and hence the stated derivative of F. Integrating between g and B gives `V>pi`. Expanding U and V gives equation (3) exactly. Both terms on its right are positive in the original acute domain. The decomposition of R in equation (4) is exact.

For `a(z)=asin(s sin z)`, its derivative is positive and at most s because
`cos²z <= 1−s² sin²z`. Integrating from zero proves `A<=sB` and `d<=sg`, and C3 gives `B/g<=(1+cs)/(1−cs)`. The decreasing sine quotient then gives equation (5).

With `X=cot B`, `Y=cot g`, and `v0=1−s²`, expansion of
`sin(B−g)>c sin(A+d)` gives equation (6). Strict sine concavity applies because `0<A+d<pi` and `0<c<1`. Each square root exceeds its positive cotangent, so
`X/Y<(1−cs)/(1+cs)`. Since `c−s>0`, this gives the strict bound on `f tan g` with the correct inequality direction.

### The w bound

Multiplication of the original Q by `tan g` gives exactly

`Q tan g = f tan g − c(1−s²)²w/[1+w+c rho(1+s²w)]`,

where `rho=s cos g/cos d<s`. Replacing rho by s increases the positive denominator, so the subtracted fraction is bounded below, as required for the bound used in the candidate. Rearrangement gives

`(c−s)(1−c²s²) > s P w`.

Independent expansion verifies the displayed polynomial identity defining P. Its derivative in s is `3c[(2+c²)s²−2cs−1]`. The bracket is convex and negative at both endpoints 0 and c; it is therefore negative throughout. Also `P(c,c)=(1−c²)(1−c⁴)>0`. Thus division by `sP` is valid and `w<W` is strict. There is no hidden sign condition.

Combining this bound with equation (5) gives exactly the ratio in Section 3. Positivity of E makes that ratio less than 1. The small-s Bernstein identity and all its positive coefficients were independently checked below.

### Cotangent inversion and argument bounds

Q>0 implies f>0, because the term subtracted from f is positive. Squaring `cX>s sqrt(X²+v0)` is legitimate because both sides are positive; it gives the asserted strict X bound.

Both functions `y−cs sqrt(y²+v0)` and `x+cs sqrt(x²+v0)` are strictly increasing. For the first, the derivative is greater than `1−cs>0`. The stated positive inverse follows by solving the quadratic and retaining the branch `y−h>0`. To verify the displayed closed form for Y0 directly, with `delta=c²−s²` and `J=1−c²s²`, the radical simplifies through the exact identity

`s²(1+c²)² + J delta = c²(1+s²)²`.

All square roots use positive branches, and the inverse's argument is positive. Therefore `Y>Y0` and `ell=Y^(−2)<Lambda` have the correct strict orientation.

From `w=k sin²g` and `ell=tan²g`, one obtains exactly

`z²=w+(1+w)ell`,

`t²=s²[w+(1+w)ell]/[1+(1−s²)ell]`.

The derivatives with respect to w are positive. The derivative of the second expression with respect to ell is `s²(1+s²w)/[1+(1−s²)ell]²>0`; the first expression is also strictly increasing. Consequently the strict inequalities `z²<Z` and `t²<D_*` follow. Substitution of the rational expressions for W and Lambda yields precisely all numerators and denominators in equation (13).

## Exact computational audit

The embedded complete verifier was run successfully with Python 3.14.4, using exact `Fraction` arithmetic. It printed exactly the manifest-listed output. No assertion was bypassed and no floating-point arithmetic was used.

A separate implementation then verified the certificate by **exact interpolation**, rather than the candidate's sparse-polynomial substitution and monomial-to-Bernstein conversion. For a polynomial of bidegree at most (n,m), its exact values at `(i/n,j/m)` determine it uniquely. We formed the Bernstein evaluation matrices at these nodes, inverted them by rational Gauss–Jordan elimination, and recovered the coefficient matrix from `V=B_n C B_m^T`. This checks the global polynomial representation, not merely its signs at sample points.

The degree bounds used in this independent method were checked algebraically:

- E has s degree at most 5. Its only potential c-degree-5 terms cancel, leaving c degree at most 4.
- The complementary Z polynomial has c degree at most 9, s degree at most 12, and total degree at most 19.
- The complementary D-star polynomial has c degree at most 9, s degree at most 13, and total degree at most 19.
- Substitution `c=a+(b−a)u`, `s=h+(c−h)v` therefore gives bidegrees at most (19,12) and (19,13). The rectangular substitution in row 3 gives bounds (9,12) and (9,13).

Thus the interpolation computations determine the exact polynomials on their whole domains. Their coefficient counts were:

| Table row | Z coefficients | Z zeros | D-star coefficients | D-star zeros |
|---|---:|---:|---:|---:|
| 1 | 260 | 0 | 280 | 0 |
| 2 | 260 | 0 | 280 | 0 |
| 3 | 130 | 0 | 140 | 0 |
| 4 | 260 | 6 | 280 | 6 |

All 30 small-s coefficients agreed exactly with equation (8) and were positive. All 1,890 complementary coefficients were nonnegative, with exactly 12 zeros and 1,878 positive coefficients. The SHA-256 of the ordered complementary coefficients, serialized as reduced Python fraction strings separated by newlines with a final newline, is `d143cc7132405be4ab147b06982774841f30bf6048078ff0a52ca974a5b2f11c`.

The independent checker is embedded at the end of this report for replay. It uses no part of the candidate verifier's polynomial implementation.

## Angular contradiction audit

The four parameter rows exhaust `12/25<=s<c<1`, `c>2/3`, including their shared endpoints. The table bounds together with `z²<Z` and `t²<D_*` give strict upper bounds for both acute H arguments.

The global tangent-line estimate for arctangent follows from its nonpositive second derivative on `[0,infinity)`. The polynomial upper estimate follows from
`(1+x²)(1−x²+x⁴)=1+x⁶`; its integrated inequality is strict at every positive upper endpoint. The polynomial lower estimates used for pi follow from the corresponding even-length geometric sums, with strict integrated inequalities.

Using the lower c endpoint in each row is valid because arctangent is positive and `1/c` decreases. Independent rational recombination gives the four constants in equation (11), namely `153/400`, `153/350`, `1243/2400`, and `29/60`, with pi coefficients `3/8`, `5/14`, `1/3`, and `1/3`.

The positive-branch addition formula gives `atan(1/2)+atan(1/3)=pi/4`: the tangent of the sum is 1, and the sum lies in `(0,pi/2)`. The stated lower bound equals `284663/90720>25/8`. Each of the four upper expressions in (11) is strictly below pi/2 using only this lower bound. Thus the contradiction to the exact C2 equality is valid.

## Boundary and adversarial audit

All quantities divided by are strictly positive in the original domain: s, c−s, c+s, `1−cs`, `1−c²s²`, `1−s²`, P, both Q denominator terms, `c²−s²`, and the denominators in (9) and (13). The cotangents and tangent multipliers are positive. No squaring or inversion discards a branch or reverses an inequality incorrectly.

The closed rectangles and triangles used for polynomial certification include boundary points where a rational denominator could vanish, such as c=s=1. This causes no gap: only the numerator polynomials are certified on those closed sets, and division occurs solely in the original open domain. The 12 zero Bernstein coefficients are compatible with nonnegative polynomial bounds; strictness needed in the argument comes earlier from Q>0 and the strict cotangent/argument bounds. The small-s certificate is strictly positive even on its closed rectangle.

The original exclusions `s=0`, `s=c`, `c=1`, `m=1`, `g=0`, and `B=pi/2` remain exclusions. Arbitrarily close approaches to them are covered without any uniform denominator lower bound. The split at s=12/25 has overlap and no uncovered equality case. The proof never infers universal truth from the earlier numerical searches.

## Verdict and residual risk

Definition audit: PASS. Logic audit: PASS. Boundary audit: PASS. Adversarial audit: PASS. Critical errors: none. Load-bearing gaps: none. Repair obligations: none.

The covered scope is all of Q9's original domain and all load-bearing mathematical and rational-certificate dependencies of this frozen candidate. The optional Lean obligation in the frozen graph is explicitly not a root dependency. Lean was unavailable and was not run; this is an independently audited proof, not a Lean formal verification. Ordinary interpreter/integer-arithmetic reliability is part of the exact computation's trusted base. External novelty was not assessed. These limitations do not leave a mathematical obligation open in the presented proof.

## Independent exact interpolation checker

```python
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
```

The standalone copy of the independent checker is `runs/q9/reproducibility/independent_audit_checker.py` (SHA-256 `76f3f9f855a6f289729a3b5865ee0f06ddff9cbca36e93c933f6857efc65825f`). The exact replay command is `python3 runs/q9/reproducibility/independent_audit_checker.py`; its recorded stdout is `runs/q9/reproducibility/independent_audit_output.txt` (SHA-256 `00fb3f10cd0a01c64d18d7edcede6814791a2b1187d1483d10c01917763ebd12`). This command was executed successfully with exit code 0.

## Deterministic metadata correction — 2026-09-08T13:55:58.898381+00:00

The current completion manifest has SHA-256 `04a7643f3e546e359bb35a1d0663e4e025318ee83229f76795dd58b857283567` and freeze timestamp `2026-09-08T13:54:33.617629+00:00`. Its paths now resolve relative to `runs/q9`, and its root proof anchor is `../../answer.md#q9-is-true`. The obligation graph differs from v1 only in that same root anchor. Exact structural comparison verified that the manifest changes comprise only these path/anchor corrections, the corresponding graph hash, and the new freeze timestamp. Every corrected path resolves to the stated content hash.

The proof and certificate bytes are unchanged. The original mathematical PASS, covered scope, and residual risk are therefore preserved; no proof or coefficient computation was repeated for this correction. The original audit is preserved at `runs/q9/audit_v1/completion_audit.json`, SHA-256 `ca35fb1ab726b3c03a9e212f97225f6703cf99c80a8e964b13c7c648bd69608d`, together with the original manifest and graph. This note records deterministic rebinding of the same independently audited proof, not a second mathematical audit.
