from adjust import *
from bay import build_bay
bay=build_bay(); fr=frame(); pl=plunger(); rd=rod(); ky=key()
def ov(a,b): return (a&b).volume
print("plunger up-stop: tab clearance to slot ceiling 0.4 -> lifted 0.3:",round(ov(Pos(0,0,0.3)*pl,fr),3)," lifted 0.5 (should touch):",round(ov(Pos(0,0,0.5)*pl,fr),3))
for d in (0,1.5,3,5,7):
    r=Pos(0,0,-d)*(Pos(CX,YT,0)*(Rot(0,0,-360*d/TP)*(Pos(-CX,-YT,0)*rd)))     # right-hand screw: CW turn = down
    p=Pos(0,0,-d)*pl
    print("preload %.1f mm: rod(screwed)/frame %.3f  plunger/frame %.3f  rod/plunger %.3f  rod/bay %.3f"%(d,ov(r,fr),ov(p,fr),ov(r,p),ov(r,bay)))
# thread clearance: radial gaps by shrinking test: rod offset 0.15 mm sideways should still not bind?
r=Pos(0.15,0,0)*rd; print("rod 0.15 off-centre / frame:",round(ov(r,fr),3))
r=Pos(0.3,0,0)*rd; print("rod 0.30 off-centre / frame:",round(ov(r,fr),3))
