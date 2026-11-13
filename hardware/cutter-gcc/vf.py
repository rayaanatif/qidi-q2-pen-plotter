import numpy as np
ST=0.2
class Grid:
    def __init__(s,x0,x1,y0,y1,h0,h1,F=None):
        s.x0,s.y0,s.h0=x0,y0,h0
        s.nx=int(round((x1-x0)/ST))+1; s.ny=int(round((y1-y0)/ST))+1; s.nh=int(round((h1-h0)/ST))+1
        s.F=np.zeros((s.ny,s.nh,s.nx),np.float32) if F is None else F
    def win(s,bx,by,bh,m=1.0):
        i=lambda v,o,n:(max(0,int(np.floor((v[0]-m-o)/ST))),min(n,int(np.ceil((v[1]+m-o)/ST))+1))
        ix=i(bx,s.x0,s.nx); iy=i(by,s.y0,s.ny); ih=i(bh,s.h0,s.nh)
        X=(s.x0+ST*np.arange(*ix))[None,None,:]; Y=(s.y0+ST*np.arange(*iy))[:,None,None]; H=(s.h0+ST*np.arange(*ih))[None,:,None]
        return (slice(*iy),slice(*ih),slice(*ix)),X,Y,H
    def op(s,mode,bx,by,bh,sdf):
        sl,X,Y,H=s.win(bx,by,bh); occ=np.clip(0.5-sdf(X,Y,H)/ST,0,1).astype(np.float32)
        if mode=='add': s.F[sl]=np.maximum(s.F[sl],occ)
        else: s.F[sl]=np.minimum(s.F[sl],1-occ)
# signed distance helpers (negative inside); combine: union=min, intersect=max, subtract a-b = max(a,-b)
def sd_box(x0,x1,y0,y1,h0,h1):
    def f(X,Y,H):
        cx,cy,ch=(x0+x1)/2,(y0+y1)/2,(h0+h1)/2; ex,ey,eh=(x1-x0)/2,(y1-y0)/2,(h1-h0)/2
        dx=np.abs(X-cx)-ex; dy=np.abs(Y-cy)-ey; dh=np.abs(H-ch)-eh
        out=np.sqrt(np.maximum(dx,0)**2+np.maximum(dy,0)**2+np.maximum(dh,0)**2)
        return out+np.minimum(np.maximum(np.maximum(dx,dy),dh),0)
    return f
def sd_poly_prism(poly,axis_range,axis):
    """convex polygon (list of (u,v)) extruded along `axis` ('x','h','y') between axis_range; polygon coords: x-axis->(y,h), h-axis->(x,y), y-axis->(x,h)"""
    P=np.array(poly,float); n=len(P)
    # ensure ccw
    a=0.5*np.sum(P[:,0]*np.roll(P[:,1],-1)-np.roll(P[:,0],-1)*P[:,1]); 
    if a<0: P=P[::-1]
    def f(X,Y,H):
        U,V,W={'x':(Y,H,X),'h':(X,Y,H),'y':(X,H,Y)}[axis]
        d=None
        for k in range(n):
            p,q=P[k],P[(k+1)%n]; e=q-p; L=np.hypot(*e); nn=np.array([e[1],-e[0]])/L   # outward normal for ccw
            dk=(U-p[0])*nn[0]+(V-p[1])*nn[1]
            d=dk if d is None else np.maximum(d,dk)
        z0,z1=axis_range; dw=np.abs(W-(z0+z1)/2)-(z1-z0)/2
        return np.maximum(d,dw)
    return f
def sd_cyl_h(cx,cy,r,h0,h1):
    def f(X,Y,H):
        d=np.hypot(X-cx,Y-cy)-r; dw=np.abs(H-(h0+h1)/2)-(h1-h0)/2
        return np.maximum(d,dw)
    return f
def sd_teardrop_h(cx,cy,r,h0,h1,up=-1.0):
    """hole axis along h; apex towards model -y (up=-1) at 45deg"""
    s2=np.sqrt(2)
    def f(X,Y,H):
        dx=X-cx; dy=(Y-cy)*up   # dy positive toward apex (up=-1: toward -y)
        circ=np.hypot(dx,Y-cy)-r
        # wedge: |dx|+dy <= r*sqrt2 and dy>=0 ; distance approx
        wedge=np.maximum((np.abs(dx)+dy-r*s2)/s2, r/s2-dy)
        d=np.minimum(circ,wedge)
        dw=np.abs(H-(h0+h1)/2)-(h1-h0)/2
        return np.maximum(d,dw)
    return f

def sd_teardrop_x(cy,ch,r,x0,x1):
    """hole axis along x, apex toward +h"""
    s2=np.sqrt(2)
    def f(X,Y,H):
        dx=Y-cy; dy=H-ch
        circ=np.hypot(dx,dy)-r
        wedge=np.maximum((np.abs(dx)+dy-r*s2)/s2, r/s2-dy)
        dw=np.abs(X-(x0+x1)/2)-(x1-x0)/2
        return np.maximum(np.minimum(circ,wedge),dw)
    return f
def mesh(G):
    from skimage import measure
    Fp=np.pad(G.F,1)
    v,f,_,_=measure.marching_cubes(Fp,0.5,spacing=(ST,ST,ST))
    v=v-ST+np.array([G.y0,G.h0,G.x0])
    V=np.stack([v[:,2],v[:,0],v[:,1]],1); f=f[:,[0,2,1]]
    T=V[f]; vol=np.einsum('ij,ij->i',T[:,0],np.cross(T[:,1],T[:,2])).sum()/6
    if vol<0: T=T[:,[0,2,1],:]; vol=-vol
    return T,vol

def sd_poly2(U,V,poly):
    """signed distance-ish (negative inside) to a convex polygon in (U,V); orientation-safe"""
    P=np.array(poly,float)
    if 0.5*np.sum(P[:,0]*np.roll(P[:,1],-1)-np.roll(P[:,0],-1)*P[:,1])<0: P=P[::-1]
    d=None
    for k in range(len(P)):
        p,q=P[k],P[(k+1)%len(P)]; e=q-p; L=np.hypot(*e); nn=np.array([e[1],-e[0]])/L
        dk=(U-p[0])*nn[0]+(V-p[1])*nn[1]; d=dk if d is None else np.maximum(d,dk)
    return d
