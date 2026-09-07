# Problem contract

Authoritative source: workspace `TASK.md`, frozen calibration task B3 O3 root count.
Contract version: 1. Research date: 2026-09-07.

## Objects and definitions
For each integer n >= 1 and real R > 1, put s = sqrt(R) > 1. For real y let
c = cos(y), q = sin(y), E = [[c,q],[-q,c]], and
C = [[c^2-q^2/s,(1+1/s)cq],[-(1+s)cq,c^2-sq^2]].
Define G(y) = (E C^n)_{12}. For -1 < x < 1 define
Q(x) = G(arccos(x))/sqrt(1-x^2).

## Hypotheses and quantifiers
Uniformly for every integer n >= 1 and every real s > 1; no boundedness or
genericity assumption on n or s is permitted.

## Target conclusion
G has exactly 2n distinct zeros in (0,pi), each with nonzero y derivative.
If a polynomial reduction is used, prove its equality with Q on (-1,1),
polynomial extension, degree, root location, and simplicity.

## Boundary and degenerate cases
Audit n=1, y=0, y=pi, y=pi/2, and R=1 separately. Endpoint zeros are excluded
from the count. R=1 is an auxiliary boundary audit, not a changed hypothesis.

## Answer space and completion criteria
An affirmative uniform exact proof, a rigorous disproof, or the strongest exact
partial theorem with the first unresolved obligation. All dependencies and
changes of variables must have checked hypotheses. Root pairing alone, a
degree bound alone, finite scans, or numerical evidence do not complete this task.
Deliver a self-contained proof in answer.md and the final response.

## Equivalent formulation
To be established: Q(x)=U_n((Kx^2-h)/2)+s^(-1)U_{n-1}((Kx^2-h)/2),
where h=s+s^(-1), K=h+2, U_0=1, U_1=2z, U_m=2zU_{m-1}-U_{m-2}.
This identity is a proof obligation, not an assumed reformulation.

## Tool, citation, and search constraints
Blind discovery only. No internet, other projects, prior solutions, sessions,
memory, repository inspection, or git history. Installed skill instructions
may be read as explicitly requested. No post-discovery literature search or
novelty claim. Scratch exact algebra may falsify identities but does not replace
the uniform proof. Remaining shared wall budget on resume: 1788 seconds;
start final consolidation no later than 25 minutes of the original 30 minutes.

## Contract audit
Coordinator pass: definitions, quantifiers, interval, derivative meaning, and
all five requested special cases match TASK.md. No ambiguity requires input.
Independent fidelity review is included in the fresh completion audit.
