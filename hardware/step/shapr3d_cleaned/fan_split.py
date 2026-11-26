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

# ---------------- user mods (feet / side plates / extra wall / roof holes) ----------------
FOOT_DROP=1.2           # magnet pockets + lug bottoms move this far toward the cover bottom (-z)
FAR_EXT=12.0            # -x plate (far plate in the slicer view) gets this much longer toward the feet
GAP=13.0; WALL_L=22.5; WALL_H=28.0   # +x side: gap below the plate end, then a new wall 22.5 long x 28 tall
ROOF_HOLE_D_OLD,ROOF_HOLE_D_NEW=4.30,4.15
def _loops(z):
    import trimesh
    plan_hull()                                   # makes sure /tmp/_lc.stl exists
    sec=trimesh.load('/tmp/_lc.stl').section(plane_origin=[0,0,z],plane_normal=[0,0,1])
    return [sec.vertices[e.points][:,:2] for e in sec.entities]
def _poly_solid(pts,z0,z1):
    pts=[(float(x),float(y)) for x,y in pts]
    area=sum(pts[i][0]*pts[(i+1)%len(pts)][1]-pts[(i+1)%len(pts)][0]*pts[i][1] for i in range(len(pts)))
    if area<0: pts=pts[::-1]                      # make it counter-clockwise so extrude() goes +z
    f=Face(Wire.make_polygon([Vector(x,y,z0) for x,y in pts],close=True)); return extrude(f,z1-z0)
def _dedupe(p,min_d=0.12):
    """drop near-duplicate vertices (mesh tessellation) so the OCC booleans stay robust"""
    q=[tuple(map(float,p[0]))]
    for a in p[1:]:
        if ((a[0]-q[-1][0])**2+(a[1]-q[-1][1])**2)**0.5>=min_d: q.append((float(a[0]),float(a[1])))
    while len(q)>3 and ((q[0][0]-q[-1][0])**2+(q[0][1]-q[-1][1])**2)**0.5<min_d: q.pop()
    return q
def user_mods(c):
    import numpy as np
    outline=_poly_solid(plan_hull(),0,200)
    # 1) magnet pockets 1.2 mm lower: extend lugs down, move the teardrop pockets down, fill the old top of the pocket
    Z_BOT,Z_TOP=16.05,18.25
    for p in _loops(17.0):
        w=p[:,0].max()-p[:,0].min(); h=p[:,1].max()-p[:,1].min(); cx=p[:,0].mean()
        if abs(cx)<8 or abs(cx)>25: continue
        if w>8:   # lug outline -> extension below the lug
            c=c+_poly_solid(_dedupe(p),Z_BOT-FOOT_DROP,Z_BOT+0.05)
    import math
    def teardrop(cx,cy,r,n=60):                 # 45 deg teardrop, tip toward -y (print: tip points up)
        pts=[(cx,cy-r*2**0.5)]
        for i in range(n+1):
            a=math.radians(-45+270*i/n); pts.append((cx+r*math.cos(a),cy+r*math.sin(a)))
        return pts
    for cx in (-17.0,17.0):                      # magnet pockets: circle r=2.55 at y=97.30, tip at y=93.69 (as in the original)
        q=teardrop(cx,97.30,2.55)
        c=c+_poly_solid(q,Z_TOP-FOOT_DROP,Z_TOP+0.4)       # fill the old upper part of the pocket
        c=c-_poly_solid(q,Z_BOT-FOOT_DROP-0.5,Z_TOP-FOOT_DROP)  # pocket in its new, lower position
    # 2) far (-x) plate: 12 mm longer toward the feet; near (+x) plate: 13 mm gap, then a new wall 22.5 x 28
    X0,X1=-26.37,-24.58
    c=c+box(X0,X1,64.5,100.4,66.0-FAR_EXT,66.05)
    zt=63.0-GAP; zb=zt-WALL_L
    c=c+box(25.44,27.23,102.8-WALL_H,100.4,zb,zt)
    # 3) roof holes 4.30 -> 4.15 (keep the teardrop shape, scale about the circle centre)
    for p in _loops(121.8):
        w=p[:,0].max()-p[:,0].min(); h=p[:,1].max()-p[:,1].min()
        if 3<w<6 and 3<h<6:
            q=_dedupe(p,0.2); P=np.array(q)
            xc=(P[:,0].max()+P[:,0].min())/2
            # circle centre: fit on the points away from the teardrop tip
            far=P[np.abs(P[:,0]-xc)>0.8]
            A=np.c_[2*far[:,0],2*far[:,1],np.ones(len(far))]; b=(far**2).sum(1)
            sol=np.linalg.lstsq(A,b,rcond=None)[0]; yc=sol[1]; xc=sol[0]
            k=ROOF_HOLE_D_NEW/ROOF_HOLE_D_OLD
            sc=lambda f:[(xc+(x-xc)*f,yc+(y-yc)*f) for x,y in q]
            ring=_poly_solid(sc(1.10),120.9,122.7)-_poly_solid(sc(k),120.0,123.5)   # outer part overlaps the roof, inner = new smaller hole
            c=c+ring
    return c
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
    c=chamfer_front(c)
    return user_mods(c)
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
