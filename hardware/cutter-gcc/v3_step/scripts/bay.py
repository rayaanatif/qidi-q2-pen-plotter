"""Cutter bay (GCC blade holder) - parametric B-rep. Run: python3 bay.py -> out/qs_cutter_bay_v3.step"""
import os,sys
from lib import *
WXL,WXR=-26.37,27.23; HR=104.5; TOP=113.5; H0=63.5
xl_in,xr_in=WXL-0.25,WXR+0.25; ARM=5.0
def build_bay():
    # --- bracket: footprint prism intersected with a 45 deg underside (epigraph of distance to the core rectangle)
    foot=[(-31.62,32.48,104.9,109.9),(xl_in-ARM,xl_in,80.0,104.9),(xr_in,xr_in+ARM,80.0,104.9)]
    fp=fuse(*[box(a,b,c,d,60.0,TOP) for a,b,c,d in foot])
    HH=TOP+1-H0; YB=140.0
    E=[box(CX-7,CX+7,104.9,YB,H0,TOP+1),
       prism_y([(CX+7,H0),(CX+7,TOP+1),(CX+7+HH,TOP+1)],104.9,YB),
       prism_y([(CX-7,H0),(CX-7,TOP+1),(CX-7-HH,TOP+1)],104.9,YB),
       prism_x([(104.9,H0),(104.9,TOP+1),(104.9-HH,TOP+1)],CX-7,CX+7)]
    for sx in (-1,1):
        E.append(Pos(CX+sx*7,104.9,H0)*Cone(0,HH,HH,align=(Align.CENTER,Align.CENTER,Align.MIN)))
    bracket=fp&fuse(*E)
    # --- spine plate
    body=bracket+box(CX-7,CX+7,104.9,109.9,19.0,TOP)
    # --- tube: 45 deg taper to the seat ring at the flange end
    tube=revolve_rz([(0,HB0),(RT,HB0),(RT,HT-(RT-SEAT_R)),(SEAT_R,HT),(0,HT)],CX,YT)
    body=body+tube
    # --- rear web tying tube and spine
    WEB=[(108.0,HB0),(113.0,HB0),(113.0,HT-10.0),(109.9,HT-6.9),(108.0,HT-6.9)]
    body=body+prism_x(WEB,CX-5.0,CX+5.0)
    # --- stiffening flanges + wings (module channel inner faces at CX +-6.8)
    FL=[(104.9,TOP),(112.5,TOP),(112.5,58.0),(110.6,56.1),(110.6,47.5),(104.9,47.5)]
    for (xa,xb) in ((CX+6.8,CX+10.4),(CX-10.4,CX-6.8)): body=body+prism_x(FL,xa,xb)
    WG=[(110.0,TOP),(120.0,TOP),(120.0,64.0),(110.0,54.0)]
    for (xa,xb) in ((CX+8.5,CX+10.8),(CX-10.8,CX-8.5)): body=body+prism_x(WG,xa,xb)
    # --- bore through the tube with a 0.6 x 45 deg lead-in chamfer at the nose end
    bore=revolve_rz([(0,HB0-1.0),(BORE_R+1.6,HB0-1.0),(BORE_R,HB0+0.6),(BORE_R,HT+1.0),(0,HT+1.0)],CX,YT)
    body=body-bore
    # --- dovetail grooves (female, widening into the arm; 45 deg flanks)
    for sign in (-1,1):
        wx=WXR if sign>0 else WXL
        pts=[(wx+sign*n, hh) for n,hh in ((-0.6,HR-2.02),(2.62,HR-5.24),(2.62,HR+5.24),(-0.6,HR+2.02))]
        body=body-prism_y(pts,79.0,102.0)
    # --- key pockets in the channel walls (open to the front)
    for sg in (-1,1):
        x0,x1=((CX-8.0,CX-6.6) if sg<0 else (CX+6.6,CX+8.0))
        body=body-box(x0,x1,110.3,114.0,POCK_H0,POCK_H1)
    return body
if __name__=="__main__":
    os.makedirs("out",exist_ok=True)
    b=build_bay(); info("bay",b); save(b,"out/qs_cutter_bay_v3.step")
