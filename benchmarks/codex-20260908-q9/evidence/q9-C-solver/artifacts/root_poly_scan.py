import random,math

def vals(c,t):
 r=t*t;h=1-r;L=(3+2*t)/(1+6*t+3*r);J=1+L*h;den=1-c*c*r
 C=c*(1+(c*c+2)*r)/den;D=t*(1+2*c*c+c*c*r)/den; a=c*t
 co=[-C*a*r*L,c*h*J-C*(1+L)+D*a*r*L,D*(1+L)-C*a,D*a-c*h]
 def P(v):return co[0]+v*(co[1]+v*(co[2]+v*co[3]))
 def Pd(v):return co[1]+v*(2*co[2]+v*3*co[3])
 star=C/D;z=star-1
 bern=[P(1),P(1)+z*Pd(1)/3,P(star)-z*Pd(star)/3,P(star)]
 return (J-star*star,min(bern),Pd(1),Pd(star),bern)
random.seed(45215)
mins=[(1e9,None) for _ in range(4)]
for _ in range(200000):
 c=random.uniform(2/3,1);t=random.uniform(1/3,c);vs=vals(c,t)
 for j in range(4):
  if vs[j]<mins[j][0]:mins[j]=(vs[j],(c,t,vs))
print(mins)
