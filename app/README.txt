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
  3. Open the printer door or lid, hold the phone level above the middle of the bed with the whole A4 sheet in view, and take the photo.
  4. The photo appears on the computer. Click the four corners of the sheet in the order shown (rear-left, rear-right, front-right, front-left). Drag a point to fine-tune using the zoom box, then press Apply.
  5. The photo now sits under the drawing in the bed preview. Use the opacity slider, or "Show photo under the drawing" to hide it.
  The sheet position comes from "Paper on the bed" (left edge X, rear edge Y). "Choose photo file" lets you use any photo from the computer instead.
  Only the phone page and photo upload are reachable from your Wi-Fi, and only with the one-time code in the QR link.
