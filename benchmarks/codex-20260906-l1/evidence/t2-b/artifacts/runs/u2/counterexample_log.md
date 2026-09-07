# Exact falsification record

The conjectured unimodality of the interval kernel in the initial point is false. At t=6, require visited interval[0,4] and endpoint2. For starting points0,2,4, path counts are respectively1,0,1 out of64: from0 the only path is0,1,2,3,4,3,2; from4 it is its reflection; from2 any path visiting0 and4 and returning2 needs at least2+4+2=8 steps. This independent path-length argument verifies the small counterexample found by the exact enumeration in reproducibility/falsify_unimodality.py.

The same script searched t=1,...,60 for violations of a proposed numerical constant in the triple-TV bound. Absence of a violation was not treated as proof, and none of its numerical survival data is used in the final result. No other computation was used to prove a mathematical claim.
