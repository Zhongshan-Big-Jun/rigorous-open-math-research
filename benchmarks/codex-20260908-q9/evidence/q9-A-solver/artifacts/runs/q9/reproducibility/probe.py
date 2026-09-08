"""Exploration only. Floating point residuals are not an exact certificate."""
import math,json
pi=math.pi

def bisect(f,a,b,n=60):
    fa=f(a); fb=f(b)
    if fa*fb>0: return None
    for _ in range(n):
        x=(a+b)/2; fx=f(x)
        if fx==0: return x
        if (fx>0)==(fa>0): a=x;fa=fx
        else: b=x
    return (a+b)/2

def evaluate(m,c,s):
    H=lambda z: math.atan2(m*math.sin(z),math.cos(z))
    az=lambda z: math.asin(s*math.sin(z))
    g=bisect(lambda g:H(az(g))+H(g)/c-pi/2,0,pi/2,48)
    d=az(g); q=g+c*d
    if pi/2-c*math.asin(s)<=q: return None
    B=bisect(lambda B:B-c*az(B)-q,g,pi/2,48)
    A=az(B)
    E=H(B)-c*H(A)-(1-c)*pi
    k=m*m-1;r=s*s;e=1-c*c
    V=pi+H(g)-H(B)+m*(B-g)
    U=(pi-H(B))*math.sin(B)**2+H(g)*math.sin(g)**2
    Q=(c*math.cos(B)-s*math.cos(A))/math.sin(B)-c*k*(1-r)**2*math.sin(g)*math.cos(d)*math.cos(g)/(math.cos(d)*(1+k*math.sin(g)**2)+c*s*math.cos(g)*(1+k*r*math.sin(g)**2))
    R=(c*c-r)*V-k*e*r*U
    S=c*c-r-k*e*r*math.sin(B)**2
    return dict(m=m,c=c,r=r,B=B,g=g,E=E,Q=Q,R=R,S=S,T=r*U/V)

def scan():
    out=[]
    for c in [.667,.68,.70,.75,.8,.85,.9,.95,.98,.99,.999]:
        for m in [1.01,1.1,1.5,2,3,5,10,30,100,1000,1e5]:
            prev=evaluate(m,c,0)
            for j in range(1,41):
                s=c*j/40
                v=evaluate(m,c,s)
                if prev and v and prev['E']*v['E']<0:
                    s0=math.sqrt(prev['r']); s1=s
                    sr=bisect(lambda t:evaluate(m,c,t)['E'],s0,s1,42)
                    sol=evaluate(m,c,sr);out.append(sol)
                prev=v
    print(json.dumps(out,indent=2))
    with open('runs/q9/reproducibility/probe_results.json','w') as f:json.dump(out,f,indent=2)
    print('COUNT',len(out),'Q positive',sum(x['Q']>0 for x in out),'counterexamples',sum(x['Q']>0 and x['R']<=0 for x in out))
    for v in sorted(out,key=lambda x:x['R'])[:5]: print('MIN R',v)
if __name__=='__main__':scan()
