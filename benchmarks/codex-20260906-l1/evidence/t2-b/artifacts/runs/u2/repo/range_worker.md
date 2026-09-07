# L2 range worker: active research artifact

Status: CANDIDATE_COMPLETE_PROOF for delegated L2, awaiting fresh independent audit. No global task completion claim. Earlier route entries below are historical.

Owner: `/root/range_worker`. Frozen parent contract: `runs/u2/problem_contract.md`, SHA256 `605926692a3192c43d7e3e7521c32529b4bc2265125c706070467dbc3989ee71`.

Exact obligation L2: for simple symmetric nearest-neighbor walks from 0 and 2, bound the total variation distance of `(minimum through t, maximum through t, endpoint at t)` by an explicit `C/sqrt(t)`, uniformly over sufficiently large integer t of both parities.

Allowed inputs: the frozen statement, this run's artifacts, and installed skill instructions. No internet, repository/history inspection, external memory, or prior solutions. No additional workers. Scratch computation can falsify claims only.

## Route record, 2026-09-07 13:22 UTC

`route_key: range_triple_translation_gradient`. Mechanism: a path-level cancellation or an explicit discrete derivative bound for the joint extrema/endpoint law. Target: L2 only. First deliverable: an exact identity or coupling whose failure has a direct `t^(-1/2)` estimate.

The naive reflection coupling at the first meeting at 1 has a specific obstruction: if the premeeting minimum of the 0-start walk is m, the reflected histories together occupy `[m,2-m]`, and common later motion must cover both historical extremes. The premeeting depth has a harmonic tail; the crude expected-depth estimate produces a logarithmic loss. This is only an obstruction to that estimate, not a disproof of the desired bound.

Next action: seek a finite-measure path reflection/surgery for joint extrema, or an explicit absolutely summable derivative formula. No external theorem is being invoked.

## Material progress, 2026-09-07 13:29 UTC

The analytic route now has a specific mechanism avoiding the logarithmic loss. Split interval lengths at `sqrt(t)`. For short intervals, use a parity-reduced sine expansion of the killed walk and differentiate its continuous extension three times (initial point, lower barrier, upper barrier). For long intervals, use images and third finite differences of the free heat kernel. The long-interval image arguments are at least a constant times `|k| L`; hence the image sums are absolutely summable in this regime. The short-interval spectral factor supplies the cancellation unavailable in absolute image bounds.

The following explicit short-interval bound has been derived, pending complete write-up and parent audit: for `t>=1024`, `2<=L<=sqrt(t)`, and coordinates `x,y` in `[0,L]`, the continuous parity-reduced spectral kernel satisfies `|partial_s partial_a partial_b H| <= 10^9/t^2`. The image route reduces to the centered third-difference estimate `|p_t(w-3)-3p_t(w-1)+3p_t(w+1)-p_t(w+3)| <= 10000 t^(-2) exp(-w^2/(16t))`, for `w=t+3 mod 2`. This helper has been sent to the parent as an independently checkable sub-obligation.

# Candidate proof of L2

**Claim.** Let `(m_t,M_t,S_t)` be the minimum, maximum, and endpoint of a simple symmetric nearest-neighbor walk through time t. For walks started respectively at 0 and 2,

`TV(Law_0(m_t,M_t,S_t), Law_2(m_t,M_t,S_t)) <= 10^12 / sqrt(t)`

for every integer `t>=1024`. Both time parities are included. This is a candidate complete proof of the delegated L2 only. The root supplied the free-kernel helper in §1; the range worker independently checked it and reproduces its elementary proof in §6. No claim about global task completion is made here.

## 1. Free-kernel helper and elementary boundary bound

Write `p_t(v)=P_0(S_t=v)`, zero when v is inaccessible. The free-kernel helper used below is

`|p_t(w-3)-3p_t(w-1)+3p_t(w+1)-p_t(w+3)| <= 10000 t^(-2) exp(-w^2/(16t))`  (H)

for integer `t>=3` and `w=t+3 mod 2`. Its proof is given in §6. Provenance: the root's `runs/u2/repo/binomial_difference_helper.md`, SHA256 `9e06455a4e7185adb938bf4fdcf24668e012ca202f94ecf5d1c5d709ece9b96a`, independently checked by the range worker before integration.

