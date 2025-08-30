#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
glyph2svg: Export characters from a font to SVG, with optional Chinese practice grids and Hanyu Pinyin.

NEW:
- For --grid tian, the glyph is scaled so its bbox is exactly (tian_frac × cell) in both width & height
  and centered at the cell's cross point. Default tian_frac = 2/3.
- Add --tian-preserve-aspect to keep uniform scaling (≤ 2/3 in one axis), otherwise X/Y are scaled independently.
"""

import argparse
import os
import re
import sys
from typing import List, Optional, Tuple

from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen

# --------------------------- small utilities ---------------------------

def fmt(n: float, decimals: int = 3) -> str:
    s = f"{n:.{decimals}f}".rstrip("0").rstrip(".")
    return s if s else "0"

def parse_codepoint(s: str) -> int:
    s = s.strip()
    if not s:
        raise ValueError("Empty character argument.")
    if len(s) == 1 and not s.startswith(("U+","u+","0x","0X")) and not s.isdigit():
        return ord(s)
    if s.lower().startswith("u+"): return int(s[2:], 16)
    if s.lower().startswith("0x"): return int(s[2:], 16)
    if re.fullmatch(r"[0-9a-fA-F]+", s) and not re.fullmatch(r"\d+", s):
        return int(s, 16)
    if re.fullmatch(r"\d+", s):
        return int(s, 10)
    return ord(s[0])

def parse_units_or_percent(spec: Optional[str], ref: float, *, default: float = 0.0) -> float:
    if spec is None:
        return default
    s = str(spec).strip()
    if s.endswith("%"):
        return float(s[:-1]) * 0.01 * ref
    return float(s)

def split_chars(text: str) -> List[str]:
    return [c for c in text]

# --------------------------- Pinyin helpers ---------------------------

TONE_MARKS = {
    "a": "āáǎàa", "e": "ēéěèe", "i": "īíǐìi", "o": "ōóǒòo", "u": "ūúǔùu", "ü": "ǖǘǚǜü",
}

def numbered_token_to_marked(token: str) -> str:
    m = re.fullmatch(r"([A-Za-züÜ:]+)([0-5])", token)
    if not m: return token
    base, num = m.group(1), int(m.group(2))
    tone_index = 4 if num in (0,5) else num - 1
    norm = (base.replace("u:", "ü").replace("U:", "Ü").replace("v", "ü").replace("V", "Ü"))
    lower = norm.lower()
    def find_mark_pos(s: str) -> Optional[int]:
        if "a" in s: return s.index("a")
        if "e" in s: return s.index("e")
        if "ou" in s: return s.index("o")
        if "iu" in s: return s.index("u")
        if "ui" in s: return s.index("i")
        for v in "o i u ü".split():
            if v in s: return s.index(v)
        for i, ch in enumerate(s):
            if ch in "aeoiuü": return i
        return None
    pos = find_mark_pos(lower)
    if pos is None: return token
    target = lower[pos]
    if target not in TONE_MARKS: return token
    marked_lower = TONE_MARKS[target][tone_index]
    repl = marked_lower.upper() if norm[pos].isupper() else marked_lower
    return norm[:pos] + repl + norm[pos+1:]

def normalize_pinyin_for_chars(pinyin: Optional[str], n_chars: int) -> List[str]:
    if not pinyin: return [""] * n_chars
    tokens = [t for t in re.split(r"[,\s;/|]+", pinyin.strip()) if t]
    tokens = [numbered_token_to_marked(t) for t in tokens]
    if len(tokens) == 1 and n_chars > 1: tokens = tokens * n_chars
    if len(tokens) != n_chars:
        print(f"warning: pinyin token count ({len(tokens)}) != character count ({n_chars}); trunc/pad applied.", file=sys.stderr)
        tokens = (tokens + [""] * n_chars)[:n_chars]
    return tokens

# --------------------------- font helpers ---------------------------

def glyph_path_and_bounds(font: TTFont, glyph_name: str) -> Tuple[str, Optional[Tuple[float, float, float, float]]]:
    glyph_set = font.getGlyphSet()
    glyph = glyph_set[glyph_name]
    svg_pen = SVGPathPen(glyph_set); glyph.draw(svg_pen)
    d = svg_pen.getCommands()
    bp = BoundsPen(glyph_set); glyph.draw(bp)
    return d, bp.bounds

# --------------------------- SVG composition ---------------------------

def _tian_transform(bounds, cell, frac, preserve_aspect):
    """
    Compute matrix(a b c d e f) that scales a glyph's bbox to (frac*cell) in X & Y
    and centers its bbox at (cell/2, cell/2) in font (Y-up) coordinates.
    """
    if not bounds:
        return ""
    xmin, ymin, xmax, ymax = map(float, bounds)
    gw = xmax - xmin; gh = ymax - ymin
    if gw <= 0 or gh <= 0:
        return ""
    target_w = cell * frac; target_h = cell * frac
    if preserve_aspect:
        s = min(target_w / gw, target_h / gh)
        sx = sy = s
    else:
        sx = target_w / gw
        sy = target_h / gh
    cx_g = (xmin + xmax) / 2.0
    cy_g = (ymin + ymax) / 2.0
    cx_cell = cy_cell = cell / 2.0
    tx = cx_cell - (cx_g * sx)
    ty = cy_cell - (cy_g * sy)
    return f' transform="matrix({fmt(sx)} 0 0 {fmt(sy)} {fmt(tx)} {fmt(ty)})"'

def build_single_svg(
    *,
    upm: int,
    d: str,
    bounds: Optional[Tuple[float, float, float, float]],
    codepoint: Optional[int],
    glyph_name: str,
    font_name: str,
    bbox_mode: str,
    margin_units: float,
    px_height: Optional[float],
    fill: str,
    stroke: Optional[str],
    stroke_width_px: Optional[float],
    grid_kind: str,
    grid_color: str,
    grid_border_w: float,
    grid_guide_w: float,
    grid_dash: Optional[str],
    pinyin: str,
    pinyin_pos: str,
    pinyin_font: Optional[str],
    pinyin_size_units: float,
    pinyin_gap_units: float,
    advance_width: Optional[float],
    # NEW:
    tian_frac: float,
    tian_preserve_aspect: bool,
) -> str:

    # --- Canvas geometry ---
    if bbox_mode == "tight":
        if bounds is None:
            w = advance_width if (advance_width and advance_width > 0) else upm / 2
            h = upm
            xmin, ymin, xmax, ymax = 0.0, 0.0, float(w), float(h)
        else:
            xmin, ymin, xmax, ymax = map(float, bounds)
        content_w = (xmax - xmin)
        content_h = (ymax - ymin)
        if grid_kind != "none":
            content_w = upm
            content_h = upm
            xmin, ymin = 0.0, 0.0
        vb_w = content_w + 2 * margin_units
        vb_h = content_h + 2 * margin_units
        pinyin_top = pinyin_bottom = 0.0
        if pinyin and grid_kind != "none":
            block = pinyin_size_units * 1.2 + pinyin_gap_units
            if pinyin_pos == "top": pinyin_top = block
            elif pinyin_pos == "bottom": pinyin_bottom = block
        vb_h += pinyin_top + pinyin_bottom
        ty = margin_units + pinyin_top + content_h
        transform = f"translate({fmt(margin_units)} {fmt(ty)}) scale(1 -1)"
        pre_translate = ""
        if grid_kind == "none" and bounds is not None:
            pre_translate = f' transform="translate({fmt(-xmin)} {fmt(-ymin)})"'
        grid_x0, cell = 0.0, (upm if grid_kind != "none" else content_h)
    else:
        content_w = content_h = upm
        vb_w = upm + 2 * margin_units
        pinyin_top = pinyin_bottom = 0.0
        if pinyin:
            block = pinyin_size_units * 1.2 + pinyin_gap_units
            if pinyin_pos == "top": pinyin_top = block
            elif pinyin_pos == "bottom": pinyin_bottom = block
        vb_h = upm + 2 * margin_units + pinyin_top + pinyin_bottom
        ty = margin_units + pinyin_top + upm
        transform = f"translate({fmt(margin_units)} {fmt(ty)}) scale(1 -1)"
        pre_translate = ""
        grid_x0, cell = 0.0, upm

    size_attrs = ""
    if px_height and vb_h > 0:
        scale = px_height / vb_h
        size_attrs = f' width="{fmt(vb_w*scale)}" height="{fmt(px_height)}"'

    cp_hex = f"U+{codepoint:04X}" if codepoint is not None else ""
    aria_label = (chr(codepoint) if codepoint is not None else "") or cp_hex
    meta = f"<metadata>font={font_name}; glyph={glyph_name}; cp={cp_hex}; unitsPerEm={upm}</metadata>"

    glyph_style = [f"fill:{fill}"]
    if stroke:
        glyph_style.append(f"stroke:{stroke}")
        if stroke_width_px:
            glyph_style.append(f"stroke-width:{fmt(stroke_width_px)}")
    glyph_style = ";".join(glyph_style)

    grid_elems = ""
    if grid_kind != "none":
        border_style = f'stroke:{grid_color};stroke-width:{fmt(grid_border_w)};fill:none;vector-effect:non-scaling-stroke'
        guide_style  = f'stroke:{grid_color};stroke-width:{fmt(grid_guide_w)};fill:none;vector-effect:non-scaling-stroke'
        if grid_dash: guide_style += f";stroke-dasharray:{grid_dash}"
        x = grid_x0
        grid_elems += f'\n    <rect x="{fmt(x)}" y="0" width="{fmt(cell)}" height="{fmt(cell)}" style="{border_style}"/>'
        if grid_kind in ("tian", "mi"):
            cx = x + cell/2; cy = cell/2
            grid_elems += f'\n    <line x1="{fmt(cx)}" y1="0" x2="{fmt(cx)}" y2="{fmt(cell)}" style="{guide_style}"/>'
            grid_elems += f'\n    <line x1="{fmt(x)}" y1="{fmt(cy)}" x2="{fmt(x+cell)}" y2="{fmt(cy)}" style="{guide_style}"/>'
        if grid_kind == "mi":
            grid_elems += f'\n    <line x1="{fmt(x)}" y1="0" x2="{fmt(x+cell)}" y2="{fmt(cell)}" style="{guide_style}"/>'
            grid_elems += f'\n    <line x1="{fmt(x)}" y1="{fmt(cell)}" x2="{fmt(x+cell)}" y2="0" style="{guide_style}"/>'

    # --- NEW: tian grid fit (2/3) & centering ---
    if grid_kind == "tian":
        tian_xform = _tian_transform(bounds, cell, tian_frac, tian_preserve_aspect)
        if tian_xform:
            pre_translate = tian_xform

    pinyin_elems = ""
    if pinyin:
        y = margin_units + (pinyin_size_units if pinyin_pos == "top" else vb_h - margin_units - pinyin_size_units*0.2)
        x_center = margin_units + (content_w / 2.0)
        font_attr = f' font-family="{pinyin_font}"' if pinyin_font else ""
        pinyin_elems = (
            f'\n  <text x="{fmt(x_center)}" y="{fmt(y)}"{font_attr} '
            f'font-size="{fmt(pinyin_size_units)}" text-anchor="middle" '
            f'fill="{fill}" dominant-baseline="alphabetic">{pinyin}</text>'
        )

    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {fmt(vb_w)} {fmt(vb_h)}"{size_attrs} aria-label="{aria_label}">']
    svg.append(f"  {meta}")
    svg.append(f'  <g transform="{transform}">')
    if grid_elems:
        svg.append(f"    {grid_elems}")
    svg.append(f'    <path d="{d}" style="{glyph_style}"{pre_translate}/>')
    svg.append("  </g>")
    if pinyin_elems:
        svg.append(pinyin_elems)
    svg.append("</svg>")
    return "\n".join(svg) + "\n"

def build_row_svg(
    *,
    upm: int,
    glyphs: List[Tuple[str, Optional[Tuple[float,float,float,float]], str, int, float]],
    font_name: str,
    margin_units: float,
    px_height: Optional[float],
    fill: str,
    stroke: Optional[str],
    stroke_width_px: Optional[float],
    grid_kind: str,
    grid_color: str,
    grid_border_w: float,
    grid_guide_w: float,
    grid_dash: Optional[str],
    pinyin_tokens: List[str],
    pinyin_pos: str,
    pinyin_font: Optional[str],
    pinyin_size_units: float,
    pinyin_gap_units: float,
    cell_units: Optional[float] = None,
    # NEW:
    tian_frac: float = 2/3,
    tian_preserve_aspect: bool = False,
) -> str:

    n = len(glyphs)
    cell = cell_units or upm
    content_w = n * cell
    content_h = cell

    pinyin_top = pinyin_bottom = 0.0
    if any(pinyin_tokens):
        block = pinyin_size_units * 1.2 + pinyin_gap_units
        if pinyin_pos == "top": pinyin_top = block
        elif pinyin_pos == "bottom": pinyin_bottom = block

    vb_w = content_w + 2 * margin_units
    vb_h = content_h + 2 * margin_units + pinyin_top + pinyin_bottom

    size_attrs = ""
    if px_height and vb_h > 0:
        scale = px_height / vb_h
        size_attrs = f' width="{fmt(vb_w*scale)}" height="{fmt(px_height)}"'

    ty = margin_units + pinyin_top + content_h
    transform = f"translate({fmt(margin_units)} {fmt(ty)}) scale(1 -1)"

    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {fmt(vb_w)} {fmt(vb_h)}"{size_attrs}>']
    svg.append(f"  <metadata>font={font_name}; unitsPerEm={upm}; cells={n}; grid={grid_kind}</metadata>")
    svg.append(f'  <g transform="{transform}">')

    if grid_kind != "none":
        border_style = f'stroke:{grid_color};stroke-width:{fmt(grid_border_w)};fill:none;vector-effect:non-scaling-stroke'
        guide_style  = f'stroke:{grid_color};stroke-width:{fmt(grid_guide_w)};fill:none;vector-effect:non-scaling-stroke'
        if grid_dash: guide_style += f";stroke-dasharray:{grid_dash}"
        for i in range(n):
            x0 = cell * i
            svg.append(f'    <rect x="{fmt(x0)}" y="0" width="{fmt(cell)}" height="{fmt(cell)}" style="{border_style}"/>')
            if grid_kind in ("tian","mi"):
                cx = x0 + cell/2; cy = cell/2
                svg.append(f'    <line x1="{fmt(cx)}" y1="0" x2="{fmt(cx)}" y2="{fmt(cell)}" style="{guide_style}"/>')
                svg.append(f'    <line x1="{fmt(x0)}" y1="{fmt(cy)}" x2="{fmt(x0+cell)}" y2="{fmt(cy)}" style="{guide_style}"/>')
            if grid_kind == "mi":
                svg.append(f'    <line x1="{fmt(x0)}" y1="0" x2="{fmt(x0+cell)}" y2="{fmt(cell)}" style="{guide_style}"/>')
                svg.append(f'    <line x1="{fmt(x0)}" y1="{fmt(cell)}" x2="{fmt(x0+cell)}" y2="0" style="{guide_style}"/>')

    glyph_style = [f"fill:{fill}"]
    if stroke:
        glyph_style.append(f"stroke:{stroke}")
        if stroke_width_px:
            glyph_style.append(f"stroke-width:{fmt(stroke_width_px)}")
    glyph_style = ";".join(glyph_style)

    for i, (d, bounds, glyph_name, cp, _aw) in enumerate(glyphs):
        if grid_kind == "tian":
            # Scale to 2/3 of the cell and center at each cell's cross point
            x0 = cell * i
            xform = _tian_transform(bounds, cell, tian_frac, tian_preserve_aspect)
            if xform:
                # shift into the i-th cell by adding x0 to tx
                # xform is matrix(a 0 0 d e f). We need to add x0 to e.
                # Safer: rebuild with parsed pieces
                m = re.search(r"matrix\(([^)]+)\)", xform)
                if m:
                    a,b,c,d_m,e,f_m = [float(v.strip()) for v in m.group(1).split()]
                    e += x0
                    xform = f' transform="matrix({fmt(a)} 0 0 {fmt(d_m)} {fmt(e)} {fmt(f_m)})"'
                svg.append(f'    <path d="{d}" style="{glyph_style}"{xform}/>')
                continue
        # default placement (no special fit): put glyph origin at left of the cell
        dx = cell * i
        svg.append(f'    <g transform="translate({fmt(dx)} 0)"><path d="{d}" style="{glyph_style}"/></g>')

    svg.append("  </g>")

    if any(pinyin_tokens):
        font_attr = f' font-family="{pinyin_font}"' if pinyin_font else ""
        base_y = margin_units + (pinyin_size_units if pinyin_pos == "top" else vb_h - margin_units - pinyin_size_units*0.2)
        for i, token in enumerate(pinyin_tokens):
            if not token: continue
            cx = margin_units + (i + 0.5) * cell
            svg.append(
                f'  <text x="{fmt(cx)}" y="{fmt(base_y)}"{font_attr} font-size="{fmt(pinyin_size_units)}" '
                f'text-anchor="middle" fill="{fill}" dominant-baseline="alphabetic">{token}</text>'
            )

    svg.append("</svg>")
    return "\n".join(svg) + "\n"

# --------------------------- main ---------------------------

def main():
    parser = argparse.ArgumentParser(
        prog="glyph2svg",
        description="Export characters from a font to SVG, with optional Chinese grids and Pinyin.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("-f", "--font", required=True, help="Path to .ttf/.otf/.ttc/.otc font file.")
    g = parser.add_mutually_exclusive_group(required=True)
    g.add_argument("-c", "--char", help="Single character or code point (A, 中, U+4E2D, 0x4E2D, 20013).")
    g.add_argument("-t", "--text", help="One or more literal characters (e.g., '示例').")
    parser.add_argument("-o", "--output", help="Output SVG filepath (default: derived from input).")
    parser.add_argument("--index", type=int, default=0, help="Face index for .ttc/.otc (default: 0).")

    parser.add_argument("--bbox", choices=["tight", "em"], default="tight",
                        help="Bounding box for single-char mode. With grids/multi-chars, em-sized cells are used.")
    parser.add_argument("--margin", default="2%", help="Outer margin in units or % of UPM.")
    parser.add_argument("--px-size", type=float, help="Set SVG height in pixels; width autoscaled.")
    parser.add_argument("--fill", default="currentColor", help="Glyph fill color.")
    parser.add_argument("--stroke", help="Glyph stroke color.")
    parser.add_argument("--stroke-width", type=float, help="Glyph stroke width in px.")

    parser.add_argument("--grid", choices=["none", "square", "fang", "tian", "mi"], default="none",
                        help="Practice grid: square(=fang), tian(田字格), mi(米字格).")
    parser.add_argument("--grid-color", default="#888", help="Grid stroke color.")
    parser.add_argument("--grid-border-width", default="1.2%", help="Outer border stroke width (units or % of cell).")
    parser.add_argument("--grid-guide-width", default="0.6%", help="Guide line stroke width (units or % of cell).")
    parser.add_argument("--grid-dash", default="4,6", help="Dash pattern for guide lines (empty for solid).")
    parser.add_argument("--cell-size", default=None, help="Cell size in units or % of UPM (default: 100% of UPM).")

    parser.add_argument("--pinyin", help="Hanyu Pinyin (tone numbers auto-converted, e.g., 'shi4 li4').")
    parser.add_argument("--pinyin-pos", choices=["top", "bottom"], default="top", help="Pinyin position.")
    parser.add_argument("--pinyin-font", help="CSS font-family for Pinyin.")
    parser.add_argument("--pinyin-size", default="18%", help="Pinyin font-size (units or % of cell).")
    parser.add_argument("--pinyin-gap", default="6%", help="Gap between Pinyin and grid (units or % of cell).")

    # NEW: tian configuration
    parser.add_argument("--tian-frac", type=float, default=2/3,
                        help="Fraction of the cell to occupy along each axis in 田字格 (default: 0.6667).")
    parser.add_argument("--tian-preserve-aspect", action="store_true",
                        help="Keep uniform scaling in 田字格; the larger dimension becomes tian-frac of the cell, the other ≤ tian-frac.")

    args = parser.parse_args()
    grid_kind = "square" if args.grid == "fang" else args.grid

    try:
        font = TTFont(args.font, fontNumber=args.index)
    except Exception as e:
        print(f"error: failed to open font '{args.font}': {e}", file=sys.stderr); sys.exit(2)

    upm = int(font["head"].unitsPerEm)
    margin_units = parse_units_or_percent(args.margin, upm)

    if args.text:
        chars = split_chars(args.text)
    else:
        cp = parse_codepoint(args.char)
        try: chars = [chr(cp)]
        except ValueError:
            print(f"error: invalid code point: U+{cp:04X}", file=sys.stderr); sys.exit(2)

    pinyin_tokens = normalize_pinyin_for_chars(args.pinyin, len(chars))
    cell_units = parse_units_or_percent(args.cell_size, upm, default=upm) if args.cell_size else upm
    grid_border_w = parse_units_or_percent(args.grid_border_width, cell_units)
    grid_guide_w  = parse_units_or_percent(args.grid_guide_width,  cell_units)
    grid_dash = args.grid_dash.strip() if args.grid_dash else None
    pinyin_size_units = parse_units_or_percent(args.pinyin_size, cell_units)
    pinyin_gap_units  = parse_units_or_percent(args.pinyin_gap,  cell_units)

    cmap = font.getBestCmap() or {}
    glyphs_data = []
    for ch in chars:
        cp = ord(ch)
        glyph_name = cmap.get(cp) or font.getGlyphName(0)
        if glyph_name == font.getGlyphName(0) and cp not in cmap:
            print(f"warning: U+{cp:04X} not in font; exporting '.notdef'.", file=sys.stderr)
        d, bounds = glyph_path_and_bounds(font, glyph_name)
        try: aw = float(font["hmtx"].metrics[glyph_name][0])
        except Exception: aw = float(upm)
        glyphs_data.append((d, bounds, glyph_name, cp, aw))

    try:
        name_tbl = font["name"]
        family = name_tbl.getDebugName(1) or ""
        subfam = name_tbl.getDebugName(2) or ""
        full = name_tbl.getDebugName(4) or ""
        font_name = (full or (family + (" " + subfam if subfam and subfam.lower() != "regular" else ""))).strip() or os.path.basename(args.font)
    except Exception:
        font_name = os.path.basename(args.font)

    if len(chars) == 1 and grid_kind == "none" and not args.pinyin:
        d, bounds, gname, cp, aw = glyphs_data[0]
        svg = build_single_svg(
            upm=upm, d=d, bounds=bounds, codepoint=cp, glyph_name=gname, font_name=font_name,
            bbox_mode=args.bbox, margin_units=margin_units, px_height=args.px_size,
            fill=args.fill, stroke=args.stroke, stroke_width_px=args.stroke_width,
            grid_kind="none", grid_color=args.grid_color, grid_border_w=grid_border_w,
            grid_guide_w=grid_guide_w, grid_dash=grid_dash,
            pinyin="", pinyin_pos=args.pinyin_pos, pinyin_font=args.pinyin_font,
            pinyin_size_units=pinyin_size_units, pinyin_gap_units=pinyin_gap_units,
            advance_width=aw,
            tian_frac=args.tian_frac, tian_preserve_aspect=args.tian_preserve_aspect,
        )
    elif len(chars) == 1:
        d, bounds, gname, cp, aw = glyphs_data[0]
        svg = build_single_svg(
            upm=upm, d=d, bounds=bounds, codepoint=cp, glyph_name=gname, font_name=font_name,
            bbox_mode="em", margin_units=margin_units, px_height=args.px_size,
            fill=args.fill, stroke=args.stroke, stroke_width_px=args.stroke_width,
            grid_kind=grid_kind, grid_color=args.grid_color, grid_border_w=grid_border_w,
            grid_guide_w=grid_guide_w, grid_dash=grid_dash,
            pinyin=pinyin_tokens[0], pinyin_pos=args.pinyin_pos, pinyin_font=args.pinyin_font,
            pinyin_size_units=pinyin_size_units, pinyin_gap_units=pinyin_gap_units,
            advance_width=aw,
            tian_frac=args.tian_frac, tian_preserve_aspect=args.tian_preserve_aspect,
        )
    else:
        svg = build_row_svg(
            upm=upm, glyphs=glyphs_data, font_name=font_name, margin_units=margin_units, px_height=args.px_size,
            fill=args.fill, stroke=args.stroke, stroke_width_px=args.stroke_width,
            grid_kind=grid_kind, grid_color=args.grid_color, grid_border_w=grid_border_w,
            grid_guide_w=grid_guide_w, grid_dash=grid_dash,
            pinyin_tokens=pinyin_tokens, pinyin_pos=args.pinyin_pos, pinyin_font=args.pinyin_font,
            pinyin_size_units=pinyin_size_units, pinyin_gap_units=pinyin_gap_units,
            cell_units=cell_units,
            tian_frac=args.tian_frac, tian_preserve_aspect=args.tian_preserve_aspect,
        )

    outpath = args.output or (f"U+{ord(chars[0]):04X}.svg" if len(chars)==1 else "-".join(f"U+{ord(c):04X}" for c in chars)+".svg")
    try:
        with open(outpath, "w", encoding="utf-8") as f: f.write(svg)
    except Exception as e:
        print(f"error: failed to write '{outpath}': {e}", file=sys.stderr); sys.exit(1)

    if len(chars) == 1:
        print(f"✓ Wrote {outpath}")
        print(f"   font: {font_name} | glyph: {glyphs_data[0][2]} | codepoint: U+{ord(chars[0]):04X}")
        if grid_kind == "tian":
            mode = "uniform" if args.tian_preserve_aspect else "anisotropic"
            print(f"   田字格 fit: {fmt(args.tian_frac)} of cell (mode: {mode}); centered at cross point")
    else:
        print(f"✓ Wrote {outpath}")
        if grid_kind == "tian":
            mode = "uniform" if args.tian_preserve_aspect else "anisotropic"
            print(f"   田字格 per cell: {fmt(args.tian_frac)} of cell (mode: {mode}); each centered")
    if args.px_size:
        print(f"   pixel height: {args.px_size}px (width auto)")

if __name__ == "__main__":
    main()
