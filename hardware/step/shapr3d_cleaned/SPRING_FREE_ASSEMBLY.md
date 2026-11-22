# Spring-free GCC cutter: assembly

No printed coil. The cutting force is the blade holder's own spring plus the toolhead's Z force. A rigid cap sits on the holder's pin, and the cap is locked onto a dovetail rib on the bay's spine with two screws.

## Print list (STEP, in `hardware/step/shapr3d_cleaned/`)
| File | Qty | Notes |
|---|---|---|
| `user_cover_with_blockstop_print.step` | 1 | Your cover. Block stop now on the other half. |
| `user_cutter_bay_spring_free_print.step` | 1 | Your rails and comb, normal barrel, dovetail rib + 2 pilot holes on the spine. |
| `qs_cutter_spring_free_cap_print.step` | 1 | Disc down, no supports (all slopes 45 deg). |

Hardware: 2x M3x8 pan-head self-tapping screws (M3x8 machine screws also work if you tap the 2.6 holes). GCC blade holder.

## Assembly
1. Drop the blade holder into the bay tube from the top, flange on the seat ring (nose at the bottom, flush with the tube end).
2. Hold the cap above the bay with the dovetail groove facing the spine. Slide it straight DOWN over the rib. The disc lands on the holder's pin.
3. Push the cap down until the pin is pushed in the amount you want:
   - 0.5 mm: about 20 gf
   - 4 mm: about 88 gf (starting point)
   - 7.5 mm: about 155 gf (limit; the disc touches the holder ring just past this)
   Force is about 10 + 19.4 x gf for x mm of pin travel (holder spring: 10 gf at touch, 165 gf at 8 mm).
4. Fit the two M3x8 screws through the slots into the rib holes (heights 68 and 80). Snug them. The cap cannot slide up (screws) and cannot pull off sideways (dovetail).
5. To change force: loosen the screws, slide the cap up or down (slots give +-3.5 mm), retighten.

To remove: undo the screws, lift the cap straight up, lift the holder out.
