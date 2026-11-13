# Cutter (work in progress)

Nothing here has been cut yet. The parts are designed and fit-checked on a computer only.

## Approach

- A **GCC blade holder** (spring-loaded pin on top, 30/45/60 degree blades). The bay hangs it by its flange. A **printed coil on the pin** sets the cutting force, so the blade backs off when the surface rises instead of digging in. This is the same principle as the Bambu cutter.
- No extra components, everything is printed. See [hardware/cutter-gcc](../hardware/cutter-gcc/README.md) for the bay, the three coil variants, the assumptions and the force table.
- Cut on a sticky cutting mat, never straight onto the PEI plate.
- The page mesh (`PLOT_MESH`) follows the surface. The cut force is set by Z through the spring.

## Superseded

The swivel drag-knife sleeve (`hardware/stl/qs_cutter_sleeve_*`) and the floating cartridge in `hardware/cutter-float` do not fit the GCC holder.

## To do

- Print, then measure the real coil rate and the blade offset.
- Calibrate Z against force with a scale (pin depression to grams).
- Tool profile in the app: blade offset, force target to Z, safe Z near the purge bin.
- Cutting G-code: blade-trail compensation and corner handling for the 30/45/60 degree blades, overcut on closed shapes, inner shapes first.
