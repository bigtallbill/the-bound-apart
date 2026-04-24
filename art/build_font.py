#!/usr/bin/env python3
"""Build TheBoundApart.ttf from language.svg.

Pipeline:
  1. Walk language.svg, extract each single-letter (A-Z) layer into its own
     temporary SVG with no background/grid layer.
  2. Use Inkscape to flatten stroked paths into filled outlines
     (fonts render filled paths, not strokes).
  3. Use FontForge to import each flattened glyph, scale/translate it into
     the font coordinate system, and generate a TTF.

Run under FontForge's bundled Python:

    nix-shell -p fontforge inkscape --run \\
        "fontforge -script art/build_font.py"

Requires inkscape and fontforge on PATH.
"""
from __future__ import annotations

import copy
import pathlib
import subprocess
import tempfile
import xml.etree.ElementTree as ET

import fontforge  # provided by fontforge's embedded Python interpreter

SVG_NS = "http://www.w3.org/2000/svg"
INK_NS = "http://www.inkscape.org/namespaces/inkscape"
SODI_NS = "http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"

ET.register_namespace("", SVG_NS)
ET.register_namespace("inkscape", INK_NS)
ET.register_namespace("sodipodi", SODI_NS)

HERE = pathlib.Path(__file__).resolve().parent
SRC = HERE / "language.svg"
OUT = HERE / "TheBoundApart.ttf"

# SVG canvas is 16.933333 x 25.4 mm. Letter body runs from the top grid row
# (y = 4.233) down to the bottom grid row (y = 21.167). The baseline is set
# at the bottom row so letters sit on it.
CANVAS_W = 16.933333
CANVAS_H = 25.4
TOP_ROW = 4.233333
BOT_ROW = 21.166666
BASELINE_FROM_BOTTOM = CANVAS_H - BOT_ROW  # 4.233333 mm

EM = 1000
SCALE = EM / CANVAS_H  # ~39.37 font units per mm
ASCENT = int(round((CANVAS_H - BASELINE_FROM_BOTTOM) * SCALE))  # 833
DESCENT = EM - ASCENT  # 167
ADVANCE = int(round(CANVAS_W * SCALE))  # 667 — monospace cell width


def is_letter_layer(elem: ET.Element) -> str | None:
    if elem.tag != f"{{{SVG_NS}}}g":
        return None
    if elem.get(f"{{{INK_NS}}}groupmode") != "layer":
        return None
    label = elem.get(f"{{{INK_NS}}}label", "")
    if len(label) == 1 and "A" <= label <= "Z":
        return label
    return None


def strip_display_none(elem: ET.Element) -> None:
    for node in elem.iter():
        style = node.get("style")
        if style and "display:none" in style:
            node.set(
                "style",
                ";".join(
                    s for s in style.split(";") if s.strip() and "display:none" not in s
                ),
            )


def force_fill_none_on_paths(elem: ET.Element) -> None:
    """Force fill:none on every <path>. Circles keep their fill.

    Inkscape's object-stroke-to-path emits the interior fill shape in
    addition to the stroke outline whenever fill is anything but `none`
    (even `fill:#000000;fill-opacity:0`). For a font we only want the
    stroke outline, so strip any fill declarations from paths.
    """
    path_tag = f"{{{SVG_NS}}}path"
    for node in elem.iter():
        if node.tag != path_tag:
            continue
        style = node.get("style", "")
        segments = [
            s for s in style.split(";")
            if s.strip() and not s.strip().startswith(("fill:", "fill-opacity:"))
        ]
        segments.insert(0, "fill:none")
        node.set("style", ";".join(segments))
        # Also strip standalone fill attributes if present.
        for attr in ("fill", "fill-opacity"):
            if attr in node.attrib:
                del node.attrib[attr]


def extract_letter_svg(root: ET.Element, layer: ET.Element, out_path: pathlib.Path) -> None:
    """Write an SVG containing only this letter's layer (no grid background)."""
    new_root = ET.Element(root.tag, dict(root.attrib))
    for child in root:
        if child.tag == f"{{{SVG_NS}}}defs":
            new_root.append(copy.deepcopy(child))
            break
    layer_copy = copy.deepcopy(layer)
    strip_display_none(layer_copy)
    force_fill_none_on_paths(layer_copy)
    new_root.append(layer_copy)
    ET.ElementTree(new_root).write(out_path, encoding="utf-8", xml_declaration=True)


def flatten_strokes(in_svg: pathlib.Path, out_svg: pathlib.Path) -> None:
    """Inkscape: expand each stroke to its own filled outline path.

    Does not union the resulting paths — keeping strokes as independent
    outlines preserves the intended shape (unioning can fill enclosed
    regions when fill rules disagree).
    """
    actions = ";".join(
        [
            "select-all",
            "object-stroke-to-path",
            f"export-filename:{out_svg}",
            "export-plain-svg",
            "export-overwrite",
            "export-do",
        ]
    )
    subprocess.run(
        ["inkscape", f"--actions={actions}", str(in_svg)],
        check=True,
        capture_output=True,
    )


def main() -> None:
    tree = ET.parse(SRC)
    root = tree.getroot()

    letter_layers: dict[str, ET.Element] = {}
    for child in list(root):
        letter = is_letter_layer(child)
        if letter is not None:
            letter_layers[letter] = child

    if not letter_layers:
        raise SystemExit("No letter layers found in language.svg")

    font = fontforge.font()
    font.fontname = "TheBoundApart"
    font.familyname = "TheBoundApart"
    font.fullname = "TheBoundApart"
    font.em = EM
    font.ascent = ASCENT
    font.descent = DESCENT
    font.encoding = "UnicodeFull"

    with tempfile.TemporaryDirectory() as td:
        tmp = pathlib.Path(td)
        for letter, layer in sorted(letter_layers.items()):
            raw = tmp / f"{letter}.svg"
            flat = tmp / f"{letter}_flat.svg"
            extract_letter_svg(root, layer, raw)
            flatten_strokes(raw, flat)

            glyph = font.createChar(ord(letter), letter)
            glyph.importOutlines(str(flat))
            # FontForge auto-maps the SVG viewBox into the em box (SVG bottom
            # -> y=-descent, SVG top -> y=ascent), Y-flipped. Because we set
            # ascent=833 / descent=167 from the grid rows, the letter baseline
            # (bottom grid row) already lands at y=0 — no transform needed.
            glyph.width = ADVANCE
            glyph.correctDirection()

        space = font.createChar(ord(" "), "space")
        space.width = ADVANCE

    font.generate(str(OUT))
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
