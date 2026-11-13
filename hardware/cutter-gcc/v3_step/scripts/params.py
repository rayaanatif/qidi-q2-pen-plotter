"""Shared parameters for the GCC-holder cutter bay + pusher module (all mm, model frame: x, y, h; h = tool axis, nose end at low h)."""
CX=0.4
YT=118.2          # tube axis y (pen bay v5 was 115.2): +3.0 so the 15.75 flange clears the spine plate (y<=109.9)
# ---- holder (measured by user: B 11.55 barrel, C 12 ring, D 3 pin, E 8 pin above ring, F 15.75 flange, G 5 nose, A 30.2)
BARREL_D=11.55; RING_D=12.0; PIN_D=3.0; PIN_E=8.0; FLANGE_D=15.75; NOSE_D=5.0
FLANGE_T=2.0      # ASSUMED
BARREL_L=28.2     # ASSUMED: flange underside -> nose end (A 30.2 - flange 2.0)
RING_H=6.0        # ASSUMED ring height above the flange
PIN_TRAVEL=8.0
# ---- bay
HB0=1.0           # tube bottom (nose end sits flush here)
HT=HB0+BARREL_L   # flange underside rests here  (29.2)
BORE_R=BARREL_D/2+0.175   # 5.95
RT=9.2; SEAT_R=6.9
# ---- pin top (rest) above flange underside
PIN0=HT+FLANGE_T+RING_H+PIN_E      # 45.2
RING_TOP=HT+FLANGE_T+RING_H        # 37.2
# internal plunger spring (measured by user): 10 gf at touch, 165 gf at 8 mm
F0_GF=10.0; K_INT=(165.0-10.0)/8.0  # 19.4 gf/mm
