"""Floating cutter cartridge: ONE printed part (sleeve + printed coil spring + skirt). No screws, springs or clips.
Axis = Z (up, as installed: nose end at z=0). Prints upright as modelled, no supports.
Usage: python3 cutter_float.py [turns] [Z0C] [bore]     (defaults: 3 turns, Z0C 44, bore 11.3)"""
import sys; sys.path.insert(0,".")
import numpy as np
from vf import *
import cad
N=int(sys.argv[1]) if len(sys.argv)>1 else 3        # coil turns incl. the land turn (3 stiffer, 4 softer)
Z0C=float(sys.argv[2]) if len(sys.argv)>2 else 44.0  # sleeve bottom face -> where the holder's pin touches the cap (sets exposure)
BORE=float(sys.argv[3]) if len(sys.argv)>3 else 11.3 # sleeve bore; slit lets it grip the 11.5 holder
SLEEVE_R=6.25            # sleeve outside radius (bay bore is 6.4)
R,A,B=8.0,1.5,1.6        # coil mean radius, radial half width, axial half height (diamond section)
GAP=1.75; P=2*B+GAP      # pitch: GAP of free space between turns = travel before the turns touch (N*GAP)
COLLAR_R,COLLAR_H=9.5,3.0
SKIRT_IN,SKIRT_OUT,SKIRT_H=9.35,11.4,12.0   # skirt slides over the bay tube (outside radius 9.2)
LAND_IN=6.7
CAP_T=2.5; RF=2.8        # cap thickness; flat contact disc radius for the pin
ZS=COLLAR_H+B-0.6        # first turn centre height (embedded 0.6 into the collar)
ZTOP_LAND=ZS+N*P+B+1.6   # flat top of the land = where the bay tube bottom sits
ZT=Z0C+CAP_T             # top of the sleeve
ZMAX=max(ZT,ZTOP_LAND+SKIRT_H)+1
G=Grid(-12,12,-12,12,-1,ZMAX+1)
TWO=2*np.pi
def polar(X,Y): return np.hypot(X,Y),np.mod(np.arctan2(Y,X),TWO)
# ---- sleeve tube + collar
def sleeve(X,Y,H):
    r,_=polar(X,Y); return np.maximum(np.maximum(r-SLEEVE_R,BORE/2-r),np.maximum(-H,H-ZT))
G.op('add',(-7,7),(-7,7),(0,ZT),sleeve)
def collar(X,Y,H):
    r,_=polar(X,Y); return np.maximum(np.maximum(r-COLLAR_R,SLEEVE_R-0.3-r),np.maximum(-H,H-COLLAR_H))
G.op('add',(-10,10),(-10,10),(0,COLLAR_H),collar)
# ---- cap: closed top with a 45-degree funnel underneath and a flat contact disc for the pin
def cap(X,Y,H):
    r,_=polar(X,Y)
    under=Z0C-np.maximum(r-RF,0.0)          # underside height at this radius
    return np.maximum(np.maximum(r-SLEEVE_R,under-H),H-ZT)
G.op('add',(-7,7),(-7,7),(Z0C-4,ZT),cap)
# ---- helical coil, diamond section (no supports needed)
def helix(X,Y,H):
    r,th=polar(X,Y)
    u=(H-ZS-P*th/TWO)/P; kk=np.round(u); v=(u-kk)*P
    d=(np.abs(r-R)/A+np.abs(v)/B-1)/np.sqrt(1/A**2+1/B**2)
    return np.where((kk>=0)&(kk<=N-1),d,1e3)
G.op('add',(-10,10),(-10,10),(COLLAR_H-1,ZTOP_LAND+1),helix)
# ---- land: the last turn thickened up to a flat top, with 45/60-degree underside, carrying the skirt
def land(X,Y,H):
    r,th=polar(X,Y)
    zc=ZS+(N-1)*P+P*th/TWO
    under=zc-B+np.abs(r-R)*B/A               # same V-slope as the wire
    return np.maximum(np.maximum(r-SKIRT_OUT,LAND_IN-r),np.maximum(under-H,H-ZTOP_LAND))
