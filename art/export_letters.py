#!/usr/bin/env python3
"""Export each letter layer (A-Z) of language.svg into its own SVG file.

Reads language.svg, and for each top-level <g> whose inkscape:label is a
single letter A-Z, writes art/letters/<letter>.svg containing the
background/grid layer plus that letter's layer (display forced on).
"""
from __future__ import annotations

import copy
import pathlib
import xml.etree.ElementTree as ET

SVG_NS = "http://www.w3.org/2000/svg"
INK_NS = "http://www.inkscape.org/namespaces/inkscape"
SODI_NS = "http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"

ET.register_namespace("", SVG_NS)
ET.register_namespace("inkscape", INK_NS)
ET.register_namespace("sodipodi", SODI_NS)

HERE = pathlib.Path(__file__).resolve().parent
SRC = HERE / "language.svg"
OUT_DIR = HERE / "letters"


def is_letter_layer(elem: ET.Element) -> str | None:
    """Return the letter label if elem is a single-letter A-Z layer."""
    if elem.tag != f"{{{SVG_NS}}}g":
        return None
    if elem.get(f"{{{INK_NS}}}groupmode") != "layer":
        return None
    label = elem.get(f"{{{INK_NS}}}label", "")
    if len(label) == 1 and "A" <= label <= "Z":
        return label
    return None


def strip_display_none(elem: ET.Element) -> None:
    """Force layer and descendants to be visible by removing display:none."""
    for node in elem.iter():
        style = node.get("style")
        if style and "display:none" in style:
            node.set(
                "style",
                ";".join(
                    seg for seg in style.split(";") if seg.strip() and "display:none" not in seg
                ),
            )


def main() -> int:
    tree = ET.parse(SRC)
    root = tree.getroot()

    OUT_DIR.mkdir(exist_ok=True)

    # Collect letter layers and the background (non-letter) layer(s).
    letter_layers: dict[str, ET.Element] = {}
    background_layers: list[ET.Element] = []
    for child in list(root):
        if child.tag != f"{{{SVG_NS}}}g":
            continue
        letter = is_letter_layer(child)
        if letter is not None:
            letter_layers[letter] = child
        elif child.get(f"{{{INK_NS}}}groupmode") == "layer":
            background_layers.append(child)

    if not letter_layers:
        print("No letter layers found.")
        return 1

    written: list[str] = []
    for letter, layer in letter_layers.items():
        new_root = ET.Element(root.tag, dict(root.attrib))
        # Copy defs if present (not strictly needed here, but harmless).
        for child in root:
            if child.tag == f"{{{SVG_NS}}}defs":
                new_root.append(copy.deepcopy(child))
                break

        for bg in background_layers:
            new_root.append(copy.deepcopy(bg))

        layer_copy = copy.deepcopy(layer)
        strip_display_none(layer_copy)
        new_root.append(layer_copy)

        out_path = OUT_DIR / f"{letter}.svg"
        ET.ElementTree(new_root).write(out_path, encoding="utf-8", xml_declaration=True)
        written.append(out_path.name)

    print(f"Wrote {len(written)} files to {OUT_DIR}: {', '.join(sorted(written))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
