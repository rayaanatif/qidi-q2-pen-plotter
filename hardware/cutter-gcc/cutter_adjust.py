"""Adjustable-force pusher: FRAME (tongue + guide tube + printed nut), PLUNGER (disc + coil + cap), ROD (printed screw + thumb knob), KEY (retention bar).
Turning the knob clockwise screws the rod down, compresses the coil further and raises the cut force (about 100 gf per 3 mm turn for the default coil).
Run: python3 cutter_adjust.py"""
import sys; sys.path.insert(0,".")
import numpy as np
from vf import *
import cad
from params import *
from module_geom import *
from scipy import ndimage
g=geom('adj'); R,A,B,P,N,ZS,AH,zd0=g['R'],g['A'],g['B'],g['P'],g['N'],g['ZS'],g['AH'],g['zd0']
TWO=2*np.pi
def polar(X,Y): x=X-CX; y=Y-YT; return np.hypot(x,y),np.mod(np.arctan2(y,x),TWO)
CAP_T=3.0; CAP_R=6.7; LAND_IN=3.9; LAND_OUT=CAP_R
TUBE_RI,TUBE_RO=7.0,8.1
TW=6.4; TY0,TY1=110.3,112.3
HT0=AH-DMAX-3.0                   # tube/tongue bottom
CAPTOP=AH+CAP_T
NUT_T=10.0; HN1=MOD_TOP; HN0=HN1-NUT_T          # nut plate
CONE=TUBE_RI-5.3                                 # 45 deg cone under the nut plate
# ---- thread (right hand, 90 deg included angle, pitch 3, depth 1.1)
TP,TDEP,TROOT=3.0,1.1,3.9
def tprof(h,th,h0):
    phi=np.mod((h-h0)/TP-th/TWO,1.0); u=np.abs(phi-0.5)
    return np.clip(1.0-(u-0.0667)/0.3667,0.0,1.0)       # 1 at crest, 0 at root
CL=0.3                                                  # print clearance (radial)
# ============ FRAME ============
al=lambda v:-1+ST*np.floor((v+1)/ST)
GF=Grid(CX-9.0,CX+9.0,109.2,YT+TUBE_RO+1.6,al(HT0-1.0),MOD_TOP+1.0)
def tube(X,Y,H):
    r,_=polar(X,Y); return np.maximum(np.maximum(r-TUBE_RO,HT0-H),H-HN1)
GF.op('add',(CX-9,CX+9),(YT-9,YT+9),(HT0,HN1),tube)
GF.op('add',(CX-TW,CX+TW),(TY0,TY1),(HT0,MOD_TOP),sd_box(CX-TW,CX+TW,TY0,TY1,HT0,MOD_TOP))
def bore(X,Y,H):
    r,th=polar(X,Y)
    rb=TROOT+CL+TDEP*tprof(H,th,0.0)
    h1=HN0-CONE
    R_=np.where(H<h1,TUBE_RI,np.where(H<HN0,TUBE_RI-(H-h1),rb))
    return np.maximum(r-R_,np.abs(H-(HT0+HN1)/2)-(HN1-HT0)/2-1.0)
GF.op('sub',(CX-8,CX+8),(YT-8,YT+8),(HT0-1,HN1+1),bore)
# key slot at the front (+y) for the plunger tab, open at the bottom, with a Delta scale beside it
TABC=AH+2.0
GF.op('sub',(CX-1.3,CX+1.3),(YT+6,YT+9.5),(HT0-1,TABC+1.0),sd_box(CX-1.3,CX+1.3,YT+6,YT+9.5,HT0-1,TABC+1.0))
for d in range(0,int(DMAX)+1):
    wlen=2.6 if d in (0,5) else 1.6
    hh=TABC-d
    GF.op('sub',(CX+1.4,CX+1.4+wlen),(YT+7.2,YT+8.6),(hh-.3,hh+.3),sd_box(CX+1.4,CX+1.4+wlen,YT+7.25,YT+8.6,hh-0.2,hh+0.2))
T,vol=mesh(GF); cad.write("qs_cutter_adj_frame_v2.stl",T)
lab,n=ndimage.label(GF.F>0.5); print("frame",len(T),"vol %.0f"%vol,"bodies",n)
np.savez("Fadj_frame.npz",F=GF.F.astype(np.float16),o=np.array([GF.x0,GF.y0,GF.h0]))
# ============ PLUNGER ============
H0G=-1+ST*np.floor((zd0-2+1)/ST)
GP=Grid(CX-9.0,CX+9.0,YT-8.0,YT+9.0,H0G,CAPTOP+1)
DISC_R=5.9
def disc(X,Y,H):
    r,_=polar(X,Y); return np.maximum(r-DISC_R,np.maximum(zd0-H,H-(zd0+TD)))
GP.op('add',(CX-7,CX+7),(YT-7,YT+7),(zd0,zd0+TD),disc)
def helix(X,Y,H):
    r,th=polar(X,Y); u=(H-ZS-P*th/TWO)/P; kk=np.round(u); v_=(u-kk)*P
    d=(np.abs(r-R)/A+np.abs(v_)/B-1)/np.sqrt(1/A**2+1/B**2)
    return np.where((kk>=0)&(kk<=N-2),d,1e3)
