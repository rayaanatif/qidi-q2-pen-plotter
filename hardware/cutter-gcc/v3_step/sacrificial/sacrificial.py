"""Breakaway sacrificial shell for the printed coils (pusher modules + adjuster plunger).
A split (C-shaped) thin tube stands round the coil with a radial gap and is tied to the coil tips by tiny
breakaway tabs, so the slender coil cannot whip while printing. Peel it off after printing."""
import math
from lib import *
GAP_S=0.35      # radial gap coil tip -> shell wall
WALL_S=1.2      # shell wall (3 perimeters @0.4)
TAB_W=0.8       # tab width (tangential), tab height TAB_H (z): neck cross-section ~0.3 mm2
TAB_H=0.4
TAB_ANG=(0,120,240)   # tab angles on every turn
SLIT_DEG=300.0; SLIT_W=1.4   # split the tube here (peel-off line), away from the tabs
def shell(R,A,B,P,N,ZS,zd0,cx=CX,cy=YT):
    tip=R+A-0.15
    ri=tip+GAP_S; ro=ri+WALL_S
    zc0=ZS+(N-1)*P
    ztop=zc0-0.2
    tube=cyl(ro,zd0,ztop,cx,cy)-cyl(ri,zd0-1,ztop+1,cx,cy)
    slit=Pos(cx,cy,0)*Rot(0,0,SLIT_DEG)*box(ri-0.5,ro+0.5,-SLIT_W/2,SLIT_W/2,zd0-1,ztop+1)
    tube=tube-slit
    brim=cyl(ro+2.5,zd0,zd0+0.4,cx,cy)-cyl(ri,zd0-1,zd0+1,cx,cy)-Pos(cx,cy,0)*Rot(0,0,SLIT_DEG)*box(ri-0.5,ro+3.5,-SLIT_W/2,SLIT_W/2,zd0-1,zd0+1)
    out=tube+brim
    n=0
    for k in range(N-1):
        for a in TAB_ANG:
            z=ZS+k*P+P*a/360.0
            if z>ztop-TAB_H: continue
            t=Pos(cx,cy,0)*Rot(0,0,a)*box(tip-0.15,ri+0.15,-TAB_W/2,TAB_W/2,z-TAB_H/2,z+TAB_H/2)
            out=out+t; n+=1
    return out,n,(ri,ro,ztop)
