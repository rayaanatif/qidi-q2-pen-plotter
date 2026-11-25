"""Print-only toolhead cover with a Sunon 40x40x10 fan on the front face (blows through the vent window onto the heatbreak/heatsink).
Model frame: x across, y depth (front = +y), z = tool axis (cover bottom z=14.5)."""
from build123d import *
from tomodel import *
CX=0.4
def box(x0,x1,y0,y1,z0,z1): return Pos((x0+x1)/2,(y0+y1)/2,(z0+z1)/2)*Box(x1-x0,y1-y0,z1-z0)
YF=104.5                      # front outer face of the cover wall
ZC=66.5                       # fan centre: fan top edge 72.0 mm above the cover bottom (z=14.5)
FAN=40.0; FCL=0.4             # fan size, pocket clearance
PAD_T=4.0; RIM_T=1.2; RIM_H=3.0
FAN_T=10.0
HOLE=16.0                     # fan hole spacing/2 (32 mm pattern)
PIL_D=1.8; PIL_DEPTH=5.0      # M2 self-tap pilot
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
def build_cover():
    cov=load_cover()
    # vent window through wall (opens the slot field to a single window)
    cov=cov+fills()
    cov=cov-box(CX-WX,CX+WX,100,YF+PAD_T+1,WZ0,WZ1)-bevel()
    # mounting pad
    ph=FAN/2+FCL/2+RIM_T
    pad=box(CX-ph,CX+ph,YF-0.3,YF+PAD_T,ZC-ph,ZC+ph)
    zt=ZC+ph
    w=wedge()
    pad=pad+w
    pad=pad-box(CX-WX,CX+WX,100,YF+PAD_T+1,WZ0,WZ1)-bevel()
    # rim (locates the fan), notched at the middle of each side
    ro=ph; ri=FAN/2+FCL/2
    rim=box(CX-ro,CX+ro,YF+PAD_T-0.01,YF+PAD_T+RIM_H,ZC-ro,ZC+ro)-box(CX-ri,CX+ri,YF+PAD_T-1,YF+PAD_T+RIM_H+1,ZC-ri,ZC+ri)
    # wire notches: both ends of the top rim, plus bottom/sides middle
    rim=rim-box(CX-5,CX+5,YF+PAD_T-1,YF+PAD_T+RIM_H+1,ZC-ro-0.5,ZC-ri+0.5)
    rim=rim-box(CX-ro-0.5,CX-ri+0.5,YF+PAD_T-1,YF+PAD_T+RIM_H+1,ZC-5,ZC+5)
    rim=rim-box(CX+ri-0.5,CX+ro+0.5,YF+PAD_T-1,YF+PAD_T+RIM_H+1,ZC-5,ZC+5)
    body=cov+pad+rim
    # M2 self-tap pilots at 32 mm pattern
    for sx in (1,-1):
        for sz in (1,-1):
            h=Pos(CX+sx*HOLE,YF+PAD_T-PIL_DEPTH/2+0.5,ZC+sz*HOLE)*Rot(90,0,0)*Cylinder(PIL_D/2,PIL_DEPTH+1)
            body=body-h
    return body
def bars():
    """two flat clamp bars (print flat): stadium 6 wide x 40 long, 1.2 thick, M2 clearance holes on the 32 mm fan pattern"""
    L=2*HOLE+8; W=6.0; T=1.2
    def one():
        b=extrude(Plane.XY*SlotOverall(L,W),amount=T)
        for sg in (1,-1): b=b-Pos(sg*HOLE,0,T/2)*Cylinder(1.2,T+1)
        return b
    return Pos(0,-(W/2+1.5),T/2-0.0)*one()+Pos(0,(W/2+1.5),0)*one() if False else (Pos(0,-(W/2+1.5),0)*one(), Pos(0,(W/2+1.5),0)*one())
if __name__=="__main__":
    c=build_cover(); bb=c.bounding_box()
    print('cover valid',c.is_valid,'solids',len(c.solids()),'vol %.0f'%c.volume,[round(v,1) for v in (bb.min.X,bb.min.Y,bb.min.Z,bb.max.X,bb.max.Y,bb.max.Z)])
    export_step(c,'out/fan_cover_model.step')
