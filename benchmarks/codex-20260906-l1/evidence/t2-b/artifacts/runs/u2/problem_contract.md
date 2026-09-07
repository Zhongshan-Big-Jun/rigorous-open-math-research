# Problem contract

Authoritative input: the user's frozen U2 total-variation task, received 2026-09-07.

For the discrete-time switch-walk-switch lamplighter chain on Z_2 wr Z, each step independently resets the departing lamp and arriving lamp to independent fair Bernoulli bits and makes a nearest-neighbor symmetric base step. Initial states are x=(all-zero lamps,0), y=(all-zero lamps,2). Prove explicit c,C>0 and integer t0 such that c/sqrt(t) <= TV(P_t^x,P_t^y) <= C/sqrt(t) for every integer t>=t0. TV means half the l1 distance, or supremum over events.

Both initial configurations are exactly zero. The second initial state does not mean a lit lamp at 2. Base parity is t mod 2 from either start. At t=0 there are no resets; for t>=1 every visited site is reset. Constants must hold simultaneously for even and odd times. Completion requires both bounds and a justified full-chain upper bound, including all conditioning and coupling laws.

Permitted outcomes: a complete self-contained proof, a counterexample, or the strongest exact partial theorem with its first unresolved obligation. No numerical evidence, recalled unverified theorem, changed lamp convention, or asymptotic heuristic is a proof.

Constraints: blind discovery only. No internet, repository or git inspection, prior solutions, external memory, sessions or other projects. Installed skill instructions are allowed by the explicit request. Scratch computation only for falsification. Total wall budget 30 minutes from 13:19:02 UTC; final consolidation by 13:44:02 UTC; hard stop 13:49:02 UTC. No further research after audited completion.

Contract audit: the two starts differ by an even base translation, both have identical all-zero lamp configurations; all t are integer and no periodicity obstruction is hidden. No ambiguities remain.
