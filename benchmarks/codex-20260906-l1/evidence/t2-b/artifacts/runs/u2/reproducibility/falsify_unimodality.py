from collections import defaultdict
from fractions import Fraction
from pathlib import Path
states={(0,0,0):1}
findings=[]
for t in range(1,61):
    nxt=defaultdict(int)
    for (m,M,z),n in states.items():
        for w in (z-1,z+1):
            nxt[min(m,w),max(M,w),w]+=n
    states=nxt
    H=defaultdict(dict)
    for (m,M,z),n in states.items(): H[M-m,z-m][-m]=n
    if not findings:
        for (L,w),col in H.items():
            seq=[col.get(s,0) for s in range((w-t)%2,L+1,2)]
            directions=[(b>a)-(b<a) for a,b in zip(seq,seq[1:]) if b!=a]
            if any(a==-1 and b==1 for a,b in zip(directions,directions[1:])):
                findings.append({'claim':'Every H_t^L(s,w) is unimodal in s along the allowed parity','counterexample':{'t':t,'L':L,'w':w,'counts':seq,'denominator':2**t}})
                break
    diff=defaultdict(int,states)
    for (m,M,z),n in states.items(): diff[m+2,M+2,z+2]-=n
    tv=Fraction(sum(abs(v) for v in diff.values()),2**(t+1))
    # Test the explicit proposed estimate TV <= 4/sqrt(t) by exact squaring.
    if t*tv*tv>16:
        findings.append({'claim':'TV triple <= 4/sqrt(t)','counterexample':{'t':t,'tv':str(tv)}})
        break
Path('runs/u2/repo/falsification_results.json').write_text(__import__('json').dumps({'purpose':'Falsification only; absence of a counterexample is not proof.','tested_times':[1,t],'findings':findings},indent=2)+'\n')
print(__import__('json').dumps({'tested_times':[1,t],'findings':findings}))
