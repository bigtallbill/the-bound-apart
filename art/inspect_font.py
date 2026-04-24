#!/usr/bin/env python3
"""Print each glyph's advance width and bounding box."""
import fontforge, pathlib

font = fontforge.open(str(pathlib.Path(__file__).resolve().parent / "TheBoundApart.ttf"))
print(f"em={font.em} ascent={font.ascent} descent={font.descent}")
for g in font.glyphs():
    if g.unicode < 0:
        continue
    ch = chr(g.unicode)
    bb = g.boundingBox()  # (xmin, ymin, xmax, ymax)
    print(f"  {ch!r} U+{g.unicode:04X}  width={g.width:4d}  bbox x=[{bb[0]:.1f},{bb[2]:.1f}] y=[{bb[1]:.1f},{bb[3]:.1f}]")