For later boundary terms, `sup_v p_t(v) <= sqrt(2/t)` for `t>=1`. Indeed binomial coefficients are unimodal by the ratio of consecutive coefficients. At even time `2n`, their maximum is `p_(2n)(0)=product_(j=1)^n (2j-1)/(2j) <= (n+1)^(-1/2)`. The last inequality follows by induction, since `(2n+1)^2(n+2) <= 4(n+1)^3` (the difference is `3n+2`). The odd-time maximum equals `p_(2n+2)(0)` and satisfies the same claimed bound. Reflecting the path after its first hit on 2 is a bijection between paths with `M_t>=2,S_t<2` and paths with `S_t>2`; thus

`P_0(M_t<=1)=P_0(-2<=S_t<2) <= 2 sup_v p_t(v) <= 3/sqrt(t)`.

Only two accessible parity sites occur in the half-open interval `[-2,2)`.

## 2. Exact killed kernels and their two representations

For integer `a<=b`, define

`K_t(a,b;s,z)=P_s(S_t=z and a<=S_i<=b for 0<=i<=t)`.

Let `L=b-a+2`, `x=s-a+1`, and `y=z-a+1`. In the interior `1<=x,y<=L-1`,

`K_t = (2/L) sum_(j=1)^(L-1) cos(pi j/L)^t sin(pi j x/L) sin(pi j y/L)`.  (S)

For completeness, on the states `1,...,L-1` with zero values at 0 and L, the one-step killed transition operator sends the vector `sin(pi j r/L)` to `cos(pi j/L) sin(pi j r/L)` by the sine addition identity. Their squared norms are `L/2`, and distinct such vectors are orthogonal; these finite sum identities follow by summing the geometric series for `exp(i pi k r/L)` (or by summing `2 sin A sin B=cos(A-B)-cos(A+B)`). There are `L-1` nonzero orthogonal vectors, hence they are a basis. Expanding the t-th matrix power proves (S). This argument invokes no spectral estimate beyond finite-dimensional orthogonal expansion.

When `z-s=t mod 2` and `t>=1`, pair j with `L-j`. The product of its three sign changes is `(-1)^(t+x+y)=1`; the unpaired middle term, when present, is zero. Consequently (S) equals the following extension at its integer arguments:

`H_t(a,b;s,z) = (4/L) sum_(j>=1) g_t(pi j/L) sin(pi j x/L) sin(pi j y/L)`,

where `g_t(theta)=cos(theta)^t` for `0<=theta<=pi/2` and `g_t(theta)=0` for `theta>pi/2`. The sum is finite locally in real `L>0`. For `t>=4`, `g_t` is twice continuously differentiable across the cutoff. Thus the mixed derivatives used below exist. The formula also vanishes when x or y is 0 or L, as does the killed kernel evaluated at a boundary point.

The second representation is the image formula

`K_t(a,b;s,z) = sum_(k in Z) [p_t(z-s+2kL)-p_t(z+s-2a+2+2kL)]`.  (I)

Every sum here is finite because `p_t` has finite support. To prove (I), its right side satisfies the free nearest-neighbor recurrence in z, vanishes at the two absorbing sites `a-1,b+1` by symmetry of `p_t` and reindexing k, and at time zero equals the point mass at s in the interior. Induction on time uniquely determines the killed transition probabilities. The same image expression is zero when s or z is an absorbing boundary point; this also follows directly by the same symmetry/reindexing. This covers all contracted-interval evaluations below.

Write

`q_s(a,b,z)=P_s(m_t=a,M_t=b,S_t=z)`.

Inclusion-exclusion gives the exact identity

`q_s(a,b,z)=K_t(a,b;s,z)-K_t(a+1,b;s,z)-K_t(a,b-1;s,z)+K_t(a+1,b-1;s,z)`.  (Q)

The terms are defined as zero when their s or z lies outside the contracted interval. In our applications s or z can only be on that interval's absorbing boundary, so both representations above still apply.

