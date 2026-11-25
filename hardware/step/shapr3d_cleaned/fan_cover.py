"""Print-only toolhead cover with a Sunon 40x40x10 fan on the front face (blows through the vent window onto the heatbreak/heatsink).
Model frame: x across, y depth (front = +y), z = tool axis (cover bottom z=14.5)."""
from build123d import *
from tomodel import *
import math
CX=0.4
def box(x0,x1,y0,y1,z0,z1): return Pos((x0+x1)/2,(y0+y1)/2,(z0+z1)/2)*Box(x1-x0,y1-y0,z1-z0)
YF=104.5                      # front outer face of the cover wall
ZC=66.5                       # fan centre: fan top edge 72.0 mm above the cover bottom (z=14.5)
FAN=40.0; FCL=0.4             # fan size, pocket clearance
PAD_T=4.0; RIM_T=1.2; RIM_H=3.0; PAD_Z=28.0     # pad half-height (room for the clamp-bracket feet)
FAN_T=10.0
HOLE=16.0                     # fan hole spacing/2 (32 mm pattern)
NUT_AF=4.2; NUT_D=1.8; SCR_HOLE=2.4; HOLE_X=17.5; FOOT_W=4.45; FOOT_T=5.5   # M2 nut trap (nut 4.0 AF x 1.6), M2x10 screws
WX=13.8                       # vent window half width (keeps clear of the M2 pilots at +-16)
WZ0=ZC-FAN/2+0.1; WZ1=ZC+FAN/2-2.0   # vent window z range
# wire gutter
RT=1.2; GAP=2.8; RH=1.8; LID=1.0
def load_cover():
    U=import_step("/mnt/user-data/uploads/90644b4f-stepfiles.step").solids()
    cov=xform(U[0],MAT_COV,T_COV)
    # remove the side dovetails (anything beyond the side plates)
    cov=cov-box(27.24,40,50,120,10,130)-box(-40,-26.38,50,120,10,130)
    return cov.solids()[0] if len(cov.solids())>0 else cov
def prism_x(pts_yz,x0,x1):
    f=Face(Wire.make_polygon([Vector(x0,y,z) for y,z in pts_yz],close=True))
    p=extrude(f,x1-x0); bb=p.bounding_box()
    return Pos(x0-bb.min.X,0,0)*p
def wedge():
    """45 deg gusset above the pad so the pad's top face is not a 7 mm horizontal cantilever when printed roof-down"""
    ph=FAN/2+FCL/2+RIM_T; zt=ZC+ph; y0=YF-0.3; y1=YF+PAD_T+RIM_H
    return prism_x([(y0,zt-0.01),(y1,zt-0.01),(y0,zt+(y1-y0))],CX-ph,CX+ph)
def bevel():
    """45 deg bevel on the model-lower edge of the vent window (the print ceiling), wider on the fan side"""
    zb=WZ0; yi=102.6; yo=YF+PAD_T+1.0
    return prism_x([(yi,zb),(yo,zb),(yo,zb-(yo-yi))],CX-WX,CX+WX)
def fills():
    """close the outer ends of the original vent slots behind the pad so the pilots have solid wall around them"""
    ph=FAN/2+FCL/2+RIM_T
    return box(CX+WX,CX+ph,102.8,YF+0.2,ZC-ph,ZC+ph)+box(CX-ph,CX-WX,102.8,YF+0.2,ZC-ph,ZC+ph)
def mirror_x(s): return s.mirror(Plane.YZ.offset(CX))
def gutter_right():
    """rails + lids for the right-hand wire path: up the front face, across at z=89.3-94.1, then back along the side plate"""
    out=[]
    # vertical run on the front face
    xl=CX+16.0
    zlo,zhi=ZC+FAN/2+FCL/2+RIM_T-0.4,94.1   # rails start at the pad top and fuse into the wedge      # start just above the pad
    yb=YF-0.2; yt=YF+RH
    out.append(box(xl,xl+RT,yb,yt,zlo,zhi))                      # left rail
    zH0=89.3
    out.append(box(xl+RT+GAP,xl+2*RT+GAP,yb,yt,zlo,zH0+RT))      # right rail (stops at the elbow)
    # horizontal run to the right edge
    xe=24.1
    out.append(box(xl+RT+GAP,xe,yb,yt,zH0,zH0+RT))               # lower rail
    out.append(box(xl,xe,yb,yt,zH0+RT+GAP,zH0+2*RT+GAP))         # upper rail
    # lids on the front runs
    
    out.append(box(xe-6,xe-1,yt-LID,yt,zH0,zH0+2*RT+GAP))
    # side plate run (outer face x=27.23), runs back from the corner to the rear
    xs=27.23-0.2; xt=27.23+RH
    y0,y1=71.0,100.4
    out.append(box(xs,xt,y0,y1,zH0,zH0+RT))
    out.append(box(xs,xt,y0,y1,zH0+RT+GAP,zH0+2*RT+GAP))
    for yc in (96.0,85.0,74.0): out.append(box(xt-LID,xt,yc-3,yc+3,zH0,zH0+2*RT+GAP))
    return out
