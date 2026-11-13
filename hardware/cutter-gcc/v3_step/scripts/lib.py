"""Parametric B-rep helpers (build123d / OpenCascade). Model frame: x, y, z=h (tool axis)."""
import math
from build123d import *
from params import *
from module_geom import *

def box(x0,x1,y0,y1,z0,z1):
    return Pos((x0+x1)/2,(y0+y1)/2,(z0+z1)/2)*Box(x1-x0,y1-y0,z1-z0)
def cyl(r,z0,z1,cx=CX,cy=YT):
    return Pos(cx,cy,z0)*Cylinder(r,z1-z0,align=(Align.CENTER,Align.CENTER,Align.MIN))
def revolve_rz(pts,cx=CX,cy=YT):
    """solid of revolution about the vertical axis through (cx,cy); pts = [(r,z),...] closed polygon"""
    f=(Plane.XZ*Polygon(*pts,align=None)).faces()[0]
    s=revolve(f,Axis.Z,360)
    return Pos(cx,cy,0)*s
def prism_x(pts_yz,x0,x1):
    """polygon in (y,z) extruded along x from x0 to x1"""
    f=(Plane.YZ*Polygon(*pts_yz,align=None)).faces()[0]
    s=extrude(f,x1-x0); bb=s.bounding_box()
    return Pos(x0-bb.min.X,0,0)*s
def prism_y(pts_xz,y0,y1):
    """polygon in (x,z) extruded along y from y0 to y1"""
    f=(Plane.XZ*Polygon(*pts_xz,align=None)).faces()[0]
    s=extrude(f,y1-y0); bb=s.bounding_box()
    return Pos(0,y0-bb.min.Y,0)*s
def helix_sweep(pts_rz,z0,turns,pitch,r_path,cx=CX,cy=YT,extra_deg=0.0):
    """sweep a closed (r,z-relative) profile along a right-hand helix starting at angle 0 / height z0"""
    path=Helix(pitch=pitch,height=turns*pitch,radius=r_path)
    f=(Plane.XZ*Polygon(*pts_rz,align=None)).faces()[0]
    s=sweep(f,path,is_frenet=True)
    return Pos(cx,cy,z0)*s
def fuse(*parts):
    r=parts[0]
    for p in parts[1:]: r=r+p
    return r
def info(name,p):
    sol=p.solids(); bb=p.bounding_box()
    print("%-28s valid=%s solids=%d vol=%.1f  bbox x[%.2f,%.2f] y[%.2f,%.2f] z[%.2f,%.2f]"%(name,p.is_valid,len(sol),p.volume,bb.min.X,bb.max.X,bb.min.Y,bb.max.Y,bb.min.Z,bb.max.Z))
def save(p,path):
    export_step(p,path)
