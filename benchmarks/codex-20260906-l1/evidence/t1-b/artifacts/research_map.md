# Research map: B3 O3 root count

- Source and target: TASK.md, exactly 2n simple interior zeros for all n>=1,R>1.
- Route R1 [SUCCEEDED, independently audited PASS]: determinant-one
  matrix recurrence -> U_n+s^(-1)U_{n-1} -> alternating signs -> root pullback.
- Exact finding: all polynomial zeros satisfy
  (s-1)/(s+1) < |x| < 1; degree is 2n and leading coefficient is (s+2+s^(-1))^n.
- Boundary findings: G(pi/2)=(-s)^n; Q(1)=Q(-1)=n+1+n/s;
  R=1 gives G(y)=sin((2n+1)y).
- Failed or blocked routes: none; no alternative route was opened.
- Avoid list: numerical scans as proof, endpoint counting, unproved polynomial
  equivalence, repository or literature retrieval, extra research after closure.
- Contributions: user supplied frozen task and restrictions; /root derived
  the candidate. The fresh independent verifier passed every frozen obligation (completion_audit.json). Research is STOP.
- Key artifact: runs/rigorous-open-math-research/b3-o3/candidate_proof.md.
