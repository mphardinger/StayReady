"""Generate Stay Ready PWA app icons (a carrot on brand green).

Run once to (re)produce the PNGs referenced by manifest.json / index.html:
    python make_icons.py
Output goes to static/icons/.
"""
import math
import os

from PIL import Image, ImageDraw

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'icons')
os.makedirs(OUT, exist_ok=True)

GREEN = (47, 97, 64)        # --green-dark
GREEN_HI = (62, 124, 79)    # --green
ORANGE = (232, 93, 61)      # --tomato
ORANGE_HI = (242, 140, 100)
LEAF = (120, 170, 95)


def _draw_carrot(draw, cx, cy, scale):
    """Carrot body (tapered) + three leaves, centered on (cx, cy)."""
    # Body: a downward-tapering shape (wide top, pointed bottom).
    top = cy - 1.4 * scale
    bottom = cy + 2.3 * scale
    half = 1.05 * scale
    body = [
        (cx - half, top),
        (cx + half, top),
        (cx + half * 0.55, cy + 0.4 * scale),
        (cx, bottom),
        (cx - half * 0.55, cy + 0.4 * scale),
    ]
    draw.polygon(body, fill=ORANGE)
    # Highlight down the left side for a little depth.
    hi = [
        (cx - half, top),
        (cx - half * 0.35, top),
        (cx - half * 0.1, cy + 0.4 * scale),
        (cx, bottom),
        (cx - half * 0.55, cy + 0.4 * scale),
    ]
    draw.polygon(hi, fill=ORANGE_HI)
    # Little ridges (dashes) across the body.
    for i, t in enumerate((-0.7, 0.0, 0.7, 1.4)):
        w = half * (1 - (t + 1.4) / 4.6) * 0.7
        y = top + (t + 1.4) / 3.7 * (bottom - top) * 0.72 + 0.35 * scale
        draw.line([(cx - w, y), (cx + w, y - 0.08 * scale)], fill=ORANGE_HI, width=max(2, int(scale * 0.12)))
    # Leaves: three overlapping ellipses fanning up from the top.
    for ang, size in ((-38, 1.0), (0, 1.25), (38, 1.0)):
        a = math.radians(ang)
        lx = cx + math.sin(a) * 0.9 * scale
        ly = top - math.cos(a) * 0.5 * scale
        w, hgt = 0.55 * scale * size, 1.15 * scale * size
        leaf = Image.new('RGBA', (int(w * 2) + 4, int(hgt * 2) + 4), (0, 0, 0, 0))
        ld = ImageDraw.Draw(leaf)
        ld.ellipse([2, 2, w * 2, hgt * 2], fill=LEAF)
        leaf = leaf.rotate(ang, expand=True, resample=Image.BICUBIC)
        draw._image.paste(leaf, (int(lx - leaf.width / 2), int(ly - leaf.height * 0.72)), leaf)


def make(size, pad_ratio, rounded, name):
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw._image = img
    inset = int(size * pad_ratio)
    box = [inset, inset, size - inset, size - inset]
    if rounded:
        radius = int((size - 2 * inset) * 0.22)
        draw.rounded_rectangle(box, radius=radius, fill=GREEN)
    else:
        draw.rectangle(box, fill=GREEN)
    # Subtle top glow.
    glow = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([inset, inset - size * 0.25, size - inset, size * 0.55],
               fill=GREEN_HI + (90,))
    img.alpha_composite(glow)
    scale = (size - 2 * inset) / 7.0
    _draw_carrot(draw, size / 2, size / 2 - scale * 0.2, scale)
    img.save(os.path.join(OUT, name))
    print('wrote', name, size)


# Standard icons (small transparent margin), maskable (big safe-zone padding),
# and an opaque Apple touch icon (iOS ignores transparency / applies its own mask).
make(192, 0.0, True, 'icon-192.png')
make(512, 0.0, True, 'icon-512.png')
make(512, 0.16, False, 'icon-maskable-512.png')
make(180, 0.0, False, 'apple-touch-icon.png')
print('done')
