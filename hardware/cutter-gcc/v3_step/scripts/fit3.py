from pusher import *
from bay import build_bay
bay=build_bay()
def holder(x): return (cyl(BARREL_D/2,HB0,HT)+cyl(FLANGE_D/2,HT,HT+FLANGE_T)+cyl(RING_D/2,HT+FLANGE_T,RING_TOP)+cyl(PIN_D/2,RING_TOP-0.5,PIN0-x))
for v in ('soft','std','firm','hard'):
    p=pusher(v); g=geom(v)
    print(v,"vs bay: %.3f"%(p&bay).volume, " shifted +/-3 mm in y:",round((Pos(0,3,0)*p&bay).volume,3),round((Pos(0,-3,0)*p&bay).volume,3)," vs holder (pin x=0): %.3f"%(p&holder(0)).volume)
    # disc touching pin at x=6: coil compressed -> only the disc/lower coil moves; check the rigid disc against holder
    d=Pos(0,0,(PIN0-6)-g['zd0'])*cyl(5.9,g['zd0'],g['zd0']+TD)
    print("    disc on pin (x=6) vs holder: %.3f"%(d&holder(6)).volume)
