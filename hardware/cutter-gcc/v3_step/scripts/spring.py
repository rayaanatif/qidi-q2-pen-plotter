"""Printed diamond-section helical coil + flat-topped land (true helical sweeps)."""
from lib import *
TIP=0.15
def at(solid,cx,cy,z,deg=0.0):
    return Pos(cx,cy,z)*(Rot(0,0,deg)*solid)
def coil(R,A,B,P,N,zs,cx=CX,cy=YT):
    """N-1 active turns, diamond section (half-width A radial, half-height B axial), centre line starts at height zs, angle 0"""
    d=TIP; t=B*d/A     # 0.15 mm flats on the radial tips (a razor-sharp tip does not print): 0.3 mm tall, 45 deg faces untouched
    return helix_sweep([(R-A+d,-t),(R,-B),(R+A-d,-t),(R+A-d,t),(R,B),(R-A+d,t)],zs,N-1,P,R,cx,cy)
def land(R,A,B,P,N,zs,AH,LIN,LOUT,cx=CX,cy=YT):
    """last turn thickened to a flat annulus top at AH; underside follows the coil's 45 deg diamond slope (printable without bridging)"""
    zc0=zs+(N-1)*P
    top=AH+1.0-zc0
    sl=lambda r:-B+abs(r-R)*B/A
    prof=[(LIN-0.5,sl(LIN-0.5)),(R,-B),(LOUT+0.5,sl(LOUT+0.5)),(LOUT+0.5,top),(LIN-0.5,top)]
    parts=[]
    for q in range(4):
        piece=helix_sweep(prof,0,0.25,P,R,0,0)           # quarter turn about the origin
        parts.append(Pos(cx,cy,zc0+q*P/4)*(Rot(0,0,90*q)*piece))
    wedge=fuse(*parts)
    ring=cyl(LOUT,zc0-B-1.0,AH,cx,cy)-cyl(LIN,zc0-B-2.0,AH+1.0,cx,cy)
    return wedge&ring
