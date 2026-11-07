# Hardware

All files are in `stl/` (print-ready) and `step/` (for editing). Version 4.

![assembly](assembly_views.png)

| File | Print | Notes |
| --- | --- | --- |
| `qs_cover_v4_A_FRONT_DOWN_print.stl` | Cover, variant A | Front face down, no supports |
| `qs_cover_v4_B_FRONT_DOWN_print.stl` | Cover, variant B | Front face down, no supports |
| `qs_pen_bay_v4_print.stl` | Pen bay | Already flipped, flat crossbar on the bed |
| `qs_pen_cartridge_v4_bore7.0.stl` to `bore11.5.stl` | Pen cartridge | Print upright. One file per pen size, in 0.5 mm steps from 7.0 to 11.5 mm. Pick the bore about 0.1 to 0.2 mm bigger than your pen's barrel. All of them have the same outside, so they fit the same bay, clip and jig. Walls get thin above 10.5 mm, so print those slowly at 100% infill |
| `qs_pen_height_jig_v1_tip3.2/4.2/5.2.stl` | Pen height jig | Sets how far the pen tip sticks out below the cartridge collar, so you don't need `PEN_TOUCH` after every pen change. Pick the number that matches your tip height (4.2 mm is what I use) |
| `qs_bay_wedge_clip_v1_end7.7/7.9/8.1.stl` | Screwless clamp | A wedge clip that slides onto the bay's two clamp ears and squeezes them shut instead of the M2 screw. See below |
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

## Pen height jig

![jig](jig_section.png)

1. Put the jig on a flat table, ring side up.
2. With the bay screw loose, stand the bay and cartridge on the jig so the cartridge collar sits on the ring.
3. Drop the pen in from the top until the tip rests on the floor.
4. Tighten the M2x8 clamp screw. The tip now sticks out exactly the same amount every time.

The three files differ only in how far the tip sticks out below the collar: 3.2, 4.2 or 5.2 mm. Use the same one every time, and keep the `z_draw` you found with it.

## Screwless wedge clip

The 7.9 version has been tested on a real Q2 and holds the cartridge well. The 7.7 and 8.1 versions are untested spares for printers that run a little tight or loose.

The bay's clamp ears are 8.8 mm thick with the slit open and 8.0 mm with it closed. The clip is a U with a tapered inside: it is 9.1 mm wide at the mouth, narrowing to 7.7, 7.9 or 8.1 mm (the number in the file name) at the bridge.

1. Set the cartridge height with the jig and leave the M2 screw out.
2. Slide the clip onto the ears from the top, bridge end first, with the thumb tab facing out, and push it until it stops.
3. The taper squeezes the slit shut. The slope is shallow enough (about 6 degrees on each side) that friction keeps it locked.

Print it upright (the U standing on its mouth) in PETG or ABS, 100% infill, 4 perimeters. Try the 7.9 first. If it will not go on, use 8.1. If it goes on but is loose, use 7.7.

## Looser dovetail cover (shorter top)

The original cover A has a very snug dovetail: it slides on but is hard to remove. These STEP files thin the cover's dovetail rails and lower the roof by 1.8 mm. The pen bay is unchanged. The roof pin holes have a flat-tipped teardrop so the roof edge stays closed above them (0.6 mm wall).

- `qs_cover_v4_A_dovetail_looser_2.20_top-1.8_FRONT_DOWN_print.step`: slightly looser (rails about 0.1 mm thinner on each flank). Try this first.
- `qs_cover_v4_A_dovetail_looser_2.10_top-1.8_FRONT_DOWN_print.step`: looser again (about 0.2 mm).
- `_model_orientation` copies of both are in the same folder.

Printed front-down, nothing overhangs more than 45.3 degrees and there are no flat downward faces above the bed.

## Stiffer pen bay (v5)

The v4 bay flexes along the short length of spine between the bracket and the pen tube. v5 adds two side wings along that section, outside the pen and collar footprint, so it still slides on and off the same way. The dovetail grooves are the same as v4, so it fits the looser cover above.

- `qs_pen_bay_v5_stiff_flanges_print.stl`: side wings only. About 4 to 10 times stiffer against bending in the weak section.
- `qs_pen_bay_v5_stiff_flanges_comb_print.stl`: the same, plus three small tines that slide into the middle front vents of the cover to lock the bay sideways. Cut the tines off if they bind.
