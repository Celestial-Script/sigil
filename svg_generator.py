#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SVG generation functionality for converting glyph data to SVG format for 云篆 (sigil).
"""

import re
from typing import List, Optional, Tuple

from models import GlyphData, FontMetrics, SVGConfig
from utils import UtilityFunctions


class SVGGenerator:
    """Generates SVG content from glyph data."""
    
    def __init__(self, config: SVGConfig):
        """
        Initialize SVGGenerator with configuration.
        
        Args:
            config: SVG generation configuration
        """
        self._config = config
    
    def generate_single_svg(
        self, 
        glyph_data: GlyphData, 
        font_metrics: FontMetrics,
        pinyin: str = ""
    ) -> str:
        """
        Generate SVG for a single glyph.
        
        Args:
            glyph_data: Glyph data
            font_metrics: Font metrics
            pinyin: Pinyin annotation
            
        Returns:
            SVG content as string
        """
        return self._build_single_svg(
            upm=font_metrics.units_per_em,
            d=glyph_data.path,
            bounds=glyph_data.bounds,
            codepoint=glyph_data.codepoint,
            glyph_name=glyph_data.name,
            font_name=font_metrics.font_name,
            advance_width=glyph_data.advance_width,
            pinyin=pinyin
        )
    
    def generate_row_svg(
        self, 
        glyphs_data: List[GlyphData], 
        font_metrics: FontMetrics,
        pinyin_tokens: List[str]
    ) -> str:
        """
        Generate SVG for multiple glyphs in a row.
        
        Args:
            glyphs_data: List of glyph data
            font_metrics: Font metrics
            pinyin_tokens: List of pinyin tokens
            
        Returns:
            SVG content as string
        """
        # Convert GlyphData objects to the format expected by _build_row_svg
        glyphs = [
            (gd.path, gd.bounds, gd.name, gd.codepoint, gd.advance_width)
            for gd in glyphs_data
        ]
        
        return self._build_row_svg(
            upm=font_metrics.units_per_em,
            glyphs=glyphs,
            font_name=font_metrics.font_name,
            pinyin_tokens=pinyin_tokens
        )
    
    def _calculate_tian_transform(
        self, 
        bounds: Optional[Tuple[float, float, float, float]], 
        cell: float
    ) -> str:
        """
        Calculate transformation matrix for tian grid fitting.
        
        Args:
            bounds: Glyph bounding box
            cell: Cell size
            
        Returns:
            Transform attribute string
        """
        if not bounds:
            return ""
            
        xmin, ymin, xmax, ymax = map(float, bounds)
        glyph_width = xmax - xmin
        glyph_height = ymax - ymin
        
        if glyph_width <= 0 or glyph_height <= 0:
            return ""
            
        target_width = cell * self._config.tian_frac
        target_height = cell * self._config.tian_frac
        
        if self._config.tian_preserve_aspect:
            scale = min(target_width / glyph_width, target_height / glyph_height)
            sx = sy = scale
        else:
            sx = target_width / glyph_width
            sy = target_height / glyph_height
            
        # Center the glyph at the cell's cross point
        cx_glyph = (xmin + xmax) / 2.0
        cy_glyph = (ymin + ymax) / 2.0
        cx_cell = cy_cell = cell / 2.0
        
        tx = cx_cell - (cx_glyph * sx)
        ty = cy_cell - (cy_glyph * sy)
        
        fmt = UtilityFunctions.format_number
        return f' transform="matrix({fmt(sx)} 0 0 {fmt(sy)} {fmt(tx)} {fmt(ty)})"'
    
    def _build_single_svg(
        self,
        upm: int,
        d: str,
        bounds: Optional[Tuple[float, float, float, float]],
        codepoint: int,
        glyph_name: str,
        font_name: str,
        advance_width: float,
        pinyin: str = ""
    ) -> str:
        """Build SVG content for a single glyph."""
        
        fmt = UtilityFunctions.format_number
        
        # Canvas geometry calculation
        if self._config.bbox_mode == "tight":
            if bounds is None:
                w = advance_width if (advance_width and advance_width > 0) else upm / 2
                h = upm
                xmin, ymin, xmax, ymax = 0.0, 0.0, float(w), float(h)
            else:
                xmin, ymin, xmax, ymax = map(float, bounds)
                
            content_w = (xmax - xmin)
            content_h = (ymax - ymin)
            
            if self._config.grid_kind != "none":
                content_w = upm
                content_h = upm
                xmin, ymin = 0.0, 0.0
                
            vb_w = content_w + 2 * self._config.margin_units
            vb_h = content_h + 2 * self._config.margin_units
            
            pinyin_top = pinyin_bottom = 0.0
            if pinyin and self._config.grid_kind != "none":
                block = self._config.pinyin_size_units * 1.2 + self._config.pinyin_gap_units
                if self._config.pinyin_pos == "top":
                    pinyin_top = block
                elif self._config.pinyin_pos == "bottom":
                    pinyin_bottom = block
                    
            vb_h += pinyin_top + pinyin_bottom
            ty = self._config.margin_units + pinyin_top + content_h
            transform = f"translate({fmt(self._config.margin_units)} {fmt(ty)}) scale(1 -1)"
            
            pre_translate = ""
            if self._config.grid_kind == "none" and bounds is not None:
                pre_translate = f' transform="translate({fmt(-xmin)} {fmt(-ymin)})"'
                
            grid_x0, cell = 0.0, (upm if self._config.grid_kind != "none" else content_h)
        else:
            # em mode
            content_w = content_h = upm
            vb_w = upm + 2 * self._config.margin_units
            
            pinyin_top = pinyin_bottom = 0.0
            if pinyin:
                block = self._config.pinyin_size_units * 1.2 + self._config.pinyin_gap_units
                if self._config.pinyin_pos == "top":
                    pinyin_top = block
                elif self._config.pinyin_pos == "bottom":
                    pinyin_bottom = block
                    
            vb_h = upm + 2 * self._config.margin_units + pinyin_top + pinyin_bottom
            ty = self._config.margin_units + pinyin_top + upm
            transform = f"translate({fmt(self._config.margin_units)} {fmt(ty)}) scale(1 -1)"
            pre_translate = ""
            grid_x0, cell = 0.0, upm
        
        # Size attributes
        size_attrs = ""
        if self._config.px_height and vb_h > 0:
            scale = self._config.px_height / vb_h
            size_attrs = f' width="{fmt(vb_w*scale)}" height="{fmt(self._config.px_height)}"'
        
        # Metadata
        cp_hex = f"U+{codepoint:04X}"
        aria_label = chr(codepoint) or cp_hex
        meta = f"<metadata>font={font_name}; glyph={glyph_name}; cp={cp_hex}; unitsPerEm={upm}</metadata>"
        
        # Glyph styling
        glyph_style = [f"fill:{self._config.fill}"]
        if self._config.stroke:
            glyph_style.append(f"stroke:{self._config.stroke}")
            if self._config.stroke_width_px:
                glyph_style.append(f"stroke-width:{fmt(self._config.stroke_width_px)}")
        glyph_style_str = ";".join(glyph_style)
        
        # Grid elements
        grid_elems = self._generate_grid_elements(grid_x0, cell)
        
        # Tian grid transformation
        if self._config.grid_kind == "tian":
            tian_transform = self._calculate_tian_transform(bounds, cell)
            if tian_transform:
                pre_translate = tian_transform
        
        # Pinyin elements
        pinyin_elems = self._generate_pinyin_elements(pinyin, vb_w, vb_h, content_w)
        
        # Build SVG
        svg_lines = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {fmt(vb_w)} {fmt(vb_h)}"{size_attrs} aria-label="{aria_label}">',
            f"  {meta}",
            f'  <g transform="{transform}">',
        ]
        
        if grid_elems:
            svg_lines.append(f"    {grid_elems}")
            
        svg_lines.extend([
            f'    <path d="{d}" style="{glyph_style_str}"{pre_translate}/>',
            "  </g>",
        ])
        
        if pinyin_elems:
            svg_lines.append(pinyin_elems)
            
        svg_lines.append("</svg>")
        
        return "\n".join(svg_lines) + "\n"
    
    def _generate_grid_elements(self, grid_x0: float, cell: float) -> str:
        """Generate grid elements based on grid kind."""
        if self._config.grid_kind == "none":
            return ""
            
        fmt = UtilityFunctions.format_number
        border_style = (f'stroke:{self._config.grid_color};'
                       f'stroke-width:{fmt(self._config.grid_border_width)};'
                       f'fill:none;vector-effect:non-scaling-stroke')
        guide_style = (f'stroke:{self._config.grid_color};'
                      f'stroke-width:{fmt(self._config.grid_guide_width)};'
                      f'fill:none;vector-effect:non-scaling-stroke')
        
        if self._config.grid_dash:
            guide_style += f";stroke-dasharray:{self._config.grid_dash}"
            
        x = grid_x0
        elements = [f'\n    <rect x="{fmt(x)}" y="0" width="{fmt(cell)}" height="{fmt(cell)}" style="{border_style}"/>']
        
        if self._config.grid_kind in ("tian", "mi"):
            cx = x + cell/2
            cy = cell/2
            elements.extend([
                f'\n    <line x1="{fmt(cx)}" y1="0" x2="{fmt(cx)}" y2="{fmt(cell)}" style="{guide_style}"/>',
                f'\n    <line x1="{fmt(x)}" y1="{fmt(cy)}" x2="{fmt(x+cell)}" y2="{fmt(cy)}" style="{guide_style}"/>',
            ])
            
        if self._config.grid_kind == "mi":
            elements.extend([
                f'\n    <line x1="{fmt(x)}" y1="0" x2="{fmt(x+cell)}" y2="{fmt(cell)}" style="{guide_style}"/>',
                f'\n    <line x1="{fmt(x)}" y1="{fmt(cell)}" x2="{fmt(x+cell)}" y2="0" style="{guide_style}"/>',
            ])
            
        return "".join(elements)
    
    def _generate_pinyin_elements(self, pinyin: str, vb_w: float, vb_h: float, content_w: float) -> str:
        """Generate pinyin text elements."""
        if not pinyin:
            return ""
            
        fmt = UtilityFunctions.format_number
        y = (self._config.margin_units + self._config.pinyin_size_units 
             if self._config.pinyin_pos == "top" 
             else vb_h - self._config.margin_units - self._config.pinyin_size_units * 0.2)
        x_center = self._config.margin_units + (content_w / 2.0)
        
        font_attr = f' font-family="{self._config.pinyin_font}"' if self._config.pinyin_font else ""
        
        return (f'\n  <text x="{fmt(x_center)}" y="{fmt(y)}"{font_attr} '
                f'font-size="{fmt(self._config.pinyin_size_units)}" text-anchor="middle" '
                f'fill="{self._config.fill}" dominant-baseline="alphabetic">{pinyin}</text>')
    
    def _build_row_svg(
        self,
        upm: int,
        glyphs: List[Tuple[str, Optional[Tuple[float,float,float,float]], str, int, float]],
        font_name: str,
        pinyin_tokens: List[str]
    ) -> str:
        """Build SVG content for multiple glyphs in a row."""
        
        fmt = UtilityFunctions.format_number
        n = len(glyphs)
        cell = self._config.cell_units
        content_w = n * cell
        content_h = cell
        
        pinyin_top = pinyin_bottom = 0.0
        if any(pinyin_tokens):
            block = self._config.pinyin_size_units * 1.2 + self._config.pinyin_gap_units
            if self._config.pinyin_pos == "top":
                pinyin_top = block
            elif self._config.pinyin_pos == "bottom":
                pinyin_bottom = block
        
        vb_w = content_w + 2 * self._config.margin_units
        vb_h = content_h + 2 * self._config.margin_units + pinyin_top + pinyin_bottom
        
        size_attrs = ""
        if self._config.px_height and vb_h > 0:
            scale = self._config.px_height / vb_h
            size_attrs = f' width="{fmt(vb_w*scale)}" height="{fmt(self._config.px_height)}"'
        
        ty = self._config.margin_units + pinyin_top + content_h
        transform = f"translate({fmt(self._config.margin_units)} {fmt(ty)}) scale(1 -1)"
        
        svg_lines = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {fmt(vb_w)} {fmt(vb_h)}"{size_attrs}>',
            f'  <metadata>font={font_name}; unitsPerEm={upm}; cells={n}; grid={self._config.grid_kind}</metadata>',
            f'  <g transform="{transform}">',
        ]
        
        # Generate grid for each cell
        if self._config.grid_kind != "none":
            border_style = (f'stroke:{self._config.grid_color};'
                           f'stroke-width:{fmt(self._config.grid_border_width)};'
                           f'fill:none;vector-effect:non-scaling-stroke')
            guide_style = (f'stroke:{self._config.grid_color};'
                          f'stroke-width:{fmt(self._config.grid_guide_width)};'
                          f'fill:none;vector-effect:non-scaling-stroke')
            
            if self._config.grid_dash:
                guide_style += f";stroke-dasharray:{self._config.grid_dash}"
            
            for i in range(n):
                x0 = cell * i
                svg_lines.append(f'    <rect x="{fmt(x0)}" y="0" width="{fmt(cell)}" height="{fmt(cell)}" style="{border_style}"/>')
                
                if self._config.grid_kind in ("tian", "mi"):
                    cx = x0 + cell/2
                    cy = cell/2
                    svg_lines.extend([
                        f'    <line x1="{fmt(cx)}" y1="0" x2="{fmt(cx)}" y2="{fmt(cell)}" style="{guide_style}"/>',
                        f'    <line x1="{fmt(x0)}" y1="{fmt(cy)}" x2="{fmt(x0+cell)}" y2="{fmt(cy)}" style="{guide_style}"/>',
                    ])
                    
                if self._config.grid_kind == "mi":
                    svg_lines.extend([
                        f'    <line x1="{fmt(x0)}" y1="0" x2="{fmt(x0+cell)}" y2="{fmt(cell)}" style="{guide_style}"/>',
                        f'    <line x1="{fmt(x0)}" y1="{fmt(cell)}" x2="{fmt(x0+cell)}" y2="0" style="{guide_style}"/>',
                    ])
        
        # Generate glyph styling
        glyph_style = [f"fill:{self._config.fill}"]
        if self._config.stroke:
            glyph_style.append(f"stroke:{self._config.stroke}")
            if self._config.stroke_width_px:
                glyph_style.append(f"stroke-width:{fmt(self._config.stroke_width_px)}")
        glyph_style_str = ";".join(glyph_style)
        
        # Generate glyphs
        for i, (d, bounds, glyph_name, cp, _aw) in enumerate(glyphs):
            if self._config.grid_kind == "tian":
                # Scale to tian_frac of the cell and center at each cell's cross point
                x0 = cell * i
                transform_attr = self._calculate_tian_transform(bounds, cell)
                if transform_attr:
                    # Adjust transformation for the i-th cell
                    match = re.search(r"matrix\(([^)]+)\)", transform_attr)
                    if match:
                        a, b, c, d_m, e, f_m = [float(v.strip()) for v in match.group(1).split()]
                        e += x0  # Shift to the i-th cell
                        transform_attr = f' transform="matrix({fmt(a)} 0 0 {fmt(d_m)} {fmt(e)} {fmt(f_m)})"'
                    svg_lines.append(f'    <path d="{d}" style="{glyph_style_str}"{transform_attr}/>')
                    continue
            
            # Default placement: put glyph origin at left of the cell
            dx = cell * i
            svg_lines.append(f'    <g transform="translate({fmt(dx)} 0)"><path d="{d}" style="{glyph_style_str}"/></g>')
        
        svg_lines.append("  </g>")
        
        # Add pinyin
        if any(pinyin_tokens):
            font_attr = f' font-family="{self._config.pinyin_font}"' if self._config.pinyin_font else ""
            base_y = (self._config.margin_units + self._config.pinyin_size_units 
                     if self._config.pinyin_pos == "top" 
                     else vb_h - self._config.margin_units - self._config.pinyin_size_units * 0.2)
            
            for i, token in enumerate(pinyin_tokens):
                if not token:
                    continue
                cx = self._config.margin_units + (i + 0.5) * cell
                svg_lines.append(
                    f'  <text x="{fmt(cx)}" y="{fmt(base_y)}"{font_attr} font-size="{fmt(self._config.pinyin_size_units)}" '
                    f'text-anchor="middle" fill="{self._config.fill}" dominant-baseline="alphabetic">{token}</text>'
                )
        
        svg_lines.append("</svg>")
        return "\n".join(svg_lines) + "\n"