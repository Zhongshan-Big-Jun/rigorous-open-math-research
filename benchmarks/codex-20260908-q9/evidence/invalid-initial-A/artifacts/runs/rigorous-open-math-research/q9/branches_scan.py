"""Independent binary64 discovery scan, never an exact Q9 certificate.

H-coordinates impose C1/C2, eliminate m via the common sine ratio,
then solve C3 in alpha. Run from workspace root.
"""
import math, json, random, sys
P=math.pi

def bisect(f,a,b,n=55):
    fa,fb=f(a),f(b)
    if fa is None or fb is None or fa*fb>0:return None
    for _ in range(n):
        z=(a+b)/2; fz=f(z)
        if fz is None:return None
        if (fz>0)==(fa>0):a,fa=z,fz
        else:b,fb=z,fz
    return (a+b)/2

def coords(c,delta,alpha,quality=False):
    beta=(1-c)*P+c*alpha; h=c*(P/2-delta)
    if not(0<delta<alpha<beta<P/2 and delta<h<beta):return None
    a=math.sin(alpha)**2;b=math.sin(beta)**2
    D=math.sin(delta)**2;H=math.sin(h)**2
    # cos squared is stable where 1-sin squared loses precision.
    ca=math.cos(alpha)**2;cb=math.cos(beta)**2
    cd=math.cos(delta)**2;ch=math.cos(h)**2
    C0=a*H*cb*cd-D*b*ch*ca
    C1=a*H*(b+D)-D*b*(H+a)
    if C1==0:return None
    t=-C0/C1
    if not 0<t<1:return None
    sm=math.sqrt(t);m=1/sm
    J=lambda z:math.atan2(sm*math.sin(z),math.cos(z))
    A,B,d,g=map(J,(alpha,beta,delta,h))
    r=D*(ch+t*H)/(H*(cd+t*D))
    if not(0<r<c*c and 0<d<A<B<P/2 and d<g<B):return None
    res=(B-g-c*(A+d))/sm
    if not quality:return res
    s=math.sqrt(r);k=(1-t)/t;e=1-c*c
    V=P+h-beta+m*(B-g)
    U=(P-beta)*math.sin(B)**2+h*math.sin(g)**2
    Q=(c*math.cos(B)-s*math.cos(A))/math.sin(B)-c*k*(1-r)**2*math.sin(g)*math.cos(d)*math.cos(g)/(math.cos(d)*(1+k*math.sin(g)**2)+c*s*math.cos(g)*(1+k*r*math.sin(g)**2))
    R=(c*c-r)*V-k*e*r*U
    return dict(c=c,delta=delta,alpha=alpha,m=m,r=r,B=B,g=g,A=A,d=d,Q=Q,R=R,ratio=k*e*r*U/((c*c-r)*V),suff=c*c-r-k*e*r*math.sin(B)**2,C3=res/m,C1=beta-c*alpha-(1-c)*P,C2=delta+h/c-P/2,t=t)

def roots(c,delta,n=400):
    lo=delta;hi=P-P/(2*c)
    if not lo<hi:return []
    fs={j/n for j in range(1,n)}
    fs.update(10**(-j/4) for j in range(1,57))
    fs.update(1-10**(-j/4) for j in range(1,57))
    out=[];prev=None
    for frac in sorted(fs):
        x=lo+(hi-lo)*frac;fx=coords(c,delta,x)
        if fx is not None and prev and fx*prev[1]<0:
            a0=bisect(lambda z:coords(c,delta,z),prev[0],x)
            if a0 is not None:
                v=coords(c,delta,a0,True)
                if v is not None and abs(v['C3'])<1e-8:out.append(v)
        prev=(x,fx) if fx is not None else None
    return out

if __name__=='__main__':
    seed=20260908; rng=random.Random(seed)
    pairs=[]
    for c in [2/3+10**(-j/3) for j in range(2,34)]+[.668,.68,.7,.71,.72,.75,.8,.85,.9,.95,.98,.995,.9999,.99999999]:
        if not 2/3<c<1:continue
        dm=min(c*P/(2*(1+c)),P-P/(2*c))
        for z in [10**(-j/3) for j in range(1,34)]+[j/40 for j in range(1,40)]+[1-10**(-j/3) for j in range(1,34)]:
            pairs.append((c,dm*z))
    for _ in range(500):
        c=rng.uniform(2/3,1);dm=min(c*P/(2*(1+c)),P-P/(2*c))
        z=rng.random() if rng.random()<.5 else 10**rng.uniform(-12,0)
        pairs.append((c,dm*z))
    out=[];multi=[]
    for i,(c,d) in enumerate(pairs):
        rr=roots(c,d);out.extend(rr)
        if len(rr)>1:multi.append((c,d,len(rr)))
    qp=[z for z in out if z['Q']>0]
    summary=dict(seed=seed,pairs=len(pairs),roots=len(out),Qpositive=len(qp),candidates=[z for z in qp if z['R']<=0],max_m=max((z['m'] for z in out),default=None),max_c_Qpositive=max((z['c'] for z in qp),default=None),multiple=multi,best=sorted(qp,key=lambda z:z['ratio'],reverse=True)[:10])
    with open('runs/rigorous-open-math-research/q9/branches_scan.json','w') as f:json.dump(dict(summary=summary,roots=out),f,indent=2)
    print(json.dumps(summary,indent=2))
