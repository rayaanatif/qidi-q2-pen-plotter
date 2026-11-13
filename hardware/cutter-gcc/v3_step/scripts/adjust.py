"""Adjustable-force pusher: FRAME, PLUNGER, ROD+KNOB, KEY as parametric B-reps (true cylinders / cones / helical sweeps)."""
import os
from spring import *
g=geom('adj'); R,A,B,P,N,ZS,AH,zd0=g['R'],g['A'],g['B'],g['P'],g['N'],g['ZS'],g['AH'],g['zd0']
CAP_T=3.0; CAP_R=6.7; LAND_IN=3.9
TUBE_RI,TUBE_RO=7.0,8.1
TW=6.4; TY0,TY1=110.3,112.3
HT0=AH-DMAX-3.0
CAPTOP=AH+CAP_T
NUT_T=10.0; HN1=MOD_TOP; HN0=HN1-NUT_T
CONE=TUBE_RI-5.3
TP,TDEP,TROOT=3.0,1.1,3.9          # thread: pitch 3, 90 deg included angle (45 deg flanks), crest r 5.0
CL=0.3                              # radial print clearance nut <-> rod
def thread_phase(z_min,z_max):
    """start height of the helix (tooth centre at 1.5 mod 3 at angle 0) and number of turns covering [z_min,z_max]"""
    k=math.ceil((z_min-1.5)/TP); z0=1.5+TP*k
    return z0,(z_max-z0)/TP
def frame():
    body=cyl(TUBE_RO,HT0,HN1)+box(CX-TW,CX+TW,TY0,TY1,HT0,HN1)
    h1=HN0-CONE
    bore=revolve_rz([(0,HT0-1),(TUBE_RI,HT0-1),(TUBE_RI,h1),(TROOT+CL,h1+(TUBE_RI-TROOT-CL)),(TROOT+CL,HN1+1),(0,HN1+1)])
    body=body-bore
    # internal thread groove: trapezoid, 45 deg flanks, 0.3 mm radial / axial clearance to the rod thread
    z0,turns=thread_phase(HN0-4,HN1+4)
    hw=lambda r:1.3-(r-(TROOT+CL))          # half width at radius r: 1.3 at 4.2 -> 0.2 at 5.3
    groove=helix_sweep([(TROOT+CL-0.3,-hw(TROOT+CL-0.3)),(TROOT+CL+TDEP,-0.2),(TROOT+CL+TDEP,0.2),(TROOT+CL-0.3,hw(TROOT+CL-0.3))],z0,turns,TP,TROOT+CL+0.5)
    body=body-groove
    # front slot for the plunger tab (open at the bottom) + scale ticks
    TABC=AH+2.0
    body=body-box(CX-1.3,CX+1.3,YT+6,YT+9.5,HT0-1,CAPTOP+0.4)   # slot ceiling 0.4 mm above the tab (up-stop with clearance)
    for d in range(0,int(DMAX)+1):
        wl=2.6 if d in (0,5) else 1.6
        body=body-box(CX+1.4,CX+1.4+wl,YT+7.25,YT+8.6,TABC-d-0.2,TABC-d+0.2)
    return body
def plunger():
    disc=cyl(5.9,zd0,zd0+TD)
    c=coil(R,A,B,P,N,ZS); l=land(R,A,B,P,N,ZS,AH,LAND_IN,CAP_R)
    capr=revolve_rz([(0.6,CAPTOP),(CAP_R,CAPTOP),(CAP_R,AH-0.3),(LAND_IN,AH-0.3)])        # 45 deg conical roof inside the bore (no bridging)
    TABP=[(YT+6.0,CAPTOP),(YT+8.6,CAPTOP),(YT+8.6,CAPTOP-1.1),(YT+6.9,CAPTOP-2.8),(YT+6.0,CAPTOP-2.8)]
    tab=prism_x(TABP,CX-1.0,CX+1.0)
    return disc+c+l+capr+tab
KB0=HN1+0.5+DMAX; KNOB_R,KNOB_T=5.6,7.2; RB0=CAPTOP+0.1
def rod():
    core=cyl(TROOT,RB0,KB0+0.5)
    z0,turns=thread_phase(KB0-20.0,KB0+1.0)
    hwm=lambda r:1.3-(r-TROOT)                 # 1.3 at root r=3.9 -> 0.2 at crest r=5.0
    th=helix_sweep([(TROOT-0.1,-hwm(TROOT-0.1)),(TROOT+TDEP,-0.2),(TROOT+TDEP,0.2),(TROOT-0.1,hwm(TROOT-0.1))],z0,turns,TP,TROOT+0.5)
    knob=cyl(KNOB_R,KB0,KB0+KNOB_T)
    for k in range(12):                              # 12 round grip flutes (R1.2 arcs, 0.6 deep)
        a=math.radians(15+30*k); knob=knob-cyl(1.2,KB0-1,KB0+KNOB_T+1,CX+6.2*math.cos(a),YT+6.2*math.sin(a))
    knob=knob-box(CX-0.4,CX+0.4,YT,YT+KNOB_R+1,KB0+KNOB_T-0.6,KB0+KNOB_T+1)               # pointer groove
    return core+th+knob
def key():
    k=box(CX-7.7,CX+7.7,110.45,112.25,KEY_H0,KEY_H1)
    for sg in (-1,1):
        x0,x1=sorted([CX+sg*6.4,CX+sg*7.7]); k=k+box(x0,x1,112.0,115.2,KEY_H0,KEY_H1)
    return k
if __name__=="__main__":
    os.makedirs("out",exist_ok=True)
    for nm,f in (("frame",frame),("plunger",plunger),("rod_knob",rod),("key",key)):
        p=f(); info(nm,p); save(p,"out/qs_cutter_adj_%s_v3.step"%nm)
