"""Binary64 diagnostic, scaled-angle C1--C3 solve at fixed (m,s).
Includes the formal m=infinity limit; no output is an exact certificate.
"""
import math,json,random
P=math.pi

def bisect(f,a,b,n=60):
    fa,fb=f(a),f(b)
    if fa is None or fb is None or fa*fb>0:return None
    for _ in range(n):
        z=(a+b)/2;fz=f(z)
        if fz is None:return None
        if (fa>0)==(fz>0):a,fa=z,fz
        else:b,fb=z,fz
    return (a+b)/2

def calc(m,s,c,quality=False):
    r=s*s;t=1/(m*m) if math.isfinite(m) else 0
    v=lambda u:s*u/math.sqrt(1+(1-r)*(u/m)**2) if t else s*u
    f=lambda u:math.atan(u)+c*math.atan(v(u))-c*P/2
    hi=1.
    while f(hi)<0 and hi<1e100:hi*=2
    u=bisect(f,0,hi)
    if u is None:return None
    vv=v(u)
    if not t:
        b=u*(1+c*s)/(1-c*s);aa=s*b;dd=s*u;gg=u
        B=g=A=d=0
        HB=math.atan(b);Hg=math.atan(u)
    else:
        gg=m*math.atan(u/m);dd=m*math.atan(vv/m)
        AA=lambda b:m*math.asin(s*math.sin(b/m))
        fB=lambda b:b-c*AA(b)-gg-c*dd
        bhi=min(m*P/2,gg*(1+c*s)/(1-c*s))
        if fB(bhi)<=0:return None
        b=bisect(fB,gg,bhi)
        if b is None:return None
        aa=AA(b);B=b/m;g=gg/m;A=aa/m;d=dd/m
        HB=math.atan(m*math.tan(B));Hg=math.atan(u)
    HA=math.atan(aa) if not t else math.atan(m*math.tan(A))
    res=HB-c*HA-(1-c)*P
    if not quality:return res
    # Work with Q/m, m^2 U, and V, avoiding overflow in k.
    if not t:
        mb= b;mg=gg;cb=ca=cg=cd=1.
    else:
        mb=m*math.sin(B);mg=m*math.sin(g)
        cb,ca,cg,cd=map(math.cos,(B,A,g,d))
    V=P+Hg-HB+b-gg
    m2U=(P-HB)*mb*mb+Hg*mg*mg
    q=(c*cb-s*ca)/mb-c*(1-t)*(1-r)**2*mg*cd*cg/(cd*(1+(1-t)*mg*mg)+c*s*cg*(1+(1-t)*r*mg*mg))
    R=(c*c-r)*V-(1-t)*(1-c*c)*r*m2U
    return dict(m=m,s=s,r=r,c=c,B=B,g=g,A=A,d=d,Q_over_m=q,R=R,ratio=(1-t)*(1-c*c)*r*m2U/((c*c-r)*V),suff=c*c-r-(1-t)*(1-c*c)*r*mb*mb,C1=res,u=u,scaled_B=b)

def roots(m,s,n=80):
    lo=max(2/3,s);hi=1.
    fs={j/n for j in range(1,n)}
    fs.update(10**(-j/3) for j in range(1,40))
    fs.update(1-10**(-j/3) for j in range(1,40))
    out=[];prev=None
    for z in sorted(fs):
        c=lo+(hi-lo)*z
        if not lo<c<1:continue
        f=calc(m,s,c)
        if f is not None and prev and f*prev[1]<0:
            c0=bisect(lambda C:calc(m,s,C),prev[0],c)
            if c0 is not None:out.append(calc(m,s,c0,True))
        prev=(c,f) if f is not None else None
    return out

if __name__=='__main__':
    ms=[1+10**(-j) for j in range(1,10)]+[1.1,1.5,2.,5.,10.,30.,100.]+[10.**j for j in [3,4,5,6,8,10,12,15,20,30,50,100,150]]+[math.inf]
    ss=[10**(-j/2) for j in range(1,29)]+[j/50 for j in range(1,50)]+[1-10**(-j/2) for j in range(1,29)]
    out=[];multi=[]
    for m in ms:
        for s in ss:
            rr=roots(m,s);out.extend(rr)
            if len(rr)>1:multi.append((m,s,len(rr)))
    qp=[z for z in out if z['Q_over_m']>0]
    summary=dict(pairs=len(ms)*len(ss),roots=len(out),Qpositive=len(qp),candidates=[z for z in qp if z['R']<=0],max_c_Qpositive=max((z['c'] for z in qp),default=None),multiple=multi,best=sorted(qp,key=lambda z:z['ratio'],reverse=True)[:10])
    with open('runs/rigorous-open-math-research/q9/branches_large_m.json','w') as f:json.dump(dict(summary=summary,roots=out),f,indent=2)
    print(json.dumps(summary,indent=2))
