Q2 Pen Plotter PRO - local app
==============================
The tuned version: everything in the standard app plus photo alignment from pen-drawn marks and
line weight (thick lines and solid colour with a marker). Same helper script, same way to run it.
Runs on your Mac or Windows computer, opens in your browser, and talks to the printer
(Moonraker) directly: upload G-code, run PLOT_MESH, start or cancel a plot.

You need Python 3.8 or newer (nothing else to install).
  Mac:     usually already there. Check in Terminal:  python3 --version
  Windows: install from python.org or the Microsoft Store (tick "Add python to PATH").

What is new in Pro
  Workspace layout (like Bambu Studio / OrcaSlicer)
    Editing happens right on the Prepare canvas: the tool strip on its left adds SVG files, Image to SVG, text, rectangle, ellipse, line, star, polygon, spiral, the calibration cross and the alignment marks. Every shape is a normal object on the bed: drag it, use the corner squares to resize and the round handle to rotate it, type exact W/H/X/Y/rotation in the bar above the canvas, and change its own settings (text, letter size, corner radius, points, tone fill) in the Shape settings panel on the right. Delete removes the selected object.
    Text uses a Word-style panel: font list, size in pt or mm, bold / italic / underline, left / centre / right, letter and line spacing. The default is the single-line pen font, which plots fastest. Included fonts (Liberation Sans/Serif/Mono, Carlito, Caladea, Lora, Work Sans, Outfit and a few display faces) work everywhere. In Chrome or Edge, Load fonts on this computer lists everything installed (the browser asks permission once). Add font file takes TTF, OTF, WOFF or TTC. Outline fonts are drawn as outlines, or hatched with Fill with tone; variable fonts and WOFF2 are not supported, and there is no kerning.
    Cutting and deboss: every object has a Tool setting in the bar above the canvas (Draw pen, Cut blade, Deboss stylus). Each tool becomes its own G-code file; pick it in the list above the G-code, fit that tool and run it without moving the sheet. The cutter assumes a Roland-style swivel blade (45 degree, 0.25 mm trail offset): the head path leads the blade, corners are swivelled or lifted and re-dropped (angle set on the Cutter tab), closed shapes start mid-edge with a run-in and overcut, inner shapes are cut first, and all passes of the whole job run before the next, deeper pass. Cut files reuse PLOT_START / PLOT_END, so plotter.cfg needs no change. Measure the blade offsets and the cut Z on scrap card before a real job; the Add a test cut button places a square and circle.
    Cutting-mat registration: tick Using the green cutting mat under Photo of the bed. The mat (trimmed to the plate size, laid square on the plate) is found by its green colour, then its 1 inch grid straightens the fit. In synthetic photos the plate corners came out within 0.5 mm; the result is only as good as the mat's trim and how squarely it sits (1 mm out of place gives about 1.5 mm error). Tell it which side of the photo the printer's rear is on (the square mat looks the same turned). Washed-out green and LED glare are tolerated. Show the mat grid the app found draws the lines it fitted in cyan on the bed view so you can check them against the photo's lines.
    Theme: the button at the right of the tab bar cycles Dark (default), Light and Auto (follows the system). The choice is remembered in the browser.
    Top tabs: Prepare, Preview, Device, Settings (then Image to SVG, Cutter). The top bar shows whether the printer is online.
    Prepare: Drawing, arrange and bed photo on the left (drop SVG files on the box); the bed in the middle (drag to move, corner squares to resize); the selected drawing's size and position, a "Settings at a glance" summary and the "Ready to plot?" checklist on the right (each open item has a Go link).
    Preview: simulation of the pen path with a scrub bar, and the G-code with Copy, Download .gcode, the calibration cross and the photo alignment marks.
    Device: printer status (Refresh, or check every 15 s), connection and upload / start / cancel / emergency stop, the PLOT_MESH command and button, and a G-code console with Home all, Motors off and Firmware restart. Needs the local helper (q2_plotter.py) running and the page opened from its address.
    Paper mode: the green dashed box is the area the pen can use. With Paper mode off it is simply what the pen can reach on the plate, with no margin. Tick Paper mode (Settings, Paper on the bed) to see the sheet outline and the margin inside it; the box is always limited to the plate, so margin that would hang off the bed is cut off. Sheet size, position, margin and two-pass options only appear in Paper mode.
    Settings: sheet and paper, pen and machine (offsets, z_draw, speeds), fill and shading, pen width and lines, several pens. All settings are remembered.
  Image to SVG drawing styles
    On the Image to SVG tab, besides the Trace modes (outline, photo edges, tone) there are six drawing styles for photos: Hatching (1-4 cross-hatch directions by tone), Squiggles (wavy lines, tighter where dark), Stipples (dots, denser where dark), Flow lines (strokes that follow the shapes in the picture), Spiral (one wobbling spiral) and Halftone (circles sized by tone). Spacing, wave size and dot size are in real millimetres, and "Output width (mm)" sets the physical size, so what you see is what plots. The preview draws lines at your pen width.
    Colour pens: split the picture into CMYK, red/green/blue plus black, or up to four pen colours of your own. Each colour gets its own set of lines at its own angle (the preview mixes them like ink). Send it to the Convert tab and tick "Separate pens by colour" for one G-code file per pen.
    Also: brightness, contrast and gamma, crop to an ellipse, ink amount, and Download SVG. Dense styles make many strokes and long plot times: check the "draw" length in the stats and raise the spacing if needed.
  Photo alignment marks (no more corner tapping)
    1. Put the sheet on the bed. Under "Paper on the bed" set where it is and its size.
    2. On the Preview tab, press "Make photo alignment marks" and plot that G-code with a black pen. It draws six ringed crosses just inside the sheet edges (inset set next to the button, default 7 mm) at exact bed positions, so the pen itself defines the reference. Keep your artwork inside the margins so a line does not touch a mark.
    3. Take the bed photo as usual. The app finds the marks and aligns the photo by itself ("Aligned automatically from N alignment marks"). If it cannot find them it opens the corner-tapping view as before. "Auto-align from marks" re-runs the search.
    No pen-drawn marks? Press "Printable alignment sheet" (Preview tab) for the same six rings as a true-size SVG for your sheet size, or use printables/alignment_sheet_A4.pdf (A4, rings 14 mm in). Print at 100%, put it with its rear-left corner at the X / Y set under Sheet and paper (default X 0, Y 270), rear at the top, tape it flat, then take the photo.
    Needs: black or dark pen, the four corner marks in view and not under the toolhead or your hand, and the paper settings unchanged since you drew the marks. Accuracy is best near the marks and a little less in the far corners of the plate.
  Pen width and line weight
    Pen tip width (mm) and Pass overlap (%) describe your pen. A stroke thicker than the pen (the SVG stroke-width, or "Force all lines to") is drawn as parallel overlapping passes, so a 2 mm line with a 0.5 mm marker becomes about 5 passes. "Solid fills" sets the fill line spacing to pen width less overlap, so a filled area comes out solid. The preview can draw lines at the real pen width. Thick lines make many strokes: the app stops with a message when a job gets too big.

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

Reference sheet (alignment without pen marks)
Print hardware/registration-plate/q2_regsheet_A3.pdf (or the 2xA4 version) at 100%, tape it flat on the plate with its rear-left corner on the plate's rear-left corner. In "Photo of the bed" tick "Using alignment reference sheet", take the photo with the toolhead parked (Park toolhead for photo), and the app aligns from the sheet's 12 printed rings (needs at least 8 visible). Plate size/position fields must match your plate (default 280 mm, X -5, rear Y 275).
