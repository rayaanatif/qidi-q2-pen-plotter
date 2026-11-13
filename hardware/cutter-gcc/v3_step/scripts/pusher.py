"""Fixed-force pusher modules (soft/std/firm/hard): disc + printed coil + land + arm + tongue, one solid, prints disc-down, no supports."""
import os,sys
from spring import *
TW=6.4; TY0,TY1=110.3,112.3; ARM_T=3.0; LAND_IN=3.9; DISC_R=5.9
def pusher(v):
    g=geom(v); R,A,B,P,N,ZS,AH,zd0=g['R'],g['A'],g['B'],g['P'],g['N'],g['ZS'],g['AH'],g['zd0']
    LAND_OUT=R+A+0.9
    disc=cyl(DISC_R,zd0,zd0+TD)
    c=coil(R,A,B,P,N,ZS); l=land(R,A,B,P,N,ZS,AH,LAND_IN,LAND_OUT)
    arm=cyl(LAND_OUT,AH-0.3,AH+ARM_T)+box(CX-TW,CX+TW,TY0,YT,AH-0.3,AH+ARM_T)
    arm=arm-revolve_rz([(0,AH-0.3),(LAND_IN,AH-0.3),(0,AH-0.3+LAND_IN)])          # 45 deg conical roof inside the bore (no bridging)
    tongue=box(CX-TW,CX+TW,TY0,TY1,AH-0.3,MOD_TOP)
    return disc+c+l+arm+tongue
if __name__=="__main__":
    os.makedirs("out",exist_ok=True)
    for v in ('soft','std','firm','hard'):
        p=pusher(v); info(v,p); save(p,"out/qs_cutter_pusher_v3_%s.step"%v)
