# Cutter (work in progress)

Nothing here has been cut yet. The sleeve is designed, not printed, and the app only has a settings scaffold.

## Approach

- A **swivel drag-knife holder** with standard Roland-type blades. It is free-turning on bearings, so it trails behind its pivot and lines itself up with the cutting direction. The printer has no rotary axis and does not need one.
- Blades: 2 mm shaft, about 24 mm long including the cap, available in 30, 45 and 60 degrees. 45 is the all-rounder for vinyl, paper and light card, 60 suits thicker card, 30 suits fine detail.
- The holder body goes in from underneath until its flange stops against the sleeve's bottom face, which gives a repeatable blade height. The bay screw squeezes the sleeve onto the holder.
- Rigid, no spring. The page mesh (`PLOT_MESH`) follows the surface and cut depth is set by Z, the same way as `z_draw`.
- Cut on a sticky cutting mat, never straight onto the PEI plate.

## Parts

| File | Notes |
| --- | --- |
| `hardware/stl/qs_cutter_sleeve_v1_bore10.5.stl` | Sleeve, outside the same as the pen cartridges |
| `hardware/stl/qs_cutter_sleeve_v1_bore11.0.stl` | |
| `hardware/stl/qs_cutter_sleeve_v1_bore11.5.stl` | Thin wall (about 0.55 mm), print slowly at 100% infill |

Measure the **plain body** of your holder (not the flange or the knob) and pick the sleeve about 0.2 to 0.3 mm bigger. If the body is 12 mm or more a sleeve will not fit and the holder can be clamped directly in the 12.8 mm bay.

## To do

- Print and fit the sleeve, measure the blade offset from the nozzle.
- Find the cut depth with a test cut on scrap.
- Generate cutting G-code: blade-trail compensation, swivel arcs or lifts at corners, overcut on closed shapes, inner shapes first.
- Deboss stylus on the same body.
