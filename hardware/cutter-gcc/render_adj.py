import sys; sys.argv=['x']
exec(open('fit_adj.py').read().split('print("frame vs bay')[0])
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
ix=int(round((CX-G0.x0)/ST)); H=holder(XEQ)
def sec(ax,F,col,idx=ix):
    m=(F[:,:,idx]>0.5).T.astype(float); m=np.ma.masked_where(m==0,m)
    ax.imshow(m,origin='lower',extent=[G0.y0,G0.y0+ST*(F.shape[0]-1),G0.h0,G0.h0+ST*(F.shape[1]-1)],cmap=ListedColormap([col]),aspect='equal',interpolation='nearest')
fig,ax=plt.subplots(1,3,figsize=(17,10),dpi=110,gridspec_kw={'width_ratios':[1.15,1,1]})
a=ax[0]
sec(a,Bf,'#8a8f98'); sec(a,frame,'#5b8c5a'); sec(a,put(Fp,op_),'#e08a1e'); sec(a,put(Fr,orr,-3.0),'#c0392b'); sec(a,key,'#8e44ad'); sec(a,H,'#2b6cb0')
a.set_xlim(104,132); a.set_ylim(-1,116); a.set_xlabel('y (mm)'); a.set_ylabel('h (mm)')
a.set_title('Section on the tool axis\ngrey bay | green frame | orange plunger (coil relaxed) | red rod+knob (turned 1 turn) | purple key | blue holder',fontsize=9)
# front view
def depth(F):
    occ=F>0.5; any_=occ.any(0); first=np.argmax(occ[::-1],0); yy=(F.shape[0]-1-first)*ST+G0.y0
    return np.where(any_,yy,np.nan)
ext=[G0.x0,G0.x0+ST*(Bf.shape[2]-1),G0.h0,G0.h0+ST*(Bf.shape[1]-1)]
b=ax[1]
for F,cm in ((Bf,'Greys'),(H,'Blues'),(frame,'Greens'),(put(Fp,op_),'Oranges'),(put(Fr,orr,-3.0),'Reds'),(key,'Purples')):
    d=depth(F)
    if np.all(np.isnan(d)): continue
    lo,hi=np.nanmin(d),np.nanmax(d); b.imshow(((d-lo)/(hi-lo+1e-6))*0.5+0.35,origin='lower',extent=ext,cmap=cm,vmin=0,vmax=1,aspect='equal',interpolation='nearest')
b.set_xlim(-18,19); b.set_ylim(-1,116); b.set_title('Front view',fontsize=10); b.set_xlabel('x (mm)')
c=ax[2]
# knob/rod detail section x=CX zoom
sec(c,frame,'#5b8c5a'); sec(c,put(Fp,op_),'#e08a1e'); sec(c,put(Fr,orr,-3.0),'#c0392b'); sec(c,key,'#8e44ad')
c.set_xlim(108,128); c.set_ylim(58,115); c.set_title('Detail: thread, nut, cap, tab slot with scale',fontsize=10); c.set_xlabel('y (mm)')
fig.tight_layout(); fig.savefig('cutter_adjust_assembly.png',bbox_inches='tight')
