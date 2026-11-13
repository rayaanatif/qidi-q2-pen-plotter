"""Cutter bay for a GCC blade holder: hangs the holder by its flange, rail/bracket identical to pen bay v5.
Run: python3 cutter_bay.py   -> qs_cutter_bay_v1.stl  (+ Fcutter_bay.npy voxel field for the fit check)"""
import sys; sys.path.insert(0,".")
import numpy as np
from vf import *
import cad
from params import *
from module_geom import roofs
WXL,WXR=-26.37,27.23; HR=104.5; TOP=113.5; H0=63.5
G=Grid(-35,38,76,132,-1,116)
s2=np.sqrt(2)
xl_in,xr_in=WXL-0.25,WXR+0.25; ARM=5.0
def sd_rect2(x0,x1,y0,y1):
    def f(X,Y): return np.maximum(np.maximum(x0-X,X-x1),np.maximum(y0-Y,Y-y1))
    return f
foot=[(-31.62,32.48,104.9,109.9),(xl_in-ARM,xl_in,80.0,104.9),(xr_in,xr_in+ARM,80.0,104.9)]
def bracket(X,Y,H):
    d2=None
    for r in foot:
        v=sd_rect2(*r)(X,Y); d2=v if d2 is None else np.minimum(d2,v)
    dxs=np.maximum(np.abs(X-CX)-7.0,0); dys=np.maximum(104.9-Y,0); U=H0+np.hypot(dxs,dys)
    return np.maximum(np.maximum(d2,(H-TOP)),(U-H)/s2)
G.op('add',(-33,34),(79,111),(60,TOP+1),bracket)
# spine plate
G.op('add',(CX-7,CX+7),(104.5,110.5),(19,TOP),sd_box(CX-7,CX+7,104.9,109.9,19,TOP))
# tube: outside tapers 45 deg to the seat ring at the flange end (prints without overhang bracket-down)
def tube(X,Y,H):
    r=np.hypot(X-CX,Y-YT); R=np.minimum(RT,SEAT_R+(HT-H))
    return np.maximum(np.maximum(r-R,HB0-H),H-HT)
G.op('add',(CX-RT,CX+RT),(YT-RT,YT+RT),(HB0,HT+0.5),tube)
# rear web tying the tube to the spine plate (sloped top, no overhang)
WEB=[(108.0,HB0),(113.0,HB0),(113.0,HT-10.0),(109.9,HT-6.9),(108.0,HT-6.9)]
G.op('add',(CX-5.0,CX+5.0),(107.5,113.5),(HB0,HT),sd_poly_prism(WEB,(CX-5.0,CX+5.0),'x'))
# bore (flush through) + lead-in chamfer at the nose end
def bore(X,Y,H):
    r=np.hypot(X-CX,Y-YT); R=BORE_R+np.maximum(0,0.6-(H-HB0))
    return np.maximum(r-R,np.abs(H-(HB0+HT)/2)-(HT-HB0)/2-1.0)
G.op('sub',(CX-BORE_R-1,CX+BORE_R+1),(YT-BORE_R-1,YT+BORE_R+1),(HB0-1,HT+1),bore)
# dovetail grooves (as v5)
for sign in (-1,1):
    wx=WXR if sign>0 else WXL
    def groove(X,Y,H,sign=sign,wx=wx):
        n=(X-wx)*sign
        d_flank=(np.abs(H-HR)-(2.4+n+0.22))/s2
        return np.maximum(np.maximum(d_flank,n-2.62),np.maximum(-0.6-n,np.maximum(79.0-Y,Y-102.0)))
    x0,x1=(WXL-3.2,WXL+0.8) if sign<0 else (WXR-0.8,WXR+3.2)
    G.op('sub',(x0,x1),(78,103),(HR-8,HR+8),groove)
# stiffening flanges + wings (as v5); they also form the module channel (inner faces at CX +-6.8)
FL=[(104.9,TOP),(112.5,TOP),(112.5,58.0),(110.6,56.1),(110.6,47.5),(104.9,47.5)]
for (xa,xb) in ((CX+6.8,CX+10.4),(CX-10.4,CX-6.8)):
    G.op('add',(xa,xb),(104.5,113),(47,TOP+0.5),sd_poly_prism(FL,(xa,xb),'x'))
WG=[(110.0,TOP),(120.0,TOP),(120.0,64.0),(110.0,54.0)]
for (xa,xb) in ((CX+8.5,CX+10.8),(CX-10.8,CX-8.5)):
    G.op('add',(xa,xb),(109,121),(53,TOP+0.5),sd_poly_prism(WG,(xa,xb),'x'))
# detent notches in the channel walls (3 positions, 3 mm apart): flat roof catches the module, 45 deg floor
for roof in roofs():
    for sg in (-1,1):
        NP=[(6.7,roof),(7.9,roof),(7.9,roof-0.5),(6.7,roof-1.7)]   # (|x-CX|, h)
        def notch(X,Y,H,sg=sg,roof=roof):
            u=sg*(X-CX); d=sd_poly2(u,H,NP)
            return np.maximum(d,np.maximum(110.3-Y,Y-113.2))
        G.op('sub',((CX-8.2) if sg<0 else (CX+6.4),(CX-6.4) if sg<0 else (CX+8.2)),(110,113.5),(roof-2,roof+1),notch)
np.save("Fcutter_bay.npy",G.F.astype(np.float16))
T,vol=mesh(G)
cad.write("qs_cutter_bay_v1.stl",T)
print("qs_cutter_bay_v1.stl",len(T),"vol %.0f mm3"%vol,"roofs",[round(r,2) for r in roofs()])
from scipy import ndimage
lab,n=ndimage.label(G.F>0.5); print("separate solid bodies:",n)
