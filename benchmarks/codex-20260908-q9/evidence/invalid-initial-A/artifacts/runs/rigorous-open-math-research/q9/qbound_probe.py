"""O-Qbound route probe; binary64 evidence only, never a proof."""
import math, random, json

def bisection(f,a,b):
    for _ in range(60):
        t=(a+b)/2
        if f(t)>0:b=t
        else:a=t
    return (a+b)/2

def qfun(c,q,B,g,k):
    r=q*q; A=math.asin(q*math.sin(B)); d=math.asin(q*math.sin(g))
    return ((c*math.cos(B)-q*math.cos(A))/math.sin(B)
      -c*k*(1-r)**2*math.sin(g)*math.cos(d)*math.cos(g)
      /(math.cos(d)*(1+k*math.sin(g)**2)
       +c*q*math.cos(g)*(1+k*r*math.sin(g)**2)))

if __name__=='__main__':
    rng=random.Random(290091); best=None; failures=0
    for i in range(10000):
        c=2/3+rng.random()/3; q=c*rng.random(); B=rng.random()*math.pi/2
        A=math.asin(q*math.sin(B))
        g=bisection(lambda z:z+c*math.asin(q*math.sin(z))-B+c*A,0,B)
        K=(c*c-q*q)/((1-c*c)*q*q*math.sin(B)**2)
        Q=qfun(c,q,B,g,K)
        row=dict(c=c,r=q*q,B=B,g=g,K=K,Q=Q)
        if Q>0:failures+=1
        if best is None or Q>best['Q']:best=row
    print(json.dumps(dict(n=10000,failures=failures,best=best),indent=2))
