# Qidi Q2 pen plotter

Clip-on toolhead attachments for the Qidi Q2, in the style of Bambu Lab's toolhead tools. Pen plotting is finished and working reliably. Cutting and debossing are next.

Pen plotting needs one cfg file on the printer (`plotter.cfg`, included from `printer.cfg`), three printed parts and a web app that runs on your own computer.

## What is in the web app

- Import as many SVGs as you want into one workspace. Move, scale, rotate, flip, mirror, align and snap them.
- Upload PNG or JPEG images and convert them to SVG, tuned in the app: outline, photo edges or tone. Send the result straight to the workspace.
- Built-in editor for text (single-stroke font, so each letter is drawn once) and shapes: rectangle, ellipse, line, polygon, star, spiral.
- Paper sizes and presets, with offsets and positions. Filled regions as outline plus hatch fill. Tone fill turns different shades into different crosshatch densities.
- Whole-page mode: plots the area the pen can reach, you turn the sheet 180 degrees, and it plots the rest.
- Multi-pen layers, plot simulation, undo and redo, project save and load.
- Bed photo: scan a QR code, take a picture of your print bed with your phone, tap the four plate corners (or the four sheet corners) in a zoomed view and it sits under your drawing so you can place things exactly.
- Upload G-code, run `PLOT_MESH`, start and cancel a plot, straight from the app (local helper app only).
- A Cutter tab with the planned settings. It is a scaffold: it does not generate cutting G-code yet.

## Status

| Feature | Status |
| --- | --- |
| Pen plotting (single pass, one pen) | Working on a real Q2 |
| Park position, `PLOT_MESH`, `PEN_TOUCH`, calibration cross | Working on a real Q2 |
| Tone fill, two-pass whole page, multi-pen output, simulation | Tested and working on Q2 |
| Phone bed photo overlay | Tested and working |
| Cutter | Sleeve designed, not printed or cut yet. See [docs/CUTTER.md](docs/CUTTER.md) |
| Debossing | Planned |

Please report results, good or bad, in an issue.

## Quick start

1. Print the parts in [hardware/](hardware/README.md).
2. Follow [docs/SETUP.md](docs/SETUP.md): mount, `plotter.cfg`, `z_draw`, mesh, calibrate.
3. Run the app from [app/](app/README.txt) and plot.

## Where things are

| Path | What |
| --- | --- |
| `docs/SETUP.md` | Step by step first-time setup |
| `docs/PLOTTER_CFG.md` | What each macro does and how to install it |
| `docs/DEFAULTS.md` | Values that worked on my Q2 and where they come from |
| `docs/CUTTER.md` | Cutter design, blades and what is still to do |
| `printer/plotter.cfg` | The Klipper config file |
| `app/page.html` + `q2_plotter.py` | Local helper app (printer upload, photo route) |
| `app/web-only.html` | Same converter as a single page with no helper |
| `hardware/stl`, `hardware/step` | Cover, bay, cartridges and cutter sleeves |

## Safety

The pen cartridge sticks out below the nozzle. Home with it removed, fit it afterwards, and take it off before you home or print again. Everything here has only been tried on one Q2, so check the first plot with the pen retracted (a dry run) before you trust it.

## License

GPL-3.0, see [LICENSE](LICENSE).
