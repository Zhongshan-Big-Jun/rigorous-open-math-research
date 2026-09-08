"""Q9 branch/adversarial scan: float-only discovery; never a certificate.
Only math/random/json/time/pathlib from stdlib. Independent s=sqrt(r)
reduction from exact C2 and C3. C2 is solved in y=H(g) to retain angular
scale when m is large. B is solved by bisection with its strict derivative.
"""
import math, random, json, time, pathlib
PI=math.pi

def H(z,m): return math.atan2(m*math.sin(z),math.cos(z))
def evaluate(m,c,s,its=43):
    lo=0.; hi=c*PI/2
    for _ in range(its):
        y=(lo+hi)/2
        g=math.atan(math.tan(y)/m)
        d=math.asin(s*math.sin(g))
        if y+c*H(d,m)>c*PI/2: hi=y
        else: lo=y
    y=(lo+hi)/2
    g=math.atan(math.tan(y)/m)
    d=math.asin(s*math.sin(g))
    target=g+c*d
    if target>=PI/2-c*math.asin(s): return None
    lo=g;hi=PI/2
    for _ in range(its):
        B=(lo+hi)/2
        A=math.asin(s*math.sin(B))
        if B-c*A>target:hi=B
        else:lo=B
    B=(lo+hi)/2; A=math.asin(s*math.sin(B))
    return H(B,m)-c*H(A,m)-(1-c)*PI,(B,g,A,d)

def full(m,c,s,ang):
    B,g,A,d=ang
    k=m*m-1;e=1-c*c;r=s*s
    v=PI+H(g,m)-m*g-H(B,m)+m*B
    u=(PI-H(B,m))*math.sin(B)**2+H(g,m)*math.sin(g)**2
    q=(c*math.cos(B)-s*math.cos(A))/math.sin(B)-c*k*(1-r)**2*math.sin(g)*math.cos(d)*math.cos(g)/(math.cos(d)*(1+k*math.sin(g)**2)+c*s*math.cos(g)*(1+k*r*math.sin(g)**2))
    rho=(c*c-r)*v-k*e*r*u
    cond=c*c-r-k*e*r*math.sin(B)**2
    return dict(m=m,c=c,s=s,B=B,g=g,A=A,d=d,Q=q,R=rho,V=v,U=u,sufficient=cond,
        C1=H(B,m)-c*H(A,m)-(1-c)*PI,C2=H(d,m)+H(g,m)/c-PI/2,C3=B-g-c*(A+d))

def roots(m,c,us,its=43):
    last=(0,PI*(1.5*c-1));roots=[]; signs=[]
    for u in us:
        s=c*u; ev=evaluate(m,c,s,its)
        if ev is None: break
        f,ang=ev
        signs.append((u,f))
        if f*last[1]<0:
            lo=last[0]; hi=s; flo=last[1]
            for _ in range(46):
                mid=(lo+hi)/2
                ev2=evaluate(m,c,mid,its)
                if ev2 is None: raise ValueError('feasibility interval broken')
                ff=ev2[0]
                if ff*flo<0: hi=mid
                else:lo=mid;flo=ff
            ss=(lo+hi)/2
            ev3=evaluate(m,c,ss,its)
            roots.append(full(m,c,ss,ev3[1]))
        last=(s,f)
    return roots, signs

def run():
    ts=time.time(); allroots=[];branchcounts={}; cfg={}
    ms=[1+10.**(-j) for j in [1,2,3,4,6,8]]+[1.3,1.7,2,3,5,10,30,100,300,1000,1e4,1e5,1e6,1e8]
    cs=[2/3+10.**(-j) for j in [2,3,4,6,8]]+[.68,.7,.75,.8,.85,.9,.95]+[1-10.**(-j) for j in [2,3,4,6,8]]
    us=sorted(set([i/100 for i in range(1,100)]+[10.**(-j) for j in [2,3,4,6,8]]+[1-10.**(-j) for j in [2,3,4,6,8]]))
    attempted=0
    nonmon=[]
    for m in ms:
        for c in cs:
            rr,sg=roots(m,c,us)
            allroots.extend(rr); attempted+=1
            if len(rr)!=1:branchcounts[str((m,c))]=len(rr)
            # Whether residual reverses derivative sign, above local rounding threshold
            dd=[b[1]-a[1] for a,b in zip(sg,sg[1:])]
            if any(x>1e-10 for x in dd) and any(x<-1e-10 for x in dd):nonmon.append((m,c))
    out=dict(pairs=attempted,grid=dict(ms=ms,cs=cs,us=us),roots=allroots,non_single=branchcounts,nonmonotone=nonmon,seconds=time.time()-ts,
        caveat='IEEE binary64 trigonometric and bisection discovery only. Tangent roots or thin branch intervals can be missed. No certification.')
    pathlib.Path('runs/q9/repo/worker_counterexample_scan.json').write_text(json.dumps(out,indent=2))
    qs=[x for x in allroots if x['Q']>0]
    print(json.dumps(dict(pairs=attempted,roots=len(allroots),Qpositive=len(qs),negativeR=[x for x in qs if x['R']<=0],multi=[(k,v) for k,v in branchcounts.items() if v>1],nonmonotone=nonmon,minR=min(qs,key=lambda x:x['R']) if qs else None,mincond=min(qs,key=lambda x:x['sufficient']) if qs else None,seconds=time.time()-ts),indent=2))
if __name__=='__main__':run()