G.op('add',(-12,12),(-12,12),(ZS+(N-1)*P-B-1,ZTOP_LAND+0.1),land)
# ---- skirt: slides over the bay tube, 3 crush ribs for a friction hold, lead-in chamfer
def skirt(X,Y,H):
    r,_=polar(X,Y)
    ch=np.maximum(SKIRT_IN+0.6-(ZTOP_LAND+SKIRT_H-H)*1.0*0+0, 0)
    rin=SKIRT_IN+np.maximum(0.0,0.7-(ZTOP_LAND+SKIRT_H-H))   # 45 deg lead-in at the open end
    return np.maximum(np.maximum(r-SKIRT_OUT,rin-r),np.maximum(ZTOP_LAND-0.2-H,H-(ZTOP_LAND+SKIRT_H)))
G.op('add',(-12,12),(-12,12),(ZTOP_LAND-0.2,ZTOP_LAND+SKIRT_H),skirt)
for ang in (90,210,330):
    c,s=np.cos(np.radians(ang)),np.sin(np.radians(ang))
    def rib(X,Y,H,c=c,s=s):
        al=X*c+Y*s; ac=-X*s+Y*c
        return np.maximum(np.maximum(np.abs(ac)-0.6,np.maximum(SKIRT_IN-0.3-al,al-SKIRT_IN-0.3)),np.maximum(ZTOP_LAND-0.2-H,H-(ZTOP_LAND+SKIRT_H-1.0)))
    G.op('add',(-12,12),(-12,12),(ZTOP_LAND-0.2,ZTOP_LAND+SKIRT_H),rib)
# ---- slit in the sleeve (and collar) so the sleeve can grip the holder; stops short of the cap
G.op('sub',(-0.3,0.3),(0,6.6),(-1,ZT-CAP_T-3.5),sd_box(-0.3,0.3,0,6.6,-1,ZT-CAP_T-3.5))
# ---- cut the land/helix away from the sleeve interior bore again (keep the bore clear)
def bore(X,Y,H):
    r,_=polar(X,Y); return np.maximum(r-BORE/2,np.maximum(-1-H,H-(Z0C-4.2)))
G.op('sub',(-7,7),(-7,7),(-1,Z0C-4),bore)
T,vol=mesh(G)
name="qs_cutter_float_v1_%dturn_bore%.1f.stl"%(N,BORE)
cad.write(name,T)
print(name,len(T),"vol %.0f mm3"%vol,"ZB(land top, sleeve drop below bay) %.1f"%ZTOP_LAND,"ZT %.1f"%ZT,"travel to solid %.1f"%((N-1)*GAP))
# rough spring rate from helical-beam torsion (G~500 MPa printed PETG, section = ~0.6 of the inscribed ellipse)
J=0.6*np.pi*A**3*B**3/(A**2+B**2)
k=500*J/(2*np.pi*R**3*(N-1))   # the last turn is the stiff land, so N-1 turns flex
print("estimated rate %.2f N/mm = %.0f gf/mm (+/-40%%)"%(k,k*101.97))
if "--png" in sys.argv:
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    F=G.F; iy=int(round((0-G.y0)/ST)); ix=int(round((0-G.x0)/ST))
    fig,ax=plt.subplots(1,3,figsize=(15,9),dpi=110)
    ex=[G.x0,G.x0+ST*(F.shape[2]-1),G.h0,G.h0+ST*(F.shape[1]-1)]
    ax[0].imshow(F[iy].T if False else F[iy],origin='lower',extent=ex,cmap='gray_r',aspect='equal'); ax[0].set_title('section y=0 (x horizontal, z up)')
    ey=[G.y0,G.y0+ST*(F.shape[0]-1),G.h0,G.h0+ST*(F.shape[1]-1)]
    ax[1].imshow(F[:,:,ix].T,origin='lower',extent=ey,cmap='gray_r',aspect='equal'); ax[1].set_title('section x=0 (y horizontal, slit at +y)')
    zl=int(round((ZTOP_LAND-2-G.h0)/ST)); ax[2].imshow(F[:,zl,:],origin='lower',extent=[G.x0,G.x0+ST*(F.shape[2]-1),G.y0,G.y0+ST*(F.shape[0]-1)],cmap='gray_r'); ax[2].set_title('plan at z=%.1f (coil/land)'%(ZTOP_LAND-2))
    fig.savefig("float_%dturn.png"%N,bbox_inches='tight')

from scipy import ndimage
lab,n=ndimage.label(G.F>0.5); print("separate solid bodies:",n)
