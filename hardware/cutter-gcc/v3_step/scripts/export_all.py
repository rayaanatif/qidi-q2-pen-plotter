import os,collections
from adjust import *
from pusher import pusher
from bay import build_bay
os.makedirs("out",exist_ok=True)
flip=lambda p: Pos(0,0,p.bounding_box().max.Z+p.bounding_box().min.Z)*(Rot(180,0,0)*Pos(0,-(p.bounding_box().min.Y+p.bounding_box().max.Y)/2*0,0)*p) 
def flipped(p):
    q=Rot(180,0,0)*p; return Pos(0,0,-q.bounding_box().min.Z)*q
parts={"qs_cutter_bay_v3":(build_bay(),True),
       "qs_cutter_adj_frame_v3":(frame(),False),"qs_cutter_adj_plunger_v3":(plunger(),False),
       "qs_cutter_adj_rod_knob_v3":(rod(),True),"qs_cutter_key_v3":(key(),False)}
for v in ('soft','std','firm','hard'): parts["qs_cutter_pusher_v3_%s"%v]=(pusher(v),False)
for nm,(p,fl) in parts.items():
    assert p.is_valid and len(p.solids())==1,nm
    export_step(p,"out/%s_model_orientation.step"%nm)
    pp=flipped(p) if fl else p
    if not fl: pp=Pos(0,0,-p.bounding_box().min.Z)*p
    export_step(pp,"out/%s_print.step"%nm)
    export_stl(pp,"out/%s_print.stl"%nm,tolerance=0.005,angular_tolerance=0.05)
    r=import_step("out/%s_print.step"%nm)
    c=collections.Counter(str(f.geom_type).split('.')[-1] for f in r.faces())
    print("%-30s reimport valid=%s vol=%.1f faces=%d %s"%(nm,r.is_valid,r.volume,len(r.faces()),dict(c)))
