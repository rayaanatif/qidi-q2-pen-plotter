# Spring-free GCC cutter (v2: blade tip level with the pen tip)

No printed coil. Cutting force = the blade holder's own spring + the toolhead's Z force. A rigid cap sits on the holder's pin and is locked onto a dovetail rib on the bay's spine with M2 screws.

## What changed in v2
- The holder seat is **7.05 mm lower**. The blade tip now sits level with the pen tip, so the **pen `z_draw` works for the blade** and you don't need `PEN_TOUCH` when swapping.
- Pilot holes are **M2 self-tap, 1.8 mm**. The lower hole is 4 mm lower than before. Cap slots are 2.6 mm wide.
- Tube bore opened to 12.2 mm (was 11.9) with a nose-end relief, so the barrel passes after printing shrink. The rail plate now runs the full length of the tube so it cannot flex.

## Print list (STEP, `hardware/step/shapr3d_cleaned/`; `_print` files are already in print orientation, do not rotate)
| File | Qty | Notes |
|---|---|---|
| `user_cover_with_blockstop_print.step` | 1 | Your cover (unchanged). |
| `user_cutter_bay_spring_free_print.step` | 1 | Cutter bay, holder seat lowered. |
| `qs_cutter_spring_free_cap_print.step` | 1 | Disc down, no supports. 100% infill or 4+ walls. |
| `qs_cutter_height_gauge_v1_tip8.2.step` | 1 | Optional gauge for setting blade exposure so the tip matches the pen. |

Hardware: 2x M2x8 pan-head self-tapping screws, GCC blade holder.

## Assembly
1. Drop the holder into the bay tube from the top, flange on the seat. The nose now hangs about 7 mm out of the bottom of the tube. That is intended.
2. Hold the cap above the bay, dovetail groove facing the spine, and slide it straight DOWN over the rib until the disc sits on the pin. Push until the pin is pushed in the amount you want (force about 10 + 19.4 x gf for x mm; 4 mm is about 88 gf; 7.5 mm limit).
3. Fit the two M2x8 screws through the slots into the rib. Snug them. To change force, loosen, slide the cap (+-3.5 mm), retighten.

## Matching the pen z_draw (no PEN_TOUCH)
The pen tip is 7.2 mm below the pen bay's tube end (pen jig 4.2 mm + 3.0 mm collar). The cutter tube end is 1.0 mm higher than the pen's, so the blade tip must be 8.2 mm below the cutter tube end.
1. Put the holder and cap in the bay. Stand the bay tube-end-down on the gauge (tube end flat on the ring, nose in the hole).
2. Turn the holder's exposure cap until the blade tip just touches the gauge floor. Do not push the blade in; stop at first contact.
3. Fit the bay on the machine and use your existing pen `z_draw`. Make cutting Z = `z_draw` minus the thickness of the material, plus or minus the small test-cut trim.

If you use a different pen jig (3.2 or 5.2), the target changes to 7.2 or 9.2 mm below the cutter tube end.

Check: because the holder's height is set by its flange, only the exposure cap changes the blade tip. Use the same exposure every time.
