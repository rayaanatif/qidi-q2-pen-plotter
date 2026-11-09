import sys, math, json, struct
sys.path.insert(0,'.')
import numpy as np
from brep import *
from faces import *
from step_out import write_step
OUT="../tiles"
S=280.0; T=3.0
# outline (estimated from the Qidi 280x280 flex plate photo - edit and re-run if your plate differs)
RT_W=35.0; RT_H=12.0                 # rear tab: width, height, centred
FT_W0=118.0; FT_W1=98.0; FT_H=10.5   # front handle: width at plate edge, width at tip, height
MAG_D=5.1; MAG_H=2.1
SX=79.0; SY=140.0                     # seams: vertical x=SX, horizontal y=SY
CL=0.15                               # dovetail clearance
big=1000.0
def pieces():
    body=box(0,S,0,S,0,T)
    rt=box(S/2-RT_W/2,S/2+RT_W/2,S-0.01,S+RT_H,0,T)
    ft=prism([(S/2-FT_W0/2,0.01),(S/2+FT_W0/2,0.01),(S/2+FT_W1/2,-FT_H),(S/2-FT_W1/2,-FT_H)],'h',0,T)
    return [body,rt,ft]
def region(x0,x1,y0,y1): return box(x0,x1,y0,y1,-1,T+1)
def dove(cx,cy,d,c=0.0,pin=False):
    """dovetail, root on the seam at (cx,cy), pointing in direction d ('+x' or '+y'); c = clearance offset"""
    r,t,L=3.0+c,5.0+c,8.0+c
    if d=='+x': pts=[(cx-c,cy-r),(cx+L,cy-t),(cx+L,cy+t),(cx-c,cy+r)]
    else:       pts=[(cx+r,cy-c),(cx+t,cy+L),(cx-t,cy+L),(cx-r,cy-c)]
    return prism(pts,'h',0,T) if pin else prism(pts,'h',-0.5,T+0.5)
keys=[((SX,35),'+x'),((SX,105),'+x'),((SX,175),'+x'),((SX,245),'+x'),((47,SY),'+y'),((140,SY),'+y'),((230,SY),'+y')]
tiles={"LF":(0,SX,-20,SY),"LR":(0,SX,SY,S+20),"RF":(SX,S+1,-20,SY),"RR":(SX,S+1,SY,S+20)}
# pins protrude +x from left tiles into right tiles, +y from front tiles into rear tiles
pin_owner={ '+x':("LF","LR"), '+y':("LF","RF")}
def owner_pin(k):
    (cx,cy),d=k
    if d=='+x': return "LF" if cy<SY else "LR", "RF" if cy<SY else "RR"
    return ("LF","LR") if cx<SX else ("RF","RR")
def build(name):
    x0,x1,y0,y1=tiles[name]; R=region(x0,x1,y0,y1); sol=None
    for p in pieces():
        q=intersect(p,R)
        if q: sol=q if sol is None else union(sol,q)
    for k in keys:
        pin,sock=owner_pin(k)
        if name==pin: sol=union(sol,dove(k[0][0],k[0][1],k[1],0.0,True))
        if name==sock: sol=subtract(sol,dove(k[0][0],k[0][1],k[1],CL))
    # magnet pockets: 4 per tile, inset 25 from the tile's plate-body corners, never on a seam
    bx0,bx1=max(x0,0),min(x1,S);by0,by1=max(y0,0),min(y1,S)
    mags=[(x,y) for x in (bx0+25,bx1-25) for y in (by0+25,by1-25)]
    for x,y in mags:
        hs=[((math.cos(2*math.pi*k/32),math.sin(2*math.pi*k/32),0.0),MAG_D/2+math.cos(2*math.pi*k/32)*x+math.sin(2*math.pi*k/32)*y) for k in range(32)]+[((0,0,1),MAG_H),((0,0,-1),0.1)]
        sol=subtract(sol,convex(hs,(x,y,1)))
    return sol,mags
MH=0.4; STOP_H=1.2; LW=0.8; RR_=4.0; CR=6.5
MARKS=[(18,14),(S-14,14),(S-14,S-14),(18,S-14),(18,60),(18,110),(18,190),(70,S-14),(150,S-14),(S-14,60),(S-14,110),(S-14,190)]
def cyl(r,N,z0,z1,cx=0,cy=0):
    hs=[((math.cos(2*math.pi*k/N),math.sin(2*math.pi*k/N),0.0),r+(math.cos(2*math.pi*k/N)*cx+math.sin(2*math.pi*k/N)*cy)) for k in range(N)]
    hs+=[((0,0,1),z1),((0,0,-1),-z0)]
    return convex(hs,(cx,cy,(z0+z1)/2))
def black_for(name):
    x0,x1,y0,y1=tiles[name]; sol=None
    def add(m):
        nonlocal sol; sol=m if sol is None else union(sol,m)
    for (x,y) in MARKS:
        if x-CR>=x0+1 and x+CR<=x1-1 and y-CR>=y0+1 and y+CR<=y1-1 and (x1<S or x+CR<=S):   # ring wholly inside this tile
            ring=subtract(cyl(RR_+LW/2,48,T-0.02,T+MH,x,y),cyl(RR_-LW/2,48,T-0.1,T+MH+0.1,x,y))
            add(union(union(ring,box(x-CR,x+CR,y-LW/2,y+LW/2,T-0.02,T+MH)),box(x-LW/2,x+LW/2,y-CR,y+CR,T-0.02,T+MH)))
    if name=="LR":   # paper corner stop: A4 portrait, left edge x=40, rear edge y=S-30
        px,py=40.0,S-30
        add(union(box(px-4.5,px+30,py,py+4.5,T-0.02,T+STOP_H),box(px-4.5,px,py-40,py+4.5,T-0.02,T+STOP_H)))
    return sol
def stl(polys,fn):
    tris=[]
    for p in polys:
        v=[np.array(a) for a in p.v]
        for i in range(1,len(v)-1): tris.append((p.plane.n,v[0],v[i],v[i+1]))
    with open(fn,'wb') as f:
        f.write(b'qidi q2 plate tile'.ljust(80,b' ')); f.write(struct.pack('<I',len(tris)))
        for n,a,b,c in tris: f.write(struct.pack('<12fH',*n,*a,*b,*c,0))
allm={};blk={}
for nm in tiles:
    sol,m=build(nm);allm[nm]=m;b=black_for(nm);blk[nm]=len(MARKS) if False else None
    stl(sol,f"{OUT}/q2_plate280_tile_{nm}_base.stl")
    if b: stl(b,f"{OUT}/q2_plate280_tile_{nm}_black.stl")
    full=union(sol,b) if b else sol
    stl(full,f"{OUT}/q2_plate280_tile_{nm}_combined.stl")
    V,faces=merge_faces(full);faces=conform(V,faces);nb,vol=check(V,faces)
    bb=np.array([v for p in full for v in p.v]);print(nm,"bbox",bb.min(0).round(1),bb.max(0).round(1),"vol %.0f"%vol,"bad",nb,"black",bool(b))
    write_step(f"{OUT}/q2_plate280_tile_{nm}.step",V,faces,"q2_plate280_tile_"+nm)
json.dump(dict(plate=[S,S,T],rear_tab=[RT_W,RT_H],front_tab=[FT_W0,FT_W1,FT_H],seams=dict(x=SX,y=SY),magnets=allm,keys=[[list(k[0]),k[1]] for k in keys],marks=MARKS,paper_corner=[40,S-30],mark_height=MH,colour_change_z=T),open(f"{OUT}/q2_plate280_layout.json","w"))
