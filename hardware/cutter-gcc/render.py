import sys; sys.argv=['x']
exec(open('fitcheck.py').read().split('print("holder vs bay')[0])
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
v='std'; g=geom(v)
P=place(v); Hh=holder(XEQ)
ix=int(round((CX-G0.x0)/ST))
def sec(ax,F,ix,col,alpha=1):
    m=(F[:,:,ix]>0.5).T.astype(float); m=np.ma.masked_where(m==0,m)
    ax.imshow(m,origin='lower',extent=[G0.y0,G0.y0+ST*(F.shape[0]-1),G0.h0,G0.h0+ST*(F.shape[1]-1)],cmap=ListedColormap([col]),alpha=alpha,aspect='equal',interpolation='nearest')
fig,ax=plt.subplots(1,2,figsize=(15,9),dpi=110,gridspec_kw={'width_ratios':[1.1,1]})
a=ax[0]
sec(a,Bf,ix,'#8a8f98'); sec(a,P,ix,'#e08a1e'); sec(a,Hh,ix,'#2b6cb0')
a.set_xlim(104,132); a.set_ylim(-1,112); a.set_xlabel('y (mm)  - spine at left, front at right'); a.set_ylabel('h (mm)  - nose end at bottom')
a.set_title('Section through the tool axis (x=%.1f)\ngrey: cutter bay   blue: GCC holder (pin pressed %.0f mm)   orange: pusher module, coil drawn relaxed'%(CX,XEQ),fontsize=10)
a.axhline(HT,color='k',lw=0.5,ls=':'); a.text(131.8,HT+0.6,'flange seat h=%.1f'%HT,ha='right',fontsize=8)
a.axhline(g['AH'],color='k',lw=0.5,ls=':'); a.text(131.8,g['AH']+0.6,'arm underside h=%.1f'%g['AH'],ha='right',fontsize=8)
a.text(131.8,PIN0-XEQ+0.6,'pin top at pressed pos. h=%.1f'%(PIN0-XEQ),ha='right',fontsize=8,color='#2b6cb0')
b=ax[1]
# front-to-back projection (looking from +y): nearest solid y for depth shade
def depth(F,y0=G0.y0):
    occ=F>0.5; any_=occ.any(0); first=np.argmax(occ[::-1],0); yy=(F.shape[0]-1-first)*ST+y0
    return np.where(any_,yy,np.nan)
ext=[G0.x0,G0.x0+ST*(Bf.shape[2]-1),G0.h0,G0.h0+ST*(Bf.shape[1]-1)]
for F,cm in ((Bf,'Greys'),(Hh,'Blues'),(P,'Oranges')):
    d=depth(F); 
    if np.all(np.isnan(d)): continue
    lo,hi=np.nanmin(d),np.nanmax(d); b.imshow(((d-lo)/(hi-lo+1e-6))*0.5+0.35,origin='lower',extent=ext,cmap=cm,vmin=0,vmax=1,aspect='equal',interpolation='nearest')
b.set_xlim(-18,19); b.set_ylim(-1,112); b.set_title('Front view (from +y): bay, holder, pusher module',fontsize=10); b.set_xlabel('x (mm)')
fig.tight_layout(); fig.savefig('cutter_assembly.png',bbox_inches='tight')
# detail: module alone + dims
