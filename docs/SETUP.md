# Setup

Do this once. Every plot after that is the short loop at the bottom.

## 1. Mount

1. Print the parts in [../hardware](../hardware/README.md).
2. Fit the cover on the toolhead.
3. Slide the pen bay onto the two side rails from the front, moving toward the back, until the crossbar touches the cover face. The fit is tapered, so it is snug at the end.

## 2. Fit the pen

1. Home **with no cartridge fitted.** The pen sticks out below the nozzle.
2. Drop the cartridge with the pen in from the top.
3. Set the pen height with the pen height jig (see [hardware](../hardware/README.md)), so the tip always sticks out the same amount below the cartridge collar. Without the jig, set the tip about 5 mm below the nozzle tip, measured from the nozzle, not from the holder.
4. Nip the M2x8 clamp screw.

## 3. Install `plotter.cfg`

1. Copy [`printer/plotter.cfg`](../printer/plotter.cfg) next to `printer.cfg` on the printer. From the folder that holds the file:

   ```
   scp plotter.cfg qidi@<printer-ip>:~/printer_data/config/
   ```

   If that folder does not exist, try `~/klipper_config/`. You can also create the file in the web UI.
2. In the web UI edit `printer.cfg` and add this line above the `#*# <---- SAVE_CONFIG ---->` block, then save and restart:

   ```
   [include plotter.cfg]
   ```
3. Type `PEN_TOUCH` in the console. It should run, not say "unknown command".

More detail and optional edits are in [PLOTTER_CFG.md](PLOTTER_CFG.md).

## 4. Find `z_draw`

1. Tape paper flat on the bed.
2. Run `PEN_TOUCH`.
3. Jog down in steps, 0.5 mm then 0.1 mm near the end:

   ```
   G91
   G1 Z-0.5 F300
   ```
4. When the tip just touches, run `GET_POSITION` and enter that Z value as `z_draw` in the app.

## 5. Mesh the paper

1. Tape the sheet in place and **remove the pen cartridge.** The probe is at the nozzle and the pen would hit the bed first.
2. Paste the `PLOT_MESH` line from the app into the console.
3. Fit the pen again, run `PEN_TOUCH` and find `z_draw` with the plot mesh active. The earlier value was found without it.

## 6. Calibrate the offset

1. In the app press **Make calibration cross**, copy the G-code to a file and run it. The cross is centred at 120, 120.
2. Measure where its centre landed.
3. New offset = old offset + (measured - commanded), for X and Y separately.
4. Enter the new values and run the cross again until it is centred.

The starting offset is X +0.4, Y -26.45.

## 7. Plot

1. Load an SVG (or build one in the editor).
2. Set fit and origin and check the bed preview.
3. Each time: pen out, run the `PLOT_MESH` line, fit the pen, then upload and start the G-code.
4. For a dry run, use the same file with the pen retracted first.

## Notes

- The pen sits 26.45 mm in front of the nozzle. The nozzle travels to Y287, but the cartridge hits the rear panel at a pen position of about Y240. Keep drawings at or below Y240.
- An A4 sheet (210 x 297 mm) lined up with the rear-left corner hangs about 27 mm off the front edge of the bed. Put magnets within the 10 mm margins, not on the overhang.
- Bed mesh fade: stock Q2 `printer.cfg` has `fade_start: 1` and `fade_end: 10`, so at Z around 6 only about 43% of the mesh is applied. Set `fade_start: 8` and `fade_end: 20` under `[bed_mesh]` (prints are barely affected) so the pen gets the full correction.
- Faint or patchy lines are usually a Z problem: lower `z_draw` by 0.1 mm or add 0.3 mm extra press.
- Stroke speed is limited by the 2000 mm/s2 acceleration set in `PLOT_START`.
- The mesh is read at the nozzle position, about 26 mm behind the pen, so it corrects tilt and bowl shapes well but not small local bumps under the pen.
- Remove the cartridge before homing or printing again.
