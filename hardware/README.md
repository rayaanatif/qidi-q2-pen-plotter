# Hardware

All files are in `stl/` (print-ready) and `step/` (for editing). Version 4.

![assembly](assembly_views.png)

| File | Print | Notes |
| --- | --- | --- |
| `qs_cover_v4_A_FRONT_DOWN_print.stl` | Cover, variant A | Front face down, no supports |
| `qs_cover_v4_B_FRONT_DOWN_print.stl` | Cover, variant B | Front face down, no supports |
| `qs_pen_bay_v4_print.stl` | Pen bay | Already flipped, flat crossbar on the bed |
| `qs_pen_cartridge_v4_bore9.0.stl` | Pen cartridge | Print upright. Pick the bore that fits your pen: 9.0, 9.5 or 10.0 |
| `qs_pen_cartridge_v4_bore9.5.stl` | | |
| `qs_pen_cartridge_v4_bore10.0.stl` | | |
| `qs_cutter_sleeve_v1_bore10.5/11.0/11.5.stl` | Cutter sleeve | Experimental, see [../docs/CUTTER.md](../docs/CUTTER.md) |

Print one cover, variant A or B (TODO: describe the difference between them).

STEP files: the cover, in print orientation and in model orientation.

## You will also need

- M2x8 screw, one (bay clamp). M2x6, M2x8 and M2x20 are the only sizes I used.
- 4 magnets, 5 x 2 mm.
- CA glue.

## Assembly

1. Fit the cover on the toolhead. For the magnets: stick each 5 x 2 mm magnet onto the duct-wing magnet (right polarity), lower the cover over them, then drip CA glue into the slot.
2. Slide the bay onto the two side rails from the **front**, toward the back, until the crossbar touches the cover face. The fit is tapered, so it is snug at the end.
3. Drop the cartridge with the pen in from the top and nip the M2x8 clamp screw.

The bay bore is 12.8 mm and the cartridge outside diameter is 12.6 mm, with a slit so the clamp screw can squeeze it onto the pen.
