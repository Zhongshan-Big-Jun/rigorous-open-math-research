#!/usr/bin/env python3
"""Exact integer polynomial/Bernstein certificate generator for O7."""
import math, time, json
from collections import defaultdict
from pathlib import Path
class P(dict):
 def __add__(a,b):
  if not isinstance(b,P):b=P({(0,0,0):b})
  d=P(a)
  for k,v in b.items():d[k]=d.get(k,0)+v
  return P({k:v for k,v in d.items() if v})
 __radd__=__add__
 def __neg__(a):return P({k:-v for k,v in a.items()})
 def __sub__(a,b):return a+-b
 def __rsub__(a,b):return -a+b
 def __mul__(a,b):
  if not isinstance(b,P):return P({k:v*b for k,v in a.items() if v*b})
  d=defaultdict(int)
  for (i,j,k),v in a.items():
   for (l,m,n),w in b.items():d[(i+l,j+m,k+n)]+=v*w
  return P({k:v for k,v in d.items() if v})
 __rmul__=__mul__
 def __pow__(a,n):
  r=P({(0,0,0):1})
  while n:
   if n&1:r=r*a
   a=a*a;n//=2
  return r

def polynomial():
 c=P({(1,0,0):1});s=P({(0,1,0):1});z=P({(0,0,1):1})
 t2=c*c*s*s;u=c*c*s
 A=1+(c**4+2*c*c)*s*s;B=s*(1+2*c*c+c**4*s*s)
 D=(1-s)*(1-u)**2
 assert A-B==D
 W=B+D*z;V=W+u*B;J100=49*(1+c)**2
 F=(1-t2)*(1-u*u)*((1-t2)*J100*W*W*B*B-100*(W*W-B*B)*V*V)-D*(1-z)*(100*B*(B+u*W)*V*V+J100*W*(W+u*t2*B)*B*B)
 return F

def affcube(poly,degree):
 nc,ns,nz=degree;d=defaultdict(int)
 for (a,b,k),v in poly.items():
  for i in range(a+1):
   vi=v*math.comb(a,i)*2**(a-i)*3**(nc-a)
   for j in range(b+1):d[(i,j,k)]+=vi*math.comb(b,j)*2**(ns-b)
 return P({k:v for k,v in d.items() if v})

def bernstein(poly,degree):
 data=dict(poly)
 for axis,n in enumerate(degree):
  lcm=math.lcm(*(math.comb(n,i) for i in range(n+1)))
  d=defaultdict(int)
  for exp,v in data.items():
   i=exp[axis];q=lcm//math.comb(n,i)
   for k in range(i,n+1):
    dest=list(exp);dest[axis]=k;d[tuple(dest)]+=v*q*math.comb(k,i)
  data=d
 nc,ns,nz=degree
 return [data.get((i,j,k),0) for i in range(nc+1) for j in range(ns+1) for k in range(nz+1)]

def split(data,degree,axis):
 shape=[n+1 for n in degree];stride=[shape[1]*shape[2],shape[2],1];n=degree[axis];st=stride[axis]
 left=[0]*len(data);right=[0]*len(data)
 for base in range(len(data)):
  if (base//st)%shape[axis]:continue
  row=[data[base+i*st] for i in range(n+1)]
  # triangle at midpoint. Scale output uniformly by 2**n.
  left[base]=row[0]<<n;right[base+n*st]=row[n]<<n
  for lev in range(1,n+1):
   row=[row[i]+row[i+1] for i in range(len(row)-1)]
   left[base+lev*st]=row[0]<<(n-lev)
   right[base+(n-lev)*st]=row[-1]<<(n-lev)
 return left,right

def stats(data):
 return dict(negative=sum(v<0 for v in data),zero=sum(v==0 for v in data),positive=sum(v>0 for v in data))

def main():
 ts=time.time();p=polynomial();degree=tuple(max(k[i] for k in p) for i in range(3));print('polynomial',len(p),'degree',degree,'seconds',time.time()-ts,flush=True)
 q=affcube(p,degree);print('affine',len(q),'seconds',time.time()-ts,flush=True)
 b=bernstein(q,degree);print('bernstein',stats(b),'seconds',time.time()-ts,flush=True)
 Path('runs/q9/worker_jensen_initial.json').write_text(json.dumps({'degree':degree,'bernstein':[str(v) for v in b]},separators=(',',':')))
 for ax in range(3):
  l,r=split(b,degree,ax)
  print('split',ax,stats(l),stats(r),flush=True)
if __name__=='__main__':main()
