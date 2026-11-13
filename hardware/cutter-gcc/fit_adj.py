import sys; sys.argv=['x']
exec(open('fitcheck.py').read().split('print("holder vs bay')[0])
def load(n):
    z=np.load(n); return z['F'].astype(np.float32),z['o']
def put(F,o,dh=0.0,hmin=None):
    out=np.zeros_like(Bf); ix=int(round((o[0]-G0.x0)/ST)); iy=int(round((o[1]-G0.y0)/ST)); ih=int(round((o[2]+dh-G0.h0)/ST))
    ny,nh,nx=F.shape; out[iy:iy+ny,ih:ih+nh,ix:ix+nx]=F; return out
Ff,of=load("Fadj_frame.npz"); Fp,op_=load("Fadj_plunger.npz"); Fr,orr=load("Fadj_rod.npz"); Fk,ok=load("Fadj_key.npz")
frame=put(Ff,of); key=put(Fk,ok)
print("frame vs bay: %.2f   key vs bay: %.2f   key vs frame: %.2f   key vs rod(D=0): %.2f"%(ov(frame,Bf),ov(key,Bf),ov(key,frame),ov(key,put(Fr,orr))))
for d in (0.0,3.0,6.0):
    print("rod pure shift %.0f vs frame (thread clearance): %.2f mm3"%(d,ov(put(Fr,orr,-d),frame)))
# plunger cap+tab only (h>=AH-0.4) shifted down by delta vs frame
g=geom('adj'); ih0=int(round((g['AH']-0.4-op_[2])/ST)); cap=Fp.copy(); cap[:,:ih0,:]=0
for d in (0.0,3.5,7.0):
    print("plunger cap shift %.1f vs frame: %.2f mm3"%(d,ov(put(cap,op_,-d),frame)))
print("rod (D=0) vs plunger cap: %.2f"%ov(put(Fr,orr),put(Fp,op_)))
H=holder(XEQ)
print("frame vs holder: %.2f   rod vs holder %.2f  plunger(relaxed,above disc) vs bay %.2f"%(ov(frame,H),ov(put(Fr,orr),H),ov(put(Fp,op_),Bf)))
# insertion: frame, then key, from above/front
worst=0
for dh in np.arange(0,40,1.0):
    sh=int(round(dh/ST)); S=np.zeros_like(frame); S[:,sh:,:]=frame[:,:frame.shape[1]-sh,:]; worst=max(worst,ov(S,Bf)+ov(S,H))
print("frame drop-in sweep (40 mm above) vs bay+holder max overlap %.2f"%worst)
worst=0
for dy in np.arange(0,12,0.6):
    sh=int(round(dy/ST)); S=np.zeros_like(key); S[sh:,:,:]=key[:key.shape[0]-sh,:,:]; worst=max(worst,ov(S,Bf)+ov(S,frame)+ov(S,put(Fr,orr,-0.0)))
print("key slide-in sweep (12 mm out front) overlap with bay+frame+rod: %.2f (0 expected at final position, pockets engaged)"%worst)
# knob vs key at Delta=0..7, knob vs tongue/key envelope
for d in (0.0,7.0):
    print("knob(rod) at Delta=%.0f vs key %.2f vs frame %.2f"%(d,ov(put(Fr,orr,-d),key),ov(put(Fr,orr,-d),frame)))
print("---- detail")
rod=put(Fr,orr)
ihk=int(round((KB0-orr[2]-0.0)/ST)) if False else None
from module_geom import *
KB0=HN1=None
