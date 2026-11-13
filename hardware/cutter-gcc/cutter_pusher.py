"""Pusher module: printed coil that presses the holder's pin with a limited, adaptive force.
One part, prints disc-down, no supports. Drops into the channel of cutter_bay and clicks into a notch.
Run: python3 cutter_pusher.py [soft|std|firm]"""
import sys; sys.path.insert(0,".")
import numpy as np
from vf import *
import cad
from params import *
from module_geom import *
v=sys.argv[1] if len(sys.argv)>1 else 'std'
g=geom(v); R,A,B,P,N,ZS,AH,zd0=g['R'],g['A'],g['B'],g['P'],g['N'],g['ZS'],g['AH'],g['zd0']
TONG_TOP=MOD_TOP
DISC_R=5.9; LAND_IN=3.9; LAND_OUT=R+A+0.9
TW=6.4; TY0,TY1=110.3,112.3     # tongue half width, back/front faces
H0G=-1+ST*np.floor((zd0-2+1)/ST)
G=Grid(CX-8.2,CX+8.2,TY0-0.5,YT+LAND_OUT+0.3,H0G,TONG_TOP+1)
TWO=2*np.pi
def polar(X,Y): 
    x=X-CX; y=Y-YT; return np.hypot(x,y),np.mod(np.arctan2(y,x),TWO)
# disc that touches the pin
def disc(X,Y,H):
    r,_=polar(X,Y); return np.maximum(r-DISC_R,np.maximum(zd0-H,H-(zd0+TD)))
G.op('add',(CX-7,CX+7),(YT-7,YT+7),(zd0,zd0+TD),disc)
# helical wire, diamond section
def helix(X,Y,H):
    r,th=polar(X,Y)
    u=(H-ZS-P*th/TWO)/P; kk=np.round(u); v_=(u-kk)*P
    d=(np.abs(r-R)/A+np.abs(v_)/B-1)/np.sqrt(1/A**2+1/B**2)
    return np.where((kk>=0)&(kk<=N-2),d,1e3)      # N-1 active turns; the N-th turn is the land
G.op('add',(CX-8,CX+8),(YT-8,YT+8),(zd0+TD-1,AH+0.1),helix)
# land: last turn thickened to a flat top (flat annulus) with the wire's own 45 deg underside slope
def land(X,Y,H):
    r,th=polar(X,Y)
    zc=ZS+(N-1)*P+P*th/TWO
    under=zc-B+np.abs(r-R)*B/A
    return np.maximum(np.maximum(r-LAND_OUT,LAND_IN-r),np.maximum(under-H,H-AH))
G.op('add',(CX-9,CX+9),(YT-9,YT+9),(ZS+(N-1)*P-B-1,AH+0.1),land)
# arm: round head over the coil + bar back to the tongue, 45 deg funnel under the middle (no bridging)
ARM_T=3.0
def arm(X,Y,H):
    r,_=polar(X,Y)
    head=np.maximum(r-(LAND_OUT),np.zeros_like(r))
    d_head=r-LAND_OUT
    d_bar=np.maximum(np.maximum(np.abs(X-CX)-TW,TY0-Y),Y-YT)
    d2=np.minimum(d_head,d_bar)
    under=AH-0.3+np.maximum(0.0,LAND_IN-r)       # conical roof inside the bore
    return np.maximum(d2,np.maximum(under-H,H-(AH+ARM_T)))
G.op('add',(CX-8,CX+8),(TY0-0.5,YT+8),(AH-0.4,AH+ARM_T),arm)
# tongue (vertical plate) up to the module top face; the key bar sits on top of it
G.op('add',(CX-TW,CX+TW),(TY0,TY1),(AH-0.3,MOD_TOP),sd_box(CX-TW,CX+TW,TY0,TY1,AH-0.3,MOD_TOP))
T,vol=mesh(G)
name="qs_cutter_pusher_v2_%s.stl"%v
cad.write(name,T); np.savez("Fpusher_%s.npz"%v,F=G.F.astype(np.float16),o=np.array([G.x0,G.y0,G.h0]))
print(name,len(T),"vol %.0f"%vol,"AH %.2f zd0 %.2f TONG_TOP %.1f rate %.0f gf/mm eq compress %.2f mm"%(AH,zd0,TONG_TOP,g['k_gf'],g['deq']))
from scipy import ndimage
lab,n=ndimage.label(G.F>0.5); print("separate solid bodies:",n)
