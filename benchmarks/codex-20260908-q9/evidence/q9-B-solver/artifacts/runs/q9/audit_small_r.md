RIGOROUS_PARTIAL_RESULT

# Independent claim-local audit of the small-r theorem

**Verdict: PASS for the stated theorem.** On the task domain, C2 and C3 together with `0<r<=c^2/4` imply the strict inequality `c^2-r>k(1-c^2)r sin(B)^2` and hence `R_quad>0`, independently of Q and without using C1.

## Input binding and scope

- `TASK.md`: SHA-256 `c7133b97e440e90095088927f105c9f88fcdc54f4a4772ee9f85ba5a139e6330`.
- `runs/q9/partial_small_r.md`: initially reviewed SHA-256 `3172c3b3000a121fa647003f053bb2facb5d4cce4266dae03019a32dffa3f706`.

The mathematical proof was independently reconstructed from these inputs under the installed rigorous-open-math-research audit instructions. No external mathematical sources or floating-point results were used. This is a separate claim-local audit; it does not alter the initial algebraic theorem's frozen audit.

## C2 and strict convexity

Put `t=sqrt(r)>0`, `s=sin(g)>0`, `p=sin(B)>0`, `e=1-c^2>0`, and `y=pi/2-H(d)`. Since `0<d<pi/2` and `m>1`, `0<H(d)<pi/2`, so `0<y<pi/2`. C2 is exactly `H(g)=c y`.

The function tan is strictly convex on `[0,y]`: its second derivative is `2 sec(z)^2 tan(z)>0` for `0<z<y`. Since `0<c<1`, strict convexity between the distinct endpoints zero and y gives

`tan(c y)<c tan(y)`.

Using the principal-branch identities `tan(H(g))=m tan(g)` and `tan(H(d))=m tan(d)`, this is

`m tan(g)<c/(m tan(d))`.

Every multiplier and denominator is strictly positive. Since `sin(d)=t sin(g)`, multiplying through gives

`m^2 t s^2<c cos(g)cos(d)<c`.

In particular, `(m^2-1)s^2<m^2 s^2<c/t`, hence `k s^2<c/t`. There is no lost orientation or tangent-period ambiguity.

## C3 and the sine ratio

From `0<r<c^2<1`, we have `0<t<1`. Concavity of sine on `[0,pi/2]`, applied to `t z+(1-t)0`, gives `sin(t z)>=t sin(z)`. Both `t z` and z lie on the principal increasing sine interval, so applying arcsine yields

`asin(t sin(z))<=t z`.

Apply this for z equal to B and g. C3 then implies

`B-g=c(A+d)<=ct(B+g)`.

Because `ct<1` and `g>0`, rearranging and dividing preserves the inequality:

`B/g<=(1+ct)/(1-ct)`.

Independently, the derivative of `sin(z)/z` has numerator `z cos(z)-sin(z)`. The opposite numerator vanishes at zero and has derivative `z sin(z)>0` for positive z. Thus `sin(z)/z` strictly decreases on `(0,pi/2)`. Since the original domain has `B>g>0`,

`p/s<B/g<=(1+ct)/(1-ct)`.

Combining the two positive strict bounds yields

`k e t^2 p^2=e t^2 (k s^2)(p/s)^2`

`             <e c t ((1+ct)/(1-ct))^2`.

This step uses exactly C2, C3, and the domain, and does not depend on C1 or Q positivity.

## Uniform estimate for t<=c/2

For fixed `c>0`, the ratio `(1+ct)/(1-ct)` is positive and strictly increasing on `0<t<1/c`; its derivative is `2c/(1-ct)^2>0`. Consequently its square times the positive increasing factor t is increasing there. Under the stated extra assumption, `t<=c/2` and `c^2<1`, so all arguments lie strictly below `1/c`. Therefore

`k e r p^2 < e c^2/2 ((1+c^2/2)/(1-c^2/2))^2`.

For `x=c^2 in (0,1)`, direct expansion gives the exact identity

`3(2-x)^2-2(1-x)(2+x)^2`

`=4-12x+9x^2+2x^3=(3x-2)^2+2x^3>0`.

The last inequality is strict even at `x=2/3`, because `x>0`. Dividing by the positive quantity `4(2-x)^2` gives

`(1-x)/2 ((2+x)/(2-x))^2<3/4`.

Multiplication by `c^2>0` proves

`k e r p^2<3c^2/4<=c^2-r`,

where the last step is precisely `r<=c^2/4`. This verifies the claimed strict sufficient condition, including the boundary `r=c^2/4`.

## Conversion to R and independence from C1

There is no hidden C1 hypothesis in the supplied bound on T. Directly from the definitions,

`V=pi-H(B)+H(g)+m(B-g)>0`,

and

`V sin(B)^2-U=H(g)(sin(B)^2-sin(g)^2)+m(B-g)sin(B)^2>0`.

Also `U>0`. Hence `0<T_quad=r U/V<r sin(B)^2` on the original domain alone. Since `k e>0`, the just-proved sufficient inequality gives

`k e T_quad<k e r sin(B)^2<c^2-r`.

Multiplying by `V>0` yields `R_quad>0`, as claimed. The sign of Q is irrelevant throughout this proof.

## Verification, interpretation, and residual risk

All algebra, strict signs, derivative claims, reciprocal operations, and endpoint cases used in the proof were checked independently. The polynomial identity was additionally checked by exact integer-coefficient polynomial multiplication in ordinary Python; both sides have coefficient vector `[4,-12,9,2]` in ascending powers of x. This is an exact algebra check, not sampling.

There are no gaps in the theorem. Its new contribution relative to the supplied facts is a proved parameter-only sufficient range derived from C2 and C3. Its formula imposes no m-dependent condition and its conclusion assumes no sign of Q.

The initial draft's final comparison sentence, concerning arbitrarily large `k e r` at fixed `(c,r)`, is valid as an observation about the unrestricted algebraic parameters. This audit does not interpret it as an additional existence theorem asserting exact C1--C3 solutions at those fixed parameters for arbitrarily large m, or as certification of a nonempty difference from the first partial range. Neither additional existence claim is proved in this candidate, and neither is needed for the audited small-r theorem. The parent was advised to phrase the comparison in terms of the restrictions appearing in the two sufficient conditions.

The audit does not settle global Q9 for `r>c^2/4`, prove existence of all parameter choices admitted by this range, establish external novelty, or provide Lean/kernel verification. No broader conclusion is licensed by this PASS.
