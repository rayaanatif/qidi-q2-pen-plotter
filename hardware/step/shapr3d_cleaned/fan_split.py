"""Qidi Q2 toolhead cover (main, prints FRONT FACE DOWN, no supports) + fan plate (prints flat).
M3 screws: head on fan front -> fan (10) -> plate (1.6) -> cover wall (1.7) -> M3 nut trapped on the INSIDE of the cover wall.  Needs M3x15 (4x)."""
from fan_cover import *
PL_T=1.6                         # fan plate thickness
BOSS_D=1.6; BOSS_HZ=4.0; BOSS_X0,BOSS_X1=12.5,20.5
NUT_SKIN=0.9                     # plastic left in front of the nut (outer face of wall)
HZ=16.0; HX=16.0                 # fan hole pattern 32x32
YIN=102.8
_HULL=None
def plan_hull():
    """convex plan outline of the shell (z=110 section) incl. its real 45 deg front corners"""
    global _HULL
    if _HULL is None:
        import trimesh
        from scipy.spatial import ConvexHull
        export_stl(load_cover(),'/tmp/_lc.stl',tolerance=0.02,angular_tolerance=0.2)
        sec=trimesh.load('/tmp/_lc.stl').section(plane_origin=[0,0,110],plane_normal=[0,0,1])
        P=sec.vertices[:,:2]; h=ConvexHull(P)
        _HULL=[tuple(map(float,P[i])) for i in h.vertices]
    return _HULL
def chamfer_front(body):
    """one continuous 45 deg flat face from the roof to the front face, across the full width (both halves and both side plates)."""
    T=1.8; y0=95.0; z_in,z_top=120.9,122.7; YW=104.5
    K_in=y0+z_in; K_out=K_in+T*2**0.5          # lines y+z=K
    big=prism_x([(y0,K_in-y0),(y0,135),(115,135),(115,K_in-115)],-30,30)
    strip=prism_x([(y0,z_in),(y0,z_top),(K_out-z_top,z_top),(YW,K_out-YW),(YW,K_in-YW)],-30,30)
    f=Face(Wire.make_polygon([Vector(x,y,100) for x,y in plan_hull()],close=True)); outline=extrude(f,30)
    return body-big+(strip&outline)
def lead_slot(): # fan lead exit below the fan bottom edge, both bottom corners
    return [(CX+sg*8.5,CX+sg*13.5) for sg in (1,-1)]
def build_main():
    c=load_cover(); ph=FAN/2+FCL/2+RIM_T; pz=PAD_Z
    c=c+box(CX-ph,CX+ph,YIN,YF,ZC-pz,ZC+pz)                     # close old slot field, wall flush with outer face
    c=c-box(CX-WX,CX+WX,100,YF+1,WZ0,WZ1)                       # vent window to the heatsink
    for sx in (1,-1):
        xa,xb=sorted((CX+sx*BOSS_X0,CX+sx*BOSS_X1))
        for sz in (1,-1):
            cx_,cz_=CX+sx*HX,ZC+sz*HZ
            c=c+box(xa,xb,YIN-BOSS_D,YIN+0.1,cz_-BOSS_HZ,cz_+BOSS_HZ)          # inner boss
            c=c-prism_y(hexagon(cx_,cz_,NUT_AF),YIN-BOSS_D-0.01,YF-NUT_SKIN)    # nut pocket (opens to the inside)
            c=c-Pos(cx_,YF-NUT_SKIN-0.5,cz_)*Rot(90,0,0)*Cylinder(SCR_HOLE/2,NUT_SKIN+1.5)   # screw hole through the skin
        xa,xb=sorted((CX+sx*8.5,CX+sx*13.5))
        c=c-box(xa,xb,100,YF+1,ZC-PAD_Z+3.0,ZC-FAN/2-1.0)        # wire pass-through into the cover
    return chamfer_front(c)
def build_plate():
    ph=FAN/2+FCL/2+RIM_T; ri=FAN/2+FCL/2
    p=box(CX-ph,CX+ph,YF,YF+PL_T,ZC-PAD_Z,ZC+PAD_Z)
    for sg in (1,-1):
        x0,x1=(CX+ri,CX+ph) if sg>0 else (CX-ph,CX-ri)
        p=p+box(x0,x1,YF+PL_T-0.01,YF+PL_T+RIM_H,ZC-ri,ZC+ri)
    p=p-box(CX-WX,CX+WX,YF-1,YF+PL_T+RIM_H+1,WZ0,WZ1)
    for sx in (1,-1):
        for sz in (1,-1):
            p=p-Pos(CX+sx*HX,YF+PL_T/2,ZC+sz*HZ)*Rot(90,0,0)*Cylinder(SCR_HOLE/2,PL_T+2)
        xa,xb=sorted((CX+sx*8.5,CX+sx*13.5))
        p=p-box(xa,xb,YF-1,YF+PL_T+1,ZC-PAD_Z-1,ZC-FAN/2-1.0)   # lead slot reaching the wall slot
    return p
if __name__=="__main__":
    m=build_main(); p=build_plate()
    for n,s in (('main',m),('plate',p)):
        bb=s.bounding_box(); print(n,'valid',s.is_valid,'solids',len(s.solids()),'vol %.0f'%s.volume,[round(v,1) for v in (bb.min.X,bb.min.Y,bb.min.Z,bb.max.X,bb.max.Y,bb.max.Z)])
    export_step(m,'out/cover_main_model.step'); export_step(p,'out/fan_plate_model.step')
