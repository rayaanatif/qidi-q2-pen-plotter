# Floating cutter cartridge (v1, not printed yet)

A single printed part: sleeve + printed coil spring + skirt. No screws, springs or clips. It gives the blade a soft, adaptive down-force instead of a rigid height.

## How it works

- The **sleeve** (outside 12.5 mm) slides in the pen bay tube, which acts as the rail. The GCC holder goes in from below until its flange stops on the collar, and the closed top (cap) presses the holder's top pin, which sets the blade exposure.
- The **skirt** slides over the bottom 12 mm of the bay tube (3 small crush ribs hold it by friction) and is the fixed end of the spring.
- The **coil** (diamond section, so it prints without supports) joins the skirt to the sleeve collar. Pushing the blade up compresses the coil, and the coil pushes back.
- The bay's clamp screw or wedge clip is **not used**. Leave the bay loose so the sleeve can slide.

## Files

| File | Notes |
| --- | --- |
| `qs_cutter_float_v1_3turn_bore11.3.stl` | Stiffer. Estimated about 44 gf/mm, about 3.5 mm travel |
| `qs_cutter_float_v1_4turn_bore11.3.stl` | Softer. Estimated about 29 gf/mm, about 5 mm travel |
| `cutter_float.py` | Parametric source (needs numpy, scipy, scikit-image). `python3 cutter_float.py TURNS Z0C BORE` |

Estimates come from a beam formula for printed PETG and are +/- 40%. Measure the real rate on a scale and use that.

## Things to set before printing

- **Z0C** (default 44): distance from the sleeve's bottom face (where the holder's flange stops) to the top of the holder's pin, with the pin pressed to the blade exposure you want. This is a placeholder. Measure it on your holder.
- **BORE** (default 11.3): sleeve bore. The slit lets it grip the 11.5 mm holder. Print 11.2 to 11.5 to tune the grip.

## Known trade-offs

- The tool hangs about 22 mm (3 turns) or 27 mm (4 turns) lower than a pen cartridge. Home and mesh with it removed, and check clearance at the park spot and near the purge bin.
- Guide length in the bay is about 24 mm, so expect some play at the tip. Print the sleeve at 12.6 mm outside if it is too loose.
- Print in PETG, upright as modelled, 0.12 to 0.16 mm layers, no supports, 100% infill. Printed coils creep, so recheck the touch height now and then.