GP.op('add',(CX-8,CX+8),(YT-8,YT+8),(zd0+TD-1,AH+0.1),helix)
def land(X,Y,H):
    r,th=polar(X,Y); zc=ZS+(N-1)*P+P*th/TWO; under=zc-B+np.abs(r-R)*B/A
    return np.maximum(np.maximum(r-LAND_OUT,LAND_IN-r),np.maximum(under-H,H-AH))
GP.op('add',(CX-9,CX+9),(YT-9,YT+9),(ZS+(N-1)*P-B-1,AH+0.1),land)
def cap(X,Y,H):
    r,_=polar(X,Y); under=AH-0.3+np.maximum(0.0,LAND_IN-r)
    return np.maximum(np.maximum(r-CAP_R,under-H),H-CAPTOP)
GP.op('add',(CX-8,CX+8),(YT-8,YT+8),(AH-0.4,CAPTOP),cap)
TABP=[(YT+6.0,CAPTOP),(YT+8.6,CAPTOP),(YT+8.6,CAPTOP-1.1),(YT+6.9,CAPTOP-2.8),(YT+6.0,CAPTOP-2.8)]
GP.op('add',(CX-1.0,CX+1.0),(YT+5.5,YT+9),(CAPTOP-3,CAPTOP+0.1),sd_poly_prism(TABP,(CX-1.0,CX+1.0),'x'))
T,vol=mesh(GP); cad.write("qs_cutter_adj_plunger_v2.stl",T)
lab,n=ndimage.label(GP.F>0.5); print("plunger",len(T),"vol %.0f"%vol,"bodies",n,"AH %.2f zd0 %.2f rate %.1f gf/mm"%(AH,zd0,g['k_gf']))
np.savez("Fadj_plunger.npz",F=GP.F.astype(np.float16),o=np.array([GP.x0,GP.y0,GP.h0]))
# ============ ROD + KNOB ============
KB0=HN1+0.5+DMAX                      # knob underside at zero preload
KNOB_R,KNOB_T=5.6,7.2
RB0=CAPTOP+0.1                        # rod bottom at zero preload
GR=Grid(CX-7,CX+7,YT-7,YT+7,al(RB0-1),KB0+KNOB_T+1)
def rod(X,Y,H):
    r,th=polar(X,Y)
    thr=KB0-20.0
    rr=np.where(H<thr,TROOT,TROOT+TDEP*tprof(H,th,0.0))
    return np.maximum(r-rr,np.maximum(RB0-H,H-(KB0+0.2)))
GR.op('add',(CX-6,CX+6),(YT-6,YT+6),(RB0,KB0+0.2),rod)
def knob(X,Y,H):
    r,th=polar(X,Y); gr=0.45*np.cos(12*th)           # 12 grip flutes
    return np.maximum(r-(KNOB_R+gr*0)+np.where(r>KNOB_R-0.9,0.5*(1-np.cos(12*th))/2*1.2,0),np.maximum(KB0-H,H-(KB0+KNOB_T)))
GR.op('add',(CX-7,CX+7),(YT-7,YT+7),(KB0,KB0+KNOB_T),knob)
# pointer groove on top
GR.op('sub',(CX-0.4,CX+0.4),(YT,YT+KNOB_R),(KB0+KNOB_T-0.6,KB0+KNOB_T+1),sd_box(CX-0.4,CX+0.4,YT,YT+KNOB_R+1,KB0+KNOB_T-0.6,KB0+KNOB_T+1))
T,vol=mesh(GR); cad.write("qs_cutter_adj_rod_knob_v2.stl",T)
lab,n=ndimage.label(GR.F>0.5); print("rod",len(T),"vol %.0f"%vol,"bodies",n)
np.savez("Fadj_rod.npz",F=GR.F.astype(np.float16),o=np.array([GR.x0,GR.y0,GR.h0]))
# ============ KEY ============
GK=Grid(CX-8.4,CX+8.4,110.2,TY1+4.0,al(KEY_H0-1),KEY_H1+1)
GK.op('add',(CX-7.7,CX+7.7),(110.45,112.25),(KEY_H0,KEY_H1),sd_box(CX-7.7,CX+7.7,110.45,112.25,KEY_H0,KEY_H1))
for sg in (-1,1):
    x0,x1=sorted([CX+sg*6.4,CX+sg*7.7])
    GK.op('add',(x0,x1),(112.0,115.2),(KEY_H0,KEY_H1),sd_box(x0,x1,112.0,115.2,KEY_H0,KEY_H1))
T,vol=mesh(GK); cad.write("qs_cutter_key_v2.stl",T)
lab,n=ndimage.label(GK.F>0.5); print("key",len(T),"vol %.0f"%vol,"bodies",n)
np.savez("Fadj_key.npz",F=GK.F.astype(np.float16),o=np.array([GK.x0,GK.y0,GK.h0]))
print("knob underside Delta=0: %.1f  top %.1f  tube top %.1f  nut %.1f-%.1f  cap top %.1f"%(KB0,KB0+KNOB_T,HN1,HN0,HN1,CAPTOP))