## 3. Short intervals: uniform third derivative

Suppose `t>=1024`, `2<=L<=sqrt(t)`, and `0<=x,y<=L`. Then

`|partial_s partial_a partial_b H_t| <= 10^9 t^(-2)`.  (D)

Here derivatives treat a,b,s,z as real variables. To prove the bound, for one summand set `theta=pi j/L`, `h=g_t(theta)`, `d=pi j`, `v=t theta^2`, and

`F=L^(-1) theta h cos(theta x) sin(theta y)`.

The s derivative of that summand of H is `4F`. In the independent coordinates `(L,x,y)`, the other operators are `partial_a=-(partial_L+partial_x+partial_y)` and `partial_b=partial_L`. On `0<=theta<=pi/2` the elementary inequality `cos(theta)<=exp(-theta^2/2)` follows by integrating `tan(theta)>=theta`. Direct differentiation gives, for `t>=4`,

`|h|<=exp(-v/4)`,

`|h'|<=t theta exp(-v/4)`,

`|h''|<=t(1+v) exp(-v/4)`.

All three are zero beyond the cutoff, and the bounds extend continuously to it.

Here are explicit derivative estimates so that no regularity estimate is hidden. Put `f(theta)=theta h cos(theta x) sin(theta y)`. Since `F=L^(-1)f(theta)`,

`partial_L F=-L^(-2)(f+theta f')`,

`partial_L^2 F=L^(-3)(2f+4theta f'+theta^2 f'')`.

For `R=cos(theta x)sin(theta y)`, one has `|R|<=1`, `|R'|<=2L`, `|R''|<=4L^2`. Expanding the last display and substituting the h bounds yields

`|partial_L^2 F| <= L^(-4) exp(-v/4) [6d+12d^2+4d^3+(7d+4d^2)v+d v^2]`

`<=34 L^(-4) d^3(1+v)^2 exp(-v/4)`.

Likewise, differentiating `partial_L F` in x gives the bound

`|partial_x partial_L F| <= L^(-4) exp(-v/4)[3d^2+2d^3+d^2 v] <=6 L^(-4)d^3(1+v)^2 exp(-v/4)`,

and the same inequality holds for y. The facts `d>=pi>1` justify the loose last inequalities. Multiplying their sum by 4 gives

`|partial_s partial_a partial_b H_t| <=200 L^(-4) sum_(j>=1) d^3(1+v)^2 exp(-v/4)`.

Let `u=t/L^2>=1`, so `v=u d^2`. After multiplying by `t^2`, the summand becomes

`u^2 d^3(1+v)^2 exp(-v/4) = d^(-1) v^2(1+v)^2 exp(-v/4)`.

For `v>=0`,

`v^2(1+v)^2 exp(-v/8) <=2[(16)^2+(32)^4] <3*10^6`,

using `(1+v)^2<=2(1+v^2)` and `sup_(v>=0) v^r exp(-v/8) <=(8r)^r` for r=2,4 (obtained by differentiation). Also `v>=pi^2 j^2`, so

`sum_(j>=1) d^(-1) exp(-v/8) <= sum_(j>=1) exp(-pi^2 j^2/8) <= integral_0^infty exp(-pi^2 r^2/8) dr =sqrt(2/pi)<1`.

The integral identity follows by squaring the Gaussian integral and using polar coordinates. Thus the derivative bound is at most `6*10^8 t^(-2)`, proving the looser (D).

Now restrict to integer `a<=0,b>=2,z in[a,b]` and `L=b-a+2<=sqrt(t)`. Apply (Q) to H at starts 0 and 2 and use the fundamental theorem of calculus three times, integrating over `s in[0,2]`, `a' in[a,a+1]`, `b' in[b-1,b]`. Throughout this box, `2<=L'=b'-a'+2<=L<=sqrt(t)`, and both `x'=s-a'+1` and `y'=z-a'+1` lie in `[0,L']`. Therefore

`|q_0(a,b,z)-q_2(a,b,z)| <=2*10^9 t^(-2)`.  (SQ)

For each integer L there are at most L choices of a with `a<=0,b>=2`, and at most L choices of z. Hence the total l1 contribution from `L<=sqrt(t)` is at most

