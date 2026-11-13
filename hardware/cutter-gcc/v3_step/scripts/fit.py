from adjust import *
from bay import build_bay
import time
bay=build_bay(); fr=frame(); pl=plunger(); rd=rod(); ky=key()
def ov(a,b): 
    try: return (a&b).volume
    except Exception as e: return float('nan')
def holder(x):
    return (cyl(BARREL_D/2,HB0,HT)+cyl(FLANGE_D/2,HT,HT+FLANGE_T)+cyl(RING_D/2,HT+FLANGE_T,RING_TOP)+cyl(PIN_D/2,RING_TOP-0.5,PIN0-x))
print("holder vs bay (rest, nose flush):",round(ov(holder(0),bay),3), " holder vs bay shifted 3mm up:",round(ov(Pos(0,0,3)*holder(0),bay),3))
print("frame vs bay:",round(ov(fr,bay),3),"  key vs bay:",round(ov(ky,bay),3),"  key vs frame:",round(ov(ky,fr),3))
print("frame vs holder:",round(ov(fr,holder(8)),3))
for dz in (0,3,6,9,10.5):
    print("plunger lifted %.1f: vs frame %.3f  vs bay %.3f  vs rod %.3f"%(dz,ov(Pos(0,0,dz)*pl,fr),ov(Pos(0,0,dz)*pl,bay),ov(Pos(0,0,dz)*pl,rd)))
for dz in (0,-3.5,-7):
    for rot in (0,45,90,137):
        r=Pos(0,0,dz)*(Pos(CX,YT,0)*(Rot(0,0,rot)*(Pos(-CX,-YT,0)*rd)))
        print("rod down %.1f rot %3d: vs frame %.3f  vs bay %.3f"%(-dz,rot,ov(r,fr),ov(r,bay)))
for x in (0,4,6,8):
    print("pin depression %d: holder vs plunger(lifted so disc on pin) %.3f"%(x,ov(holder(x),Pos(0,0,(PIN0-x)-zd0)*pl)))
