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
  4. The app proposes the four corners of the build plate (yellow points). Check them, drag any that are off using the zoom box (corners hidden under a big sheet usually need a nudge), rotate the photo if needed, then press Apply.
  Buttons in the aligner: "Next guess" cycles through other starting boxes (your last confirmed corners come first), "Snap to edges" nudges the points onto straight edges, "Rotate photo 90" turns the photo.
  5. Auto-fit then finds the sheet on the plate from its own straight edges, at any position or angle, even with the toolhead or rail covering part of it, and fills in Paper on the bed (size, orientation, left edge, rear edge). If the sheet is turned, the green usable area is the biggest upright rectangle that fits inside it.
  6. The photo sits under the drawing in the bed preview. Use the opacity slider, or "Show photo under the drawing" to hide it.
  "Align by sheet corners" is the older manual method (tap the four sheet corners). "Choose photo file" lets you use any photo from the computer instead.
  Plate size, left X and rear Y (default 280 mm, -5, 275) describe where the plate sits in machine coordinates; adjust them if the outline is off. If your sheet is darker than the plate, change "The sheet looks" to darker.
  Only the phone page and photo upload are reachable from your Wi-Fi, and only with the one-time code in the QR link.