`2*10^9 t^(-2) sum_(L<=sqrt(t)) L^2 <=2*10^9 /sqrt(t)`.  (SL)

## 4. Long intervals: images and third differences

Let `D_h f(v)=f(v)-f(v-h)`. Combining (I) and (Q) exactly, at starts 0 and 2, gives

`q_0-q_2 = sum_(k in Z) [D_(2k)^2 D_2 p_t(z+2kL) + D_(2k) D_(2k+2) D_2 p_t(z-2a+4+2kL)]`.  (F)

The plus sign on the second term comes from both subtracting the reflected image and changing its argument by +2 with the start. The first summand vanishes at k=0; the second vanishes at k=0,-1.

For nonzero integer k, `D_(2k)` is a signed sum of `|k|` translates of `D_2`, at shifts of magnitude at most `2|k|`. More explicitly, use shifts `-2r`, with `r=0,...,k-1` when k>0, and `r=k,...,-1` with an overall minus sign when k<0. Thus the first expression in (F) is a sum of `k^2` translates of `D_2^3 p_t`, and the second of `|k(k+1)|` such translates.

The centered argument w for `D_2^3 p_t(v)` is `w=v-3`, and (H) applies in absolute value; it has the required parity because `z=t mod 2`. For endpoints of the other parity both q values vanish.

Assume now `L>sqrt(t)>=32`. For the first expression set `m=|k|>=1`. Since `|z|<=L-2`, every centered argument obeys

`|w| >= (2m-1)L-4m-1 >= mL/2`.

For the second expression set `m=min(|k|,|k+1|)>=1`. Writing `r=1-a` and `y=z-a+1`, one has `1<=r<=L-3`, `1<=y<=L-1`, hence `4<=r+y+2<=2L-2`. Its original argument `z-2a+4+2kL=r+y+2+2kL` has magnitude at least `2mL+2`. The subsequent shifts and centering change it by at most `2|k|+2|k+1|+3=4m+5`. Therefore again

`|w| >=2mL-4m-3 >=mL/2`.

There are two first-image indices for each m, with total multiplicity `2m^2`, and two second-image indices, with total multiplicity `2m(m+1)<=4m^2`. Applying (H) termwise proves

`|q_0-q_2| <=60000 t^(-2) sum_(m>=1) m^2 exp(-m^2 L^2/(64t))`.  (LQ)

All estimates also hold for translated third differences outside the free walk support, where their values are zero. For each finite t the exact pre-estimate sums in (F) contain only finitely many nonzero terms; the displayed majorant is an ordinary convergent nonnegative series.

To sum (LQ), put `X=L^2/t>=1`, `Y=m^2>=1`. The inequality `XY>=(X+Y)/2` gives

`exp(-m^2 L^2/(64t)) <=exp(-m^2/128) exp(-L^2/(128t))`.

For every `T>=1`, comparison on each interval `[n-1,n]` gives

`sum_(n>=1) n^2 exp(-n^2/(128T)) <= integral_0^infty (r+1)^2 exp(-r^2/(128T)) dr`

`= (128T)^(3/2) sqrt(pi)/4 +128T +sqrt(128pi T)/2 <1000 T^(3/2)`.

For example the last numerical bound follows from `sqrt(128)<12`, `sqrt(pi)<2`, and `T>=1`. Therefore, after allowing all positive L in the separated second sum, the total l1 contribution from `L>sqrt(t)` is at most

`60000 t^(-2) (1000)(1000 t^(3/2)) =6*10^10/sqrt(t)`.  (LL)

## 5. Boundary support and final assembly

Outside the common set `a<=0,b>=2`, the q_0 law can occur only when `b<=1`, and the q_2 law only when `a>=1`. The respective total masses are `P_0(M_t<=1)` and `P_2(m_t>=1)`, equal by reflection about 1. Their combined contribution after the factor 1/2 in total variation is at most `3/sqrt(t)` by §1.

Combining (SL) and (LL), and remembering this factor 1/2, gives

`TV <= [3+10^9+3*10^10]/sqrt(t) <10^12/sqrt(t)`.

