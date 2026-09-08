"""Binary64 numerical exploration ONLY; no result here is a proof."""
import math, json, random, sys
P=math.pi

def bisect(f,a,b,n=52):
    fa,fb=f(a),f(b)
    if fa*fb>0:return None
    for _ in range(n):
        z=(a+b)/2; fz=f(z)
        if (fz>0)==(fa>0):a,fa=z,fz
        else:b,fb=z,fz
    return (a+b)/2

def angles(m,c,s):
    H=lambda z:math.atan(m*math.tan(z))
    arc=lambda z:math.asin(s*math.sin(z))
    g=bisect(lambda z:H(z)+c*H(arc(z))-c*P/2,0,P/2)
    d=arc(g); t=g+c*d
    if P/2-c*math.asin(s)<=t:return None
    B=bisect(lambda z:z-c*arc(z)-t,g,P/2)
    A=arc(B)
    return B,g,A,d

def residual(m,c,s):
    z=angles(m,c,s)
    if z is None:return None
    B,g,A,d=z
    H=lambda z:math.atan(m*math.tan(z))
    return H(B)-c*H(A)-(1-c)*P

def vals(m,c,s):
    B,g,A,d=angles(m,c,s); r=s*s; k=m*m-1; e=1-c*c
    H=lambda z:math.atan(m*math.tan(z))
    V=P+H(g)-H(B)+m*(B-g)
    U=(P-H(B))*math.sin(B)**2+H(g)*math.sin(g)**2
    Q=(c*math.cos(B)-s*math.cos(A))/math.sin(B)-c*k*(1-r)**2*math.sin(g)*math.cos(d)*math.cos(g)/(math.cos(d)*(1+k*math.sin(g)**2)+c*s*math.cos(g)*(1+k*r*math.sin(g)**2))
    R=(c*c-r)*V-k*e*r*U
    return dict(m=m,c=c,r=r,B=B,g=g,A=A,d=d,Q=Q,R=R,T=r*U/V,ratio=k*e*r*U/((c*c-r)*V),suff=(c*c-r)-k*e*r*math.sin(B)**2,residual=residual(m,c,s))

def roots(c,s):
    grid=[1+10**(-5+j*0.18) for j in range(58)]
    out=[];prev=None
    for m in grid:
        f=residual(m,c,s)
        if f is not None and prev and f*prev[1]<0:
            a,b=prev[0],m
            root=bisect(lambda M:residual(M,c,s),a,b,48)
            out.append(vals(root,c,s))
        prev=(m,f) if f is not None else None
    return out
if __name__=='__main__':
    out=[]
    for c in [.668,.68,.7,.72,.75,.8,.85,.9,.95,.98,.995]:
        for frac in [.02,.05,.1,.2,.3,.4,.5,.6,.7,.8,.9,.95,.99]:
            out+=roots(c,c*frac)
    with open('runs/rigorous-open-math-research/q9/reproducibility/scan.json','w') as f:json.dump(out,f,indent=2)
    qp=[z for z in out if z['Q']>0]
    print('roots',len(out),'Qpositive',len(qp),'counterexample candidates',sum(z['R']<=0 for z in qp))
    print('worst Qpositive',sorted(qp,key=lambda z:z['ratio'],reverse=True)[:8])
    print('sample roots',out[:4])
