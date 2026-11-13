"""Tiny analytic mesh toolkit: convex hulls, slit tubes, polygon-ring prisms. Triangles array (n,3,3)."""
import numpy as np, struct
from scipy.spatial import ConvexHull
def vol(T): return np.einsum('ij,ij->i',T[:,0],np.cross(T[:,1],T[:,2])).sum()/6
def fix(T):
    return T if vol(T)>=0 else T[:,[0,2,1],:]
def hull(P):
    P=np.asarray(P,float); h=ConvexHull(P); c=P.mean(0); T=[]
    for s in h.simplices:
        a,b,cc=P[s]; n=np.cross(b-a,cc-a)
        if n@(a-c)<0: b,cc=cc,b
        T.append([a,b,cc])
    return np.array(T)
def prism(poly,h0,h1):
    """convex polygon (x,y) extruded h0..h1"""
    poly=np.asarray(poly,float); return hull([(x,y,h0) for x,y in poly]+[(x,y,h1) for x,y in poly])
def box(x0,x1,y0,y1,h0,h1): return prism([(x0,y0),(x1,y0),(x1,y1),(x0,y1)],h0,h1)
def tube(cx,cy,st,slit=0.6,N=120,slit_dir=90.0):
    """stations [(h,rin,rout)]; slit half-width `slit` (mm, planar faces) centred on direction slit_dir (deg, from +x toward +y); slit=0 -> closed ring"""
    T=[]
    def ang(r):
        d=np.degrees(np.arcsin(slit/r)) if slit>0 else 0
        return np.radians(slit_dir+d), np.radians(slit_dir+360-d)
    ths={}
    for key in ('in','out'): pass
    def ring(r,h):
        a0,a1=ang(r); th=np.linspace(a0,a1,N); return np.stack([cx+r*np.cos(th),cy+r*np.sin(th),np.full(N,h)],1)
    O=[ring(r,h) for h,ri,r in st]; I=[ring(ri,h) for h,ri,r in st]
    def strip(A,B):  # quads between two polylines A (lower) B (upper), along k
        for k in range(len(A)-1):
            T.append([A[k],A[k+1],B[k+1]]); T.append([A[k],B[k+1],B[k]])
    for j in range(len(st)-1):
        strip(O[j],O[j+1]); strip(I[j+1],I[j])
    # end caps (annulus strips)
    for j,flip in ((0,1),(len(st)-1,0)):
        for k in range(N-1):
            a,b,c,d=I[j][k],I[j][k+1],O[j][k+1],O[j][k]
            if flip: T.append([a,c,b]);T.append([a,d,c])
            else: T.append([a,b,c]);T.append([a,c,d])
    if slit>0:
        for end in (0,N-1):
            for j in range(len(st)-1):
                a,b,c,d=I[j][end],I[j+1][end],O[j+1][end],O[j][end]
                T.append([a,b,c]);T.append([a,c,d])
    return fix_comp(np.array(T))
def fix_comp(T): return fix(T)
def ray_poly(poly,ang):
    """distance from origin along angle to boundary of convex polygon containing origin"""
    d=np.array([np.cos(ang),np.sin(ang)]); best=None
    n=len(poly)
    for i in range(n):
        p,q=poly[i],poly[(i+1)%n]; e=q-p; M=np.array([[d[0],-e[0]],[d[1],-e[1]]])
        if abs(np.linalg.det(M))<1e-12: continue
        t,u=np.linalg.solve(M,p)
        if t>0 and -1e-9<=u<=1+1e-9: best=t if best is None else min(best,t)
    return best
def ringprism(outer,inner,ctr,axis,a0,a1):
    """outer, inner: convex polygons (2D, in plane coords) both containing ctr; extruded along `axis` ('x') from a0..a1.
    plane coords are (y,h) for axis x, (x,h) for axis y, (x,y) for axis z."""
    outer=np.asarray(outer,float)-ctr; inner=np.asarray(inner,float)-ctr
    angs=sorted(set([np.arctan2(p[1],p[0]) for p in outer]+[np.arctan2(p[1],p[0]) for p in inner]))
    angs=np.array(angs)
    Po=np.array([ray_poly(outer,t)*np.array([np.cos(t),np.sin(t)]) for t in angs])+ctr
    Pi=np.array([ray_poly(inner,t)*np.array([np.cos(t),np.sin(t)]) for t in angs])+ctr
    def lift(p,a):
        if axis=='x': return np.array([a,p[0],p[1]])
        if axis=='y': return np.array([p[0],a,p[1]])
        return np.array([p[0],p[1],a])
    T=[]; n=len(angs)
    for k in range(n):
        k2=(k+1)%n
        for a,flip in ((a0,1),(a1,0)):
            A,B,C,D=lift(Pi[k],a),lift(Pi[k2],a),lift(Po[k2],a),lift(Po[k],a)
            T+= ([[A,C,B],[A,D,C]] if flip else [[A,B,C],[A,C,D]])
        for P,rev in ((Po,0),(Pi,1)):
            A,B=lift(P[k],a0),lift(P[k2],a0); C,D=lift(P[k2],a1),lift(P[k],a1)
            T+= ([[A,B,C],[A,C,D]] if not rev else [[A,C,B],[A,D,C]])
    return fix(np.array(T))
def teardrop(cy,ch,r,n=24):
    pts=[(cy+r*np.cos(t),ch+r*np.sin(t)) for t in np.radians(np.linspace(135,405,n))]  # circle except top arc (45..135)
    pts.append((cy,ch+r*np.sqrt(2)))
    return np.array(pts)
def write(path,T,name=b"Q2 tool"):
    n=np.cross(T[:,1]-T[:,0],T[:,2]-T[:,0]); l=np.linalg.norm(n,axis=1,keepdims=True); l[l==0]=1; n/=l
    rec=np.zeros(len(T),dtype=np.dtype([("n","<f4",3),("v","<f4",(3,3)),("a","<u2")])); rec["n"]=n; rec["v"]=T
    with open(path,"wb") as f: f.write(name.ljust(80,b" ")); f.write(struct.pack("<I",len(T))); f.write(rec.tobytes())

def orient_mesh(T):
    """make triangle winding consistent (BFS over shared edges) and outward (positive volume)"""
    T=np.asarray(T,float).copy(); key=np.round(T,4).reshape(-1,3)
    _,inv=np.unique(key,axis=0,return_inverse=True); I=inv.reshape(-1,3).copy()
    from collections import defaultdict, deque
    ed=defaultdict(list)
    for t,(a,b,c) in enumerate(I):
        for u,v in ((a,b),(b,c),(c,a)): ed[frozenset((u,v))].append(t)
    seen=np.zeros(len(I),bool)
    for s in range(len(I)):
        if seen[s]: continue
        seen[s]=True; q=deque([s]); comp=[s]
        while q:
            t=q.popleft(); a,b,c=I[t]
            for u,v in ((a,b),(b,c),(c,a)):
                for n in ed[frozenset((u,v))]:
                    if n==t or seen[n]: continue
                    na,nb,nc=I[n]; dirs=[(na,nb),(nb,nc),(nc,na)]
                    if (u,v) in dirs:  # same direction -> flip neighbour
                        I[n]=[na,nc,nb]; T[n]=T[n][[0,2,1]]
                    seen[n]=True; q.append(n); comp.append(n)
        if vol(T[comp])<0: T[comp]=T[comp][:,[0,2,1],:]; I[comp]=I[comp][:,[0,2,1]]
    return T