The time assumption `t>=1024` ensures every long interval used above has `L>=32`; no parity restriction on t was imposed. This completes all interfaces of L2, using the proved helper below.

## 6. Proof of the free-kernel helper (root contribution, checked here)

First, for every integer `N>=1` and every allowed w,

`p_N(w)<=2 N^(-1/2) exp(-w^2/(4N))`.  (G)

The central binomial bound was proved in §1. Put `w0=0` at even N and `w0=1` at odd N, and by symmetry suppose `w>=w0`. For `v<N`, the consecutive mass ratio is

`p_N(v+2)/p_N(v)=(N-v)/(N+v+2)=(1-u)/(1+u)`, `u=(v+1)/(N+1)`.

Differentiation shows `log((1-u)/(1+u))<=-2u` for `0<=u<1`. Multiplying the ratios and summing the resulting arithmetic progression gives

`p_N(w)<=sqrt(2/N) exp(-(w^2-w0^2)/(2(N+1)))`.

Since `2(N+1)<=4N`, `w0^2<=1`, and `exp(1/(2(N+1)))<=exp(1/4)<=4/3`, (G) follows from `(4/3)sqrt(2)<2`. The exponential bound follows directly by comparing its power series with the geometric series. Points outside the support have zero mass.

Let `N=t+3`, and let `xi_1,...,xi_N` be independent uniform signs, with sum S. Conditioning on the first three signs (and using exchangeability to choose those three) gives the exact identity

`D3 p_t(w)=8 p_N(w) E[xi_1 xi_2 xi_3 | S=w]`,

where `D3 p_t(w)=p_t(w-3)-3p_t(w-1)+3p_t(w+1)-p_t(w+3)`.

The pointwise expansion

`S^3=(3N-2)S+sum_(i,j,k all distinct) xi_i xi_j xi_k`

and conditional exchangeability therefore imply

`D3 p_t(w)=8 p_N(w)[w^3-(3N-2)w]/[N(N-1)(N-2)]`.  (E)

This derivation is valid at every allowed point with `|w|<=N`; outside that set both sides are zero, and no conditioning on a null event is used.

For `t>=3`, one has `N>=6`, `N<=2t`, and `N(N-1)(N-2)>=N^3/2`. With `u=|w|/sqrt(N)`, (G) and (E) give

`|D3 p_t(w)|<=32 N^(-2)(u^3+3u) exp(-u^2/4)`.

Differentiation places the maxima of `u^3 exp(-u^2/8)` and `u exp(-u^2/8)` at `sqrt(12)` and 2 respectively. In particular

`(u^3+3u)exp(-u^2/8)<=12sqrt(12)+6<54`.

Thus

`|D3 p_t(w)|<=1728 N^(-2) exp(-w^2/(8N)) <=2048 t^(-2) exp(-w^2/(16t))`,

which is stronger than (H). The parity requirement precisely ensures that all four free-walk arguments have the allowed parity. This also verifies all support boundaries.

## Local audit / exact handoff status

The derivation checked: both walk parities; the factor 1/2 in TV; all supports outside the common interval set; contracted intervals with endpoints on absorbing boundaries; the parity reduction of the sine formula; the sign of the reflected-image start difference; short-interval cutoff regularity; all summation powers and constants. No numerical experiment was used as proof, and no external theorem was cited. The elementary Gaussian integral, finite sine expansion, reflection bijection, and fundamental theorem of calculus have explicit derivations or immediate elementary verification routes above.

Exact currently unclosed local obligations: none identified after attaching and checking the root's helper proof in §6. The full L2 package still awaits a fresh independent audit and is not a global completion claim. The helper itself was independently checked for its mass-ratio exponent, exact cubic identity, denominator estimate, support boundary, parity, and polynomial absorption; no issue was found.

`decision_delta`: the range-triple route advances from the reflection-coupling logarithmic obstruction to an explicit short/long interval kernel proof. The split makes two previously non-summable bounds summable in their respective regimes. Together with the root's elementary third-difference helper, it supplies a candidate complete L2 upper bound with explicit constants and both parities.
