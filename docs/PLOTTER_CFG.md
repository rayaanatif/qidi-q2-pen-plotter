# plotter.cfg

[`printer/plotter.cfg`](../printer/plotter.cfg) is the only file the printer needs. Pen offsets are applied by the app when it writes the G-code, so the macros only handle safety, speeds, the bed mesh and calibration.

## Install

See [SETUP.md](SETUP.md), step 3.

## Macros

| Macro | What it does |
| --- | --- |
| `PLOT_VARS` | Holds the settings (below). Running it prints the current mesh, profile and acceleration. |
| `PLOT_MESH` | Probes a bed mesh over the drawing area and keeps it in memory as profile `plot`. Run it with the pen cartridge **removed**. Takes `MIN_X MIN_Y MAX_X MAX_Y COUNT_X COUNT_Y`. The app prints a line with the right bounds for your drawing. |
| `PLOT_START` | Called at the top of the plot G-code. Refuses to run if not homed or if the `plot` mesh is missing, then loads the mesh and sets acceleration. |
| `PLOT_END` | Lifts, restores the printer state and speeds, and parks. |
| `PLOT_PARK` | Moves to the idle park position. Also handy before taking the bed photo. |
| `PEN_TOUCH` | Loads the mesh and moves to the middle of the bed so you can find `z_draw`. |

Bounds in `PLOT_MESH` are **nozzle** positions. The pen is 26.45 mm in front of the nozzle.

## Settings in `PLOT_VARS`

| Variable | Default | Meaning |
| --- | --- | --- |
| `accel` | 2000 | Acceleration while plotting (mm/s2) |
| `corner` | 5.0 | Square corner velocity while plotting |
| `use_mesh` | 1 | 1 follows the `plot` mesh, 0 draws at flat Z |
| `mesh_profile` | `"plot"` | Profile name `PLOT_MESH` creates |
| `do_tilt` | 1 | Run `Z_TILT_ADJUST` before meshing |
| `park_x`, `park_y`, `park_z` | 232, 125, 13.8 | Idle park position. Clears the camera view and makes it easy to reach the bed. It never lowers: if the toolhead is already higher it stays there. |
| `plotting` | 0 | Set to 1 by `PLOT_START`, back to 0 by `PLOT_END` |

To change the park position, edit `park_x`, `park_y` and `park_z`. You can find a good spot by moving the toolhead there and running `GET_POSITION`.

## Optional: CANCEL_PRINT

`PLOT_VARS.plotting` exists so a cancel macro can tell a plot from a print. The stock Qidi `CANCEL_PRINT` raises to Z100 and then moves to `X265 Y5`. If you want a cancelled plot to stop safely with the pen clear, add a check on `printer['gcode_macro PLOT_VARS'].plotting` there. This edit is not tested yet, so look at your own `gcode_macro.cfg` before changing anything.
