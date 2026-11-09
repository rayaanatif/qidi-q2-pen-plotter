Q2 Pen Plotter - local app
==========================
Runs on your Mac or Windows computer, opens in your browser, and talks to the printer
(Moonraker) directly: upload G-code, run PLOT_MESH, start or cancel a plot.

You need Python 3.8 or newer (nothing else to install).
  Mac:     usually already there. Check in Terminal:  python3 --version
  Windows: install from python.org or the Microsoft Store (tick "Add python to PATH").

Start it
  Mac:     double-click run_mac.command   (first time: right-click, Open)
           or in Terminal:  python3 q2_plotter.py
  Windows: double-click run_windows.bat
           or in a terminal:  py q2_plotter.py

Then use the page in your browser (http://127.0.0.1:8765). Keep the small terminal window open.
It only listens on this computer and rejects requests without its one-time token.

Workflow
  1. Pen cartridge removed. Load your SVG, tick "pen cartridge is removed", press "Run PLOT_MESH".
  2. Fit the pen. Press "Upload G-code" (or "Upload and start plot" after ticking the box).
  3. First time only: find z_draw with PEN_TOUCH, enter it on the page, run the calibration cross.

Bed photo (phone camera)
  1. In the app press "Use phone camera". A QR code appears.
  2. Scan it with your phone (phone and computer on the same Wi-Fi). If Windows asks, allow Python through the firewall (private networks).
  3. Open the printer door or lid, hold the phone above the bed with the whole build plate in view and the printer's REAR at the top of the picture, and take the photo.
  4. A zoomed view opens with a small overview in the corner (the yellow box shows the zoomed area). Drag the picture, or tap the overview, until the crosshair sits exactly on each corner, then press Next corner. The point moves slower than your finger by the zoom factor. + / - or the mouse wheel change the zoom, arrow keys nudge, "Next guess" loads other starting positions and "Rotate photo 90" turns the photo. Press Done after the fourth corner.
  Two ways to align:
    - "Align to plate corners": tap the four corners of the build plate (rear-left, rear-right, front-right, front-left). Works wherever the paper is.
    - "Align to sheet corners": tap the four corners of the sheet instead, in the same order. Use this when the paper is placed exactly as set under "Paper on the bed" (left edge X, rear edge Y, size). It can be more accurate right where you will draw.
  Measure on photo: once the photo is aligned, press "Measure on photo", move the crosshair to a spot and press Add point for the next. It lists each point's bed X/Y, the distance and direction between points, path length, angles and the area. Distances are on the plate surface, so raised things (toolhead, rail) read wrong. "Copy results" copies the list.
  5. The photo sits under the drawing in the bed preview. Use the opacity slider, or "Show photo under the drawing" to hide it.
  "Block areas off the plate" shades everything outside the plate and keeps drawings out of it. Plate size, left X and rear Y (default 280 mm, -5, 275) say where the plate sits in machine coordinates; adjust them if the dashed plate outline is off.
  "Choose photo file" lets you use any photo from the computer instead.
  Only the phone page and photo upload are reachable from your Wi-Fi, and only with the one-time code in the QR link.
