# Analytic route subclaim O3-F (owner fourier_lemma)

For every integer t>=32, define the real smooth interpolation
f_t(x)=(1/pi) integral_{-pi/2}^{pi/2} cos(theta)^t exp(i*x*theta) dtheta, x real.
Prove an explicit universal A such that
|f_t'''(x)| <= A*t^(-2)*(1+|x|/sqrt(t))^(-6).
Only exact symbolic inequalities; numerical computations may only falsify. No external sources or repositories. State external calculus/Fourier results exactly or derive them.

Direct root attempt: raw integral and cos(theta)<=exp(-theta^2/2) give A*t^-2 without spatial decay. Integrating by parts six times on theta^3*cos(theta)^t should give A*t/|x|^6. For t>=32 endpoint derivatives through order5 vanish. Need explicit bound on L1 norm of sixth derivative, uniformly <=A*t. Combining estimates gives desired bound. Probe: t=0 is invalid; choose t>=32 to eliminate endpoint regularity issues. This lemma closes only Fourier-decay subclaim, not the whole upper bound. Root concurrently proves small-interval spectral derivative bound and assembly. Worker return can close this named derivative estimate or give first unsupported step. Deadline05:13 UTC, stop after proof. Save runs/u2/fourier_lemma.md.
