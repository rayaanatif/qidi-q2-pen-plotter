# GCC blade holder: cutter bay + adjustable pusher (v2, untested)

Nothing here has been printed or cut yet. It was checked only by a voxel fit test against the holder dimensions you measured.

![assembly](cutter_adjust_assembly.png)

## How it works

A GCC-style holder hangs by its flange and a spring presses its top pin. The pin force minus the holder's own internal spring is the cutting force, and the blade backs off if the surface rises. A **thumbwheel** compresses the printed coil further, so you dial the force by hand. The holder's 165 gf at full travel does not add to the force, it opposes the coil.

## Parts (print list)

| File | Qty | Notes |
| --- | --- | --- |
| `qs_cutter_bay_v2.stl` | 1 | Same bracket, spine, dovetails, flanges and wings as pen bay v5, print bracket down, no supports. Tube axis is 3.0 mm further forward (y 118.2, was 115.2). Two key pockets in the flange walls. |
| `qs_cutter_adj_frame_v2.stl` | 1 | Tongue, guide tube and a printed nut. Print with the tube bottom on the bed, no supports. |
| `qs_cutter_adj_plunger_v2.stl` | 1 | Pusher disc, coil, cap and a tab that shows the setting. Print disc down, no supports. |
| `qs_cutter_adj_rod_knob_v2.stl` | 1 | Threaded rod and thumb knob. Print with the knob on the bed. |
| `qs_cutter_key_v2.stl` | 1 | Slides in from the front through the flange pockets and holds the frame down. |
| `qs_cutter_pusher_v2_soft/std/firm/hard.stl` | optional | Fixed-force modules with no thumbwheel (coil 24, 33, 58, 103 gf/mm). They use the same bay and key. |

Thread: 3 mm pitch, right hand, 0.3 mm radial clearance. Print the rod and frame with 0.2 mm layers, 100% infill for the rod.

## Assembly order

1. Drop the holder into the bay tube (flange on the seat ring).
2. Drop the plunger into the frame from below and the frame onto the bay's channel, so the disc lands on the pin. Press the frame down until the key pockets show at the top.
3. Slide the key in from the front through both flange pockets, above the frame.
4. Screw the rod in from the top, last. Turn **clockwise** to raise the force. The tab and ticks on the front of the tube show the setting.

To remove it, unscrew the rod, pull the key, lift the frame and plunger out. The rod has to come out first because the key slides past it.

## Force setting (coil about 32 gf/mm, estimated, plus or minus 40%)

Cut force in gf at pin depression x (blade out is about 0.875 x), for rod travel from the zero mark:

| Rod travel | Turns | x = 5 | x = 4.6 (about 4 mm blade) | x = 4 | x = 3 |
| --- | --- | --- | --- | --- | --- |
| 0 mm | 0 | 51 | 72 | 102 | 153 |
| 3 mm | 1 | 146 | 167 | 197 | 248 |
| 6 mm | 2 | 241 | 262 | 292 | 344 |
| 7 mm (max) | 2.3 | 273 | 294 | 324 | 375 |

One turn adds about 95 gf. Do not combine the maximum travel with x below about 3.4 mm, because the coil goes solid.

Without the coil rate known better, **calibrate with your scale**: record the force at several knob settings and use that table in the app.

## Assumptions (check these)

- Flange 2.0 mm thick.
- Barrel 28.2 mm from the flange underside to the nose end (A 30.2 minus the flange).
- Ring 6.0 mm tall above the flange, pin 8 mm above the ring.
- Internal spring 10 gf at touch and 165 gf at 8 mm (your measurement, treated as linear).
- Printed PETG shear modulus about 500 MPa.
- Nothing above the bay's top face (h 113.5): the knob reaches 113.4.

Change `params.py` and rerun `python3 cutter_bay.py; python3 cutter_adjust.py; python3 fit_adj.py` if any dimension is off.

## Consequences

- The tool axis moves 3.0 mm in model y compared with the pen bay, so the cutter needs its own XY offset.
- The blade is always exposed (about 5 mm free-hanging). Lift Z before travelling near the purge bin, and run homing and bed mesh with the cutter off.
- The nose is flush with the bottom of the tube, so Z touch needs its own calibration.
- The earlier notch-and-finger retention in v1 could not hold the coil's push, so it was replaced by the key.
