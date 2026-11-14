# Using the "QIDI Q2 02.04 Tweaked" package with the plotter

Review of [muchak1994-lpg/qidi-q2-0204-tweaked](https://github.com/muchak1994-lpg/qidi-q2-0204-tweaked) (release 1.0.0) for a Q2 that is also used as a pen plotter or cutter. This is a read-through of its docs, the module definitions and six module diffs, plus a check of the hosts its tools download from (QIDI's public server, PyPI, Debian). The installer was not run. It only works on firmware **01.01.02.04**, so check that first.

## Skip

| Module | Why |
|---|---|
| `z-home-random-point` | Homes Z at a random point within 10 mm of the centre. The plot mesh and `z_draw` are tied to the Z zero found at the last homing. The module's own note says the zero differs by up to about 0.04 mm 10 mm away, and that is a visible change in pen pressure. The wear argument is weak next to that. Stock behaviour is better here. |
| `ai-libraries`, `ai-fixes` | About 100 MB of libraries for the camera AI. Only worth it if you use the foreign-object / spaghetti check. |
| `box-heater-keepalive`, `box-fixes`, `box-fan-threshold`, `moonraker-box-status-merge` | Only matter with a QIDI Box. |
| `screen-drying-*`, `dark-mode-light`, `dns-fallback-global` | Cosmetic or network-region tweaks. Fine either way. |

## Install (real value for plotting and cutting)

| Module | Why it matters here |
|---|---|
| `probe-retry-fix` | Without it a mesh point whose two samples disagree is re-probed forever. `PLOT_MESH` would hang. Highest value. |
| `fluidd-z-like-screen` | Fluidd's Z arrows move the bed the same way as the screen. With a pen or blade below the nozzle, a wrong-way jog is a crash. |
| `save-variables-atomic`, `z-offset-persistence` | A power cut cannot leave an empty settings file, and temporary Z offsets are not saved as yours. |
| `homing-trsync`, `mcu-ack-timeout`, `mcu-restart-shutdown`, `serialqueue-fixes`, `serialqueue-clock-margin`, `stepcompress-far`, `heater-comm-loss-message`, `tmc-direction-event` | Upstream Klipper fixes: cleaner errors and fewer hangs during long jobs. |
| `klipper-priority`, `restart-on-exit` | Klipper gets the CPU first (Nice -10); Klipper and Moonraker restart after a clean exit. Small, safe startup improvements. |
| `3mf-cache`, `print-cache-protection`, `gcode-history`, `fluidd-fixes` | Faster file handling, no corrupted print cache, usable controls while paused. |
| `update-check-off`, `firmware-download-guard` | Stops the screen pushing an update that would replace 02.04 for good. |
| `park-rear-right` | After a print or stop the head parks at the rear right (X260 Y260) instead of the front right. Plot park is separate (`PLOT_PARK`). |
| `z-home-guard` | Home Z alone is refused unless X and Y are homed and the nozzle is over the plate. It does **not** stop a Home Z with the pen fitted, so keep removing the pen before homing. |

## Install, but with our macros

`idle-timeout-drying` changes the idle timeout from 12 h to **5 min and turns the motors off**, which forgets home. Homing must be done with the pen removed, so losing it while you fit the pen or jog for `z_draw` costs you a re-home with the pen off again. The updated `plotter.cfg` holds the idle timeout (default 1 h) during `PLOT_MESH`, `PEN_TOUCH` and `PLOT_START`, and restores the configured value at `PLOT_END`. It never changes the timeout while any heater is on. The drying fixes in that module are kept.

## Changes in `printer/plotter.cfg`

- `PLOT_IDLE_HOLD` / `PLOT_IDLE_RESTORE`: the idle-timeout handling above. `PLOT_VARS.idle_hold` sets the hold in seconds.
- `PLOT_RESET` and a `PLOT_WATCHDOG` delayed macro: if a plot that runs as a file print is cancelled, nothing ran `PLOT_END`, and acceleration and corner speed stay at the plot values for the next print (stock QIDI does not reset them: `CANCEL_PRINT` only sets `M204`). The watchdog notices the print ended and restores them within 5 s, and clears the `plotting` flag.
- Stock `CANCEL_PRINT` already lifts to Z100 before moving to X265 Y5, so a cancelled plot is safe for the pen without editing QIDI's file. That is why no `CANCEL_PRINT` edit is needed any more.

Checked: the file parses and all 11 macro bodies compile as Jinja. Not run on a printer yet: after copying it over, restart Klipper, run `PLOT_VARS`, and cancel a short plot once to see the "plot state reset" message.

## How to install

```
py tools/printer.py check --host PRINTER_IP        (read-only: is it 02.04?)
py tools/install.py plan  --host PRINTER_IP --skip z-home-random-point --skip ai-libraries --skip ai-fixes
py tools/install.py install --host PRINTER_IP --skip z-home-random-point --skip ai-libraries --skip ai-fixes
```

Add more `--skip MODULE` options from the tables above. Keep the `backups/` folder it creates. Install the `plotter.cfg` afterwards; the installer only edits QIDI's own lines.
