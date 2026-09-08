# Independent audit of the unconditional small-r lemma

I checked the proof in `analytic_notes.md` of the following statement: on the task's domain, C2 and C3 imply `R_quad>0` whenever `r<=1/9`, without any Q hypothesis.

- C2 gives `H(g)=c(pi/2-H(d))`; strict convexity of tangent on the relevant positive interval gives `m² tan(g)tan(d)<c`. Therefore `m² r sin²(g)<c sqrt(r) cos(g)cos(d)<c sqrt(r)`.
- For `s=sqrt(r)`, the derivative of `asin(s sin z)` is strictly less than s for positive acute z; C3 therefore yields `B/g<(1+cs)/(1-cs)`. Decrease of `sin(z)/z` supplies the same strict upper bound for `sin B/sin g`.
- Combining the two estimates yields `k(1-c²)r sin²B < (1-c²)c s[(1+cs)/(1-cs)]²`.
- The normalized ratio G in the note is increasing in s. Its logarithmic c derivative is exactly
  `(1-3c²)/(c(1-c²)) - 2c/(c²-s²) + 4s/(1-c²s²)`.
  On `c>=2/3`, `s<=1/3`, these three terms are respectively negative, strictly below -2, and at most 3/2. Thus G decreases in c.
- The corner value is `G(2/3,1/3)=1210/1323<1`. The strict supplied sufficient inequality follows.

All divisions are positive on the stated domain. The endpoints used only for monotonic comparison are legitimate. No unproved numerical statement is used in this lemma.
