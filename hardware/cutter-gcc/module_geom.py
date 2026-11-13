"""Module (pusher) numbers shared by bay (notch heights) and module."""
import numpy as np
from params import *
VARIANTS={ # name: (n_active, R, A, B, GAP)
 'soft':(4,5.0,1.1,1.15,3.0),
 'std': (3,5.0,1.1,1.15,3.6),
 'firm':(3,5.0,1.3,1.3,3.4),
 'hard':(3,5.0,1.5,1.5,3.2,7.0)}   # optional 6th value: free-hang pin depression
TD=1.5            # pusher disc thickness
XEQ=6.0           # free-hanging pin depression (blade out ~5.2 mm) with this module in place
def rate(v):
    n,R,A,B,GAP=VARIANTS[v][:5]
    J=0.6*np.pi*A**3*B**3/(A**2+B**2)
    return 500*J/(2*np.pi*R**3*n)        # N/mm (G~500 MPa printed PETG, +/-40 %)
def geom(v):
    n,R,A,B,GAP=VARIANTS[v][:5]; xe=VARIANTS[v][5] if len(VARIANTS[v])>5 else XEQ; N=n+1; P=2*B+GAP
    k=rate(v)*101.97
    feq=F0_GF+K_INT*xe; deq=feq/k
    zd0=PIN0-xe-deq                       # disc underside, coil relaxed
    ZS=zd0+TD+B-0.6
    AH=ZS+N*P+B+1.6                        # flat underside of the arm = top of the land
    return dict(n=n,N=N,R=R,A=A,B=B,GAP=GAP,P=P,k_gf=k,deq=deq,zd0=zd0,ZS=ZS,AH=AH)
# detent: bump top face at local height HBT above AH; three notches 3 mm apart (centre = nominal)
HBT=34.0; NOTCH_PITCH=3.0
ROOF0=geom('std')['AH']+HBT+0.1          # centre notch roof (absolute h); same bay for all coil variants
def roofs(): return [ROOF0+NOTCH_PITCH*i for i in (-1,0,1)]
def hbt(v): return ROOF0-0.1-geom(v)['AH']   # bump top face above this variant's arm underside
if __name__=="__main__":
    for v in VARIANTS:
        g=geom(v); print(v,{k:round(x,2) if isinstance(x,float) else x for k,x in g.items()})
