import importlib.util, random, math, json, time,pathlib
sp=importlib.util.spec_from_file_location('w2','runs/q9/repo/worker_counterexample_search.py');M=importlib.util.module_from_spec(sp);sp.loader.exec_module(M)
rng=random.Random(926001); best=[]; ts=time.time()
for i in range(5000):
 m=1+10**rng.uniform(-5,7)
 c=rng.uniform(2/3,1) if i%3==0 else (1-10**rng.uniform(-8,math.log10(1/3))) if i%3==1 else 2/3+10**rng.uniform(-8,math.log10(1/3))
 last=(0,M.full(m,c,0,M.evaluate(m,c,0)[1])['Q'])
 candidates=[]
 for j in range(1,41):
  s=c*j/40
  ev=M.evaluate(m,c,s)
  if ev is None:break
  ob=M.full(m,c,s,ev[1]);q=ob['Q']
  if q>0:
   ob['S']=(m*m-1)*(1-c*c)*s*s*math.sin(ob['B'])**2/(c*c-s*s); candidates.append(ob)
  if q*last[1]<0:
   lo=last[0];hi=s
   for _ in range(35):
    ss=(lo+hi)/2;ee=M.evaluate(m,c,ss);qq=M.full(m,c,ss,ee[1])['Q']
    if qq>0:lo=ss
    else:hi=ss
   ss=lo;ee=M.evaluate(m,c,ss); ob=M.full(m,c,ss,ee[1]);ob['S']=(m*m-1)*(1-c*c)*ss*ss*math.sin(ob['B'])**2/(c*c-ss*ss); candidates.append(ob)
  last=(s,q)
 if candidates: best.append(max(candidates,key=lambda z:z['S']))
best.sort(key=lambda z:z['S'],reverse=True)
pathlib.Path('runs/q9/repo/worker_counterexample_qboundary.json').write_text(json.dumps(dict(seed=926001,best=best,seconds=time.time()-ts),indent=2))
print(json.dumps(dict(pairs=5000,best=best[:4],seconds=time.time()-ts),indent=2))
