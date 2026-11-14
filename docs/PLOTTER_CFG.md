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
| `PLOT_IDLE_HOLD` / `PLOT_IDLE_RESTORE` | Keep the motors on (and home kept) while you set up, then put the normal idle timeout back. Called by the macros above. |
| `PLOT_RESET` | Restores plot-time speeds, idle timeout and the `plotting` flag. Runs by itself (via `PLOT_WATCHDOG`) after a cancelled plot. |

Bounds in `PLOT_MESH` are **nozzle** positions. The pen is 26.45 mm in front of the nozzle.

## Settings in `PLOT_VARS`

| Variable | Default | Meaning |
| --- | --- | --- |
| `accel` | 2000 | Acceleration while plotting (mm/s2) |
| `corner` | 5.0 | Square corner velocity while plotting |
| `use_mesh` | 1 | 1 follows the `plot` mesh, 0 draws at flat Z |
| `mesh_profile` | `"plot"` | Profile name `PLOT_MESH` creates |
| `do_tilt` | 1 | Run `Z_TILT_ADJUST` before meshing |
| `park_x`, `park_y`, `park_z` | 85, 287.5, 13.8 | Idle park position = Qidi's default purge/trash position (rear chute). Out of the camera view and off the bed. It never lowers: if the toolhead is already higher it stays there. |
| `plotting` | 0 | Set to 1 by `PLOT_START`, back to 0 by `PLOT_END` or `PLOT_RESET` |
| `idle_hold` | 3600 | Idle timeout in seconds while you set up (QIDI stock 12 h; the Q2 tweaked package uses 5 min and turns the motors off) |

To change the park position, edit `park_x`, `park_y` and `park_z`. You can find a good spot by moving the toolhead there and running `GET_POSITION`.

## Cancelling a plot

Stock QIDI `CANCEL_PRINT` lifts to Z100 first and then moves to X265 Y5, so the pen is clear. It does not reset the plot speeds; `PLOT_WATCHDOG` does that within 5 s. See [Q2_TWEAKS.md](Q2_TWEAKS.md) for the firmware package review.
