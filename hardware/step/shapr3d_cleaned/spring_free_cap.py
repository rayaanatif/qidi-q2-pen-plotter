"""Spring-free cutter: bay rib + rigid height-adjustable cap. Model frame (x, y, h)."""
from build123d import *
CX=0.4; YT=118.2
PIN0=45.2; X0=4.0; TD=1.5
Y_FACE=109.91          # spine front face
RB_Y0,RB_Y1=109.4,112.4; RB_W0,RB_W1=3.2,4.7     # dovetail rib half widths at base / top
RB_H0,RB_H1=56.0,96.0
CLR=0.3                # cap-to-rib clearance
PIL_D=2.6; PIL_Y0=106.2; HS=(68.0,80.0)          # pilot holes (screw heights)
def rib_profile(clr=0.0,y0=RB_Y0,y1=RB_Y1):
    w=lambda y: RB_W0+(y-RB_Y0)*(RB_W1-RB_W0)/(RB_Y1-RB_Y0)+clr
    return [(CX-w(y0),y0),(CX+w(y0),y0),(CX+w(y1),y1),(CX-w(y1),y1)]
def prism_h(pts_xy,h0,h1):
    f=Face(Wire.make_polygon([Vector(x,y,h0) for x,y in pts_xy],close=True))
    return extrude(f,h1-h0)
def add_rib(bay):
    rib=prism_h(rib_profile(),RB_H0,RB_H1)
    out=bay+rib
    for h in HS:
        hole=Pos(CX,(PIL_Y0+RB_Y1+1)/2,h)*Rot(90,0,0)*Cylinder(PIL_D/2,RB_Y1+1-PIL_Y0)
        out=out-hole
    return out
# ---- cap
DISC_R=4.5; COL_R=3.8; ARM0,ARM1=52.0,55.0; ZT=90.0
WEB_X=6.4; WEB_Y0=Y_FACE+CLR; WEB_Y1=RB_Y1+CLR+2.0     # 110.21 .. 114.7
SLOT_W=3.4; TRAVEL=7.0
def cap(x0=X0):
    zd=PIN0-x0
    disc=Pos(CX,YT,zd)*Cylinder(DISC_R,TD,align=(Align.CENTER,Align.CENTER,Align.MIN))
    col=Pos(CX,YT,zd+TD-0.01)*Cylinder(COL_R,ARM0-(zd+TD)+0.02,align=(Align.CENTER,Align.CENTER,Align.MIN))
    yf=RB_Y1+CLR      # groove floor
    arm=Pos(CX,(yf+YT+COL_R)/2,(ARM0+ARM1)/2)*Box(2*COL_R,YT+COL_R-yf,ARM1-ARM0)
    web=Pos(CX,(WEB_Y0+WEB_Y1)/2,(ARM0+ZT)/2)*Box(2*WEB_X,WEB_Y1-WEB_Y0,ZT-ARM0)
    groove=prism_h(rib_profile(CLR,WEB_Y0-0.5,yf),ARM0-7.9,ZT+1)
    # 45 deg skirt under the arm/web so the cap prints disc-down with no overhang (kept out of the groove, off the spine)
    SK=6.8
    cone=Pos(CX,YT,ARM0-SK)*Cone(COL_R,COL_R+SK,SK,align=(Align.CENTER,Align.CENTER,Align.MIN))
    clipb=Pos(CX,(WEB_Y0+YT+COL_R)/2,(ARM0-SK+ARM0)/2)*Box(2*WEB_X,YT+COL_R-WEB_Y0,SK+0.02)
    skirt=cone&clipb
    body=disc+col+arm+web+skirt-groove
    for h in HS:
        # slot centred on the screw height at the nominal setting: slot is (TRAVEL+SLOT_W) long
        zc=h-(PIN0-X0-(PIN0-x0))      # nominal
        L=TRAVEL+SLOT_W
        slot=Pos(CX,(yf+WEB_Y1)/2,h)*Rot(90,0,0)*SlotOverall(L,SLOT_W,rotation=90)
        slot=extrude(Plane.XZ.offset(-(yf-0.5))*Pos(CX,h)*SlotOverall(L,SLOT_W,rotation=90),amount=-(WEB_Y1-yf+1.0))
        body=body-slot
    return body
