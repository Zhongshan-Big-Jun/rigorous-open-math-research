# Completed algebraic observations

Throughout, put `a=H_m(A)`, `b=H_m(B)`, `h=H_m(d)`, and `j=H_m(g)`.
The following observations are exact, not numerical evidence.

1. The supplied sufficient inequality is equivalent to
   `sin(a) <= c sin(b)`.
   Indeed `sin(H_m(z)) = m sin(z)/sqrt(1+k sin(z)^2)` on the acute domain, so
   `sin(a)^2/sin(b)^2 = r(1+k sin(B)^2)/(1+k r sin(B)^2)`.
   Comparing this positive ratio with `c^2` and multiplying by its positive
   denominator gives `c^2-r >= k(1-c^2)r sin(B)^2`.

2. All three constraints imply
   `V=c[3 pi/2-F_m(A)-F_m(d)]`.
   In fact C1 and C2 give
   `pi-H_m(B)+H_m(g)=c[3 pi/2-H_m(A)-H_m(d)]`, and C3 supplies
   `m(B-g)=mc(A+d)`.

3. Q positivity requires `c cos B > sqrt(r) cos A`, since its subtracted
   term is strictly positive. Squaring these positive quantities gives
   `c^2-r > (c^2-r^2) sin(B)^2`.
   Consequently Q9 holds if `k(1-c^2)r <= c^2-r^2`, and in particular if
   `1<m<=sqrt(2)`: here `k<=1` and
   `c^2-r^2-(1-c^2)r=(c^2-r)(1+r)>0`.
   This is a proved subdomain implication beyond the supplied sufficient
   condition, because Q positivity itself forces that sufficient condition
   in this stated parameter range. See structure_notes.md for nonemptiness.
