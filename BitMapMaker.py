import argparse
from PIL import Image, ImageDraw
import freetype

def render_font_spritesheet_freetype(ttf_path, size, output_path, cols=16, border=1):
    PINK = (255, 0, 255)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    face = freetype.Face(ttf_path)
    face.set_pixel_sizes(0, size)

    chars = [chr(c) for c in range(32, 127)]

    # Collect glyph raster and metrics
    glyphs = []
    max_advance = 0
    max_above = 0   # pixels above baseline (bitmap_top)
    max_below = 0   # pixels below baseline (bitmap.rows - bitmap_top)

    for ch in chars:
        face.load_char(ch, freetype.FT_LOAD_RENDER | freetype.FT_LOAD_TARGET_NORMAL)
        g = face.glyph
        bmp = g.bitmap
        width, rows = bmp.width, bmp.rows
        bitmap_left = g.bitmap_left
        bitmap_top = g.bitmap_top
        advance = (g.advance.x >> 6)  # 26.6 -> integer pixels

        # compute above/below baseline for this glyph
        above = bitmap_top
        below = rows - bitmap_top

        max_advance = max(max_advance, advance)
        max_above = max(max_above, above)
        max_below = max(max_below, below)

        # copy the bitmap buffer (bytes) for later
        buffer = bytes(bmp.buffer) if bmp.buffer else b''

        glyphs.append({
            'char': ch,
            'width': width,
            'rows': rows,
            'bitmap_left': bitmap_left,
            'bitmap_top': bitmap_top,
            'advance': advance,
            'buffer': buffer
        })

    # cell dimensions (pink border around each cell)
    inner_w = max_advance
    inner_h = max_above + max_below
    cell_w = inner_w + border * 2
    cell_h = inner_h + border * 2

    rows = (len(chars) + cols - 1) // cols
    sheet_w = cols * cell_w + border
    sheet_h = rows * cell_h + border

    sheet = Image.new("RGB", (sheet_w, sheet_h), PINK)
    draw = ImageDraw.Draw(sheet)

    # top of baseline relative to cell top: border + max_above
    baseline_offset = border + max_above

    for idx, g in enumerate(glyphs):
        col = idx % cols
        row = idx // cols

        cell_x_outer = col * cell_w
        cell_y_outer = row * cell_h

        # inside black rect top-left (after 1px pink border)
        inner_x = cell_x_outer + border
        inner_y = cell_y_outer + border

        # draw black rectangle (inside pink border)
        draw.rectangle([inner_x, inner_y, inner_x + inner_w - 1, inner_y + inner_h - 1], fill=BLACK)

        # compute pen position (where FreeType would place glyph pen)
        # center the glyph's advance horizontally inside the inner width
        pen_x = inner_x + (inner_w - g['advance']) / 2.0

        # bitmap draw position:
        # x_bitmap = pen_x + bitmap_left
        x_bitmap = int(round(pen_x + g['bitmap_left']))

        # y: baseline is at inner_y + max_above; the glyph bitmap top should be at baseline - bitmap_top
        baseline_y = inner_y + max_above
        y_bitmap = int(round(baseline_y - g['bitmap_top']))

        # Only paste if there is a bitmap (some glyphs like space have zero mask)
        if g['width'] > 0 and g['rows'] > 0 and g['buffer']:
            # create mask from freetype buffer (L mode)
            mask = Image.frombytes('L', (g['width'], g['rows']), g['buffer'])
            # paste white glyph using mask onto sheet
            sheet.paste(WHITE, (x_bitmap, y_bitmap), mask)

    if not output_path.lower().endswith('.png'):
        output_path += '.png'
    sheet.save(output_path)
    print(f"Saved spritesheet to {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Spritesheet gen")
    parser.add_argument("ttf", help="Path to TTF font file")
    parser.add_argument("--size", type=int, default=64, help="Font pixel size")
    parser.add_argument("--output", type=str, default="spritesheet.png", help="Output PNG")
    parser.add_argument("--cols", type=int, default=16, help="Columns in grid")
    args = parser.parse_args()

    render_font_spritesheet_freetype(args.ttf, args.size, args.output, cols=args.cols)
