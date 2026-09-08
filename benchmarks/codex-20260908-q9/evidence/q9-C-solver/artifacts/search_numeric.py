import math,random,json,time
pi=math.pi

def vals(m,c,x,extra=False):
    a=math.tan(x); y=(1-c)*pi+c*x
    A=math.atan(a/m); B=math.atan(math.tan(y)/m)
    sr=math.sin(A)/math.sin(B); r=sr*sr
    lo=0.;hi=pi/2
    for _ in range(52):
        g=(lo+hi)/2; d=math.asin(min(1.,sr*math.sin(g)))
        z=math.atan(m*math.tan(d))+math.atan(m*math.tan(g))/c-pi/2
        if z>0: hi=g
        else: lo=g
    g=(lo+hi)/2; d=math.asin(min(1.,sr*math.sin(g)))
    eq=B-g-c*(A+d)
    if not extra: return eq
    k=m*m-1; e=1-c*c; sg=math.sin(g); cg=math.cos(g); cd=math.cos(d); sb=math.sin(B)
    hb=y;hg=math.atan(m*math.tan(g));V=pi+hg-hb+m*(B-g)
    U=(pi-hb)*sb*sb+hg*sg*sg
    Q=(c*math.cos(B)-sr*math.cos(A))/sb-c*k*(1-r)**2*sg*cd*cg/(cd*(1+k*sg*sg)+c*sr*cg*(1+k*r*sg*sg))
    R=(c*c-r)*V-k*e*r*U
    return dict(m=m,c=c,r=r,B=B,g=g,A=A,d=d,x=x,Q=Q,R=R,V=V,U=U,eq=eq,normalized_R=R/V,ratio=k*e*r*U/((c*c-r)*V),sufficient=(c*c-r)-k*e*r*sb*sb)

def roots(m,c,n=80):
    xmax=pi*(1-1/(2*c)); lastx=xmax*1e-12;lastv=vals(m,c,lastx)
    found=[]
    # endpoint geometric spacing for high-m regimes
    grid=sorted(set([xmax*i/n for i in range(1,n)]+[xmax*(1-10**(-i/5)) for i in range(1,71)]+[xmax*(1-1e-14)]))
    for x in grid:
        v=vals(m,c,x)
        if lastv*v<0:
            lo=lastx;hi=x;vlo=lastv
            for _ in range(45):
                mid=(lo+hi)/2;vmid=vals(m,c,mid)
                if vmid*vlo>0:lo=mid;vlo=vmid
                else:hi=mid
            vv=vals(m,c,(lo+hi)/2,True)
            if vv['r']<c*c and 0<vv['g']<vv['B']<pi/2: found.append(vv)
        lastx=x;lastv=v
    return found

if __name__=='__main__':
    import sys
    start=time.time();data=[]
    for j in range(int(sys.argv[1]) if len(sys.argv)>1 else 500):
        c=2/3+random.random()/3
        m=1+10**random.uniform(-5,5)
        rr=roots(m,c,30)
        for v in rr:
            data.append(v)
            if v['Q']>0 and v['R']<=0:
                print('COUNTEREXAMPLE',json.dumps(v),flush=True)
            if v['Q']>0 and len([a for a in data if a['Q']>0])%20==1:
                print('positive Q sample',json.dumps(v),flush=True)
        if j%100==0: print('iteration',j,'roots',len(data),'elapsed',time.time()-start,flush=True)
    with open('search_numeric_results.json','w') as f:json.dump(data,f,indent=1)
    pos=[v for v in data if v['Q']>0]
    print('roots',len(data),'positive Q',len(pos),'negative R',sum(v['R']<0 for v in data))
    print('smallest R ratio with Q>0',json.dumps(max(pos,key=lambda v:v['ratio']) if pos else {}))
