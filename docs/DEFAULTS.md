# Defaults that worked on my Q2

These are the starting values in the app and `plotter.cfg`. They come from tests on my own Q2, so treat them as a good starting point, not a guarantee. `z_draw` is different on every printer and pen, so measure yours.

## Pen geometry

| Value | Default | Notes |
| --- | --- | --- |
| Pen offset X | +0.4 mm | Pen tip relative to the nozzle |
| Pen offset Y | -26.45 mm | Pen is in front of the nozzle |
| Nozzle limits | X 0 to 270, Y 0 to 287 | |
| Pen rear limit | Y 240 | Measured: the cartridge hits the rear panel beyond about Y240 |
| Pen front limit | offset Y + 1 mm | |
| Pen tip below nozzle | about 5 mm | When fitting the cartridge |
| `z_draw` | measure it | Use `PEN_TOUCH` with the plot mesh loaded |

## Motion

| Value | Default |
| --- | --- |
| Draw speed | 2400 mm/min |
| Travel speed | 9000 mm/min |
| Z speed | 1200 mm/min |
| Acceleration while plotting | 2000 mm/s2 |
| Square corner velocity | 5 |
| Path smoothing | 0.03 mm |

## Idle park position

X 232, Y 125, Z 13.8. Clears the camera's view and the area for moving paper in and out.

## Paper and mesh

| Value | Default |
| --- | --- |
| Sheet | A4, 210 x 297 mm |
| Mesh area (nozzle) | X 10 to 200, Y 36 to 260 |
| Mesh points | 5 x 6, Lagrange |
| Usable drawing area on A4 | about 190 x 250 mm with 10 mm margins |
| `[bed_mesh]` fade | `fade_start: 8`, `fade_end: 20` |

## Hardware

| Value | Default |
| --- | --- |
| Screws | M2x8 only (one clamp screw on the bay) |
| Magnets | 4x 5 x 2 mm |
| Cartridge bore | 9.0, 9.5 or 10.0 mm, pick to fit your pen |
| Cartridge | 12.6 mm outside diameter, 40 mm long, 16 mm collar |
| Bay bore | 12.8 mm |
