import importlib.util, random, math, json, time, pathlib
p='runs/q9/repo/worker_counterexample_search.py'; sp=importlib.util.spec_from_file_location('w2',p); M=importlib.util.module_from_spec(sp);sp.loader.exec_module(M)
rng=random.Random(906081729)
t0=time.time()
roots=[];fail=[];maxn=0;randompairs=[];arbitrary=[]
us=sorted(set([j/128 for j in range(1,128)]+[1-10.**(-j) for j in [3,4,6,8,10]]))
for i in range(2500):
 m=1+10**rng.uniform(-6,6)
 if i%4==0: c=2/3+10**rng.uniform(-8,math.log10(1/3-1e-8))
 elif i%4==1:c=1-10**rng.uniform(-8,math.log10(1/3-1e-8))
 else:c=rng.uniform(2/3,1)
 rr,sg=M.roots(m,c,us)
 roots.extend(rr);maxn=max(maxn,len(rr))
 if len(rr)>1: fail.append((m,c,rr))
 randompairs.append((m,c,len(rr)))
for i in range(10000):
 m=1+10**rng.uniform(-4,4);c=rng.uniform(2/3,1);s=c*rng.random()
 ev=M.evaluate(m,c,s)
 if ev is None:continue
 x=M.full(m,c,s,ev[1]);
 if x['Q']>0 and x['sufficient']<=0:arbitrary.append(x)
qs=[x for x in roots if x['Q']>0]
result=dict(seed=906081729,pairs=randompairs,roots=roots,us=us,multiples=fail,arbitrary_C2C3_failures=arbitrary,seconds=time.time()-t0)
pathlib.Path('runs/q9/repo/worker_counterexample_explore.json').write_text(json.dumps(result,indent=2))
print(json.dumps(dict(pairs=len(randompairs),roots=len(roots),Qpositive=len(qs),maxroots=maxn,Qpositive_Rnegative=[x for x in qs if x['R']<=0],Qpositive_suffnegative=[x for x in qs if x['sufficient']<=0],minconds=min(qs,key=lambda x:x['sufficient']),arbitrary_fail_count=len(arbitrary),arbitrary_failure=arbitrary[:2],seconds=time.time()-t0),indent=2))