def hexagon(cx,cz,af):
    R=af/2/math.cos(math.radians(30))
    return [(cx+R*math.cos(math.radians(30+60*k)),cz+R*math.sin(math.radians(30+60*k))) for k in range(6)]
def prism_y(pts_xz,y0,y1):
    f=Face(Wire.make_polygon([Vector(x,y0,z) for x,z in pts_xz],close=True))
    p=extrude(f,y1-y0); bb=p.bounding_box()
    return Pos(0,y0-bb.min.Y,0)*p
def build_cover():
    cov=load_cover()
    ph=FAN/2+FCL/2+RIM_T                       # pad half width (x) = 21.8
    pz=PAD_Z                                   # pad half height (z)
    # close the wall behind the pad (covers the old slot field), then open the vent window
    cov=cov+box(CX-ph,CX+ph,102.8,YF+0.2,ZC-pz,ZC+pz)
    cov=cov-box(CX-WX,CX+WX,100,YF+PAD_T+1,WZ0,WZ1)-bevel()
    pad=box(CX-ph,CX+ph,YF-0.3,YF+PAD_T,ZC-pz,ZC+pz)
    zt=ZC+pz
    pad=pad+prism_x([(YF-0.3,zt-0.01),(YF+PAD_T+RIM_H,zt-0.01),(YF-0.3,zt+(PAD_T+RIM_H+0.3))],CX-ph,CX+ph)   # 45 deg gusset above the pad
    pad=pad-box(CX-WX,CX+WX,100,YF+PAD_T+1,WZ0,WZ1)-bevel()
    # side rim walls (locate the fan in x); the clamp brackets hold it in z and y
    ri=FAN/2+FCL/2
    rim=Compound([])
    for sg in (1,-1):
        x0,x1=(CX+ri,CX+ph) if sg>0 else (CX-ph,CX-ri)
        w=box(x0,x1,YF+PAD_T-0.01,YF+PAD_T+RIM_H,ZC-ri,ZC+ri)-box(x0-1,x1+1,YF+PAD_T-1,YF+PAD_T+RIM_H+1,ZC-4,ZC+4)   # lead notch
        rim=w if not rim.solids() else rim+w
    body=cov+pad+rim
    # captive M2 nut traps + clearance holes for the clamp brackets (nuts drop in from the front under the feet)
    for sx in (1,-1):
        for sz in (1,-1):
            cx_,cz_=CX+sx*HOLE_X,ZC+sz*(FAN/2+FOOT_W)
            hexp=prism_y(hexagon(cx_,cz_,NUT_AF),YF+PAD_T-NUT_D,YF+PAD_T+1)
            body=body-hexp
            hole=Pos(cx_,YF+PAD_T-NUT_D-1.5,cz_)*Rot(90,0,0)*Cylinder(SCR_HOLE/2,3.4)
            body=body-hole
    return body
def jbracket():
    """Fan clamp bracket (print two).  J-profile extruded 44 mm: foot (5.5 thick, two M2 holes), web beside the fan edge, 1.3 mm lip over the fan face.
    Model here: extrusion axis = z (print standing on its end, no overhangs).  Profile coords: u = outward from the fan edge, v = height above the pad face."""
    L=2*HOLE_X+10
    pts=[(0.2,0),(0.2+7.5,0),(0.2+7.5,FOOT_T),(1.8,FOOT_T),(1.8,11.7),(-1.3,11.7),(-1.3,10.2),(0.2,10.2)]
    prof=Face(Wire.make_polygon([Vector(u,v,0) for u,v in pts],close=True))
    b=extrude(prof,L)
    b=Pos(0,0,-L/2)*b
    for sx in (1,-1):
        b=b-Pos(FOOT_W,0,sx*HOLE_X)*Rot(-90,0,0)*Cylinder(SCR_HOLE/2,FOOT_T*2,align=(Align.CENTER,Align.CENTER,Align.MIN))
    return b
if __name__=="__main__":
    c=build_cover(); bb=c.bounding_box()
    print('cover valid',c.is_valid,'solids',len(c.solids()),'vol %.0f'%c.volume,[round(v,1) for v in (bb.min.X,bb.min.Y,bb.min.Z,bb.max.X,bb.max.Y,bb.max.Z)])
    export_step(c,'out/fan_cover_model.step')
