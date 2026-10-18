# LODs of PiCo logo

Team logo for the NDE HackaLOD 2026: three persons standing on the node positions
of the RDF logo, linked by NDE-style slices, seen through a perspective camera.

## Files

- `lods-of-pico.svg`: logo with text
- `lods-of-pico-mark.svg`: logo without text
- `lods-of-pico-animated.svg`: camera circling the group (SMIL, loops forever)
- `lods-of-pico-settings.json`: the settings everything above is built from
- `tweaker.html`: interactive page to tweak the settings
- `build_logo.py`: builds the SVGs from the settings, including the print
  variants listed under `variants` (horizontal, dark, embroidery, one-colour white)
- `build_mockups.py`: draws `mockups.svg`, the logo on a cap, scarf, hoodie and t-shirt

## Changing the logo

1. Open the tweaker. It needs a local web server:

   ```bash
   python3 -m http.server 8765 --directory logo
   ```

   Then browse to http://127.0.0.1:8765/tweaker.html
2. Move the sliders until it looks right, then click **Copy settings**.
3. Paste the result into `lods-of-pico-settings.json`.
4. Rebuild:

   ```bash
   python3 logo/build_logo.py && python3 logo/build_mockups.py
   ```

Colours, the label text and the animation length (`frames`, `duration_s`) are only
editable in the JSON file.

The tweaker and `build_logo.py` implement the same model twice (JavaScript and
Python). If you change one, change the other; with the same settings both
produce byte-identical SVGs.

## Before printing

The text is live Arial. Convert it to outlines first (Inkscape: Path → Object to
Path). For embroidery, switch off highlights: the thin white strokes don't stitch.
