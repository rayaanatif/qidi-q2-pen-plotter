"""Voxel fit check: holder (measured dims + assumptions) vs bay vs pusher, at several states."""
import sys; sys.path.insert(0,".")
import numpy as np
from vf import *
from params import *
from module_geom import *
Bf=np.load("Fcutter_bay.npy").astype(np.float32)
G0=Grid(-35,38,76,132,-1,116)
def holder(xpin, dr=0.0):
    G=Grid(-35,38,76,132,-1,116,F=np.zeros_like(Bf))
    r=lambda d:d/2+dr
    G.op('add',(CX-9,CX+9),(YT-9,YT+9),(HB0,HT),sd_cyl_h(CX,YT,r(BARREL_D),HB0,HT))
    G.op('add',(CX-9,CX+9),(YT-9,YT+9),(HT,HT+FLANGE_T),sd_cyl_h(CX,YT,r(FLANGE_D),HT,HT+FLANGE_T))
    G.op('add',(CX-9,CX+9),(YT-9,YT+9),(HT+FLANGE_T,RING_TOP),sd_cyl_h(CX,YT,r(RING_D),HT+FLANGE_T,RING_TOP))
    G.op('add',(CX-9,CX+9),(YT-9,YT+9),(RING_TOP,PIN0-xpin),sd_cyl_h(CX,YT,r(PIN_D),RING_TOP,PIN0-xpin))
    return G.F
def place(v,dh=0.0):
    z=np.load("Fpusher_%s.npz"%v); F=z['F'].astype(np.float32); o=z['o']
    out=np.zeros_like(Bf)
    ix=int(round((o[0]-G0.x0)/ST)); iy=int(round((o[1]-G0.y0)/ST)); ih=int(round((o[2]+dh-G0.h0)/ST))
    ny,nh,nx=F.shape; out[iy:iy+ny,ih:ih+nh,ix:ix+nx]=F
    return out
vox=ST**3
def ov(a,b,t=0.5): return float(((a>t)&(b>t)).sum()*vox)
print("holder vs bay (clearance bore +0.175 radial):", "%.2f mm3"%ov(holder(0),Bf))
print("holder with +0.1 mm oversize vs bay: %.2f mm3"%ov(holder(0,0.1),Bf))
for v in [k for k in VARIANTS if k!='adj']:
    P=place(v)
    for x in (0.0,XEQ,PIN_TRAVEL):
        # pusher assumed relaxed pose: disc at zd0; compare against holder, disc only interferes if pin top above zd0 -> flag by contact depth
        H=holder(x)
        o=ov(P,H); print("%-5s pin x=%.1f: pusher/holder overlap %.2f mm3 (pin top %.1f vs disc %.2f -> compress %.2f mm)"%(v,x,o,PIN0-x,geom(v)['zd0'],PIN0-x-geom(v)['zd0']))
    print("%-5s pusher vs bay overlap (nominal notch): %.2f mm3"%(v,ov(P,Bf)))
    for dh in (-3.0,3.0):
        print("%-5s  shifted %+.0f mm: pusher vs bay %.2f mm3"%(v,dh,ov(place(v,dh),Bf)))
print("---- insertion sweeps")
# holder dropped in from above (pin at rest)
Hh=holder(0.0); worst=0
for dh in np.arange(0,70,1.0):
    sh=int(round(dh/ST)); S=np.zeros_like(Hh); S[:,sh:,:]=Hh[:,:Hh.shape[1]-sh,:] if sh>0 else Hh
    worst=max(worst,ov(S,Bf))
print("holder sweep from 70 mm above: max overlap with bay %.2f mm3"%worst)
for v in [k for k in VARIANTS if k!='adj']:
    P=place(v); g=geom(v)
    Hx=holder(XEQ); 
    # module held rigid at the moment the disc touches the pin (eq pin top) and above
    worstH=0; worstB=0; atnom=None
    top_touch=PIN0-XEQ-g['zd0']          # shift that puts disc on the pin top at eq
    for dh in np.arange(top_touch,top_touch+45,0.6):
        sh=int(round(dh/ST)); S=np.zeros_like(P); S[:,sh:,:]=P[:,:P.shape[1]-sh,:]
        worstH=max(worstH,ov(S,Hx)); b=ov(S,Bf); worstB=max(worstB,b)
    print("%-5s module sweep from touch..+45 mm: max overlap with holder %.2f, with bay (detent bumps only) %.2f mm3"%(v,worstH,worstB))
