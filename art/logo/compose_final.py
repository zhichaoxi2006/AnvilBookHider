#!/usr/bin/env python3
"""Anvil Book Hider logo - flat vanilla style (final composition).

* anvil: hand-built pixel sprite using the vanilla anvil texture's palette,
  front view with horn / waist / plinth, dark outline + bevel.
* enchanted book: textures/item/enchanted_book.png at 18x nearest.
* barrier: textures/item/barrier.png as the prohibition frame.

Camera-flat layout, no perspective trickery: the book is the banned subject,
the anvil is the context, the barrier is the verdict.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

TEX = Path(__file__).resolve().parent / "tex"
OUT = Path(__file__).resolve().parent
S = 1024

BOOK = Image.open(TEX / "enchanted_book.png").convert("RGBA")
BARRIER = Image.open(TEX / "barrier.png").convert("RGBA")

# palette sampled from textures/block/anvil.png (dark stone greys)
OUTLINE = (14, 15, 21)
G1 = (44, 46, 52)    # shadow
G2 = (62, 65, 72)    # base tone
G3 = (82, 86, 94)    # mid
G4 = (108, 112, 121) # light
G5 = (140, 145, 155) # highlight


# ----------------------------------------------------------------- anvil
# Vanilla anvil block model, straight out of
# assets/minecraft/models/block/template_anvil.json:
# element boxes + the per-face UV rectangles of the real model.
#   (from, to, {face: (u0, v0, u1, v1)})
ANVIL_MODEL = [
    ((2, 0, 2), (14, 4, 14), {
        "up": (2, 2, 14, 14), "south": (2, 12, 14, 16), "east": (4, 2, 0, 14)}),
    ((4, 4, 3), (12, 5, 13), {
        "up": (4, 3, 12, 13), "south": (4, 11, 12, 12), "east": (5, 3, 4, 13)}),
    ((6, 5, 4), (10, 10, 12), {
        "up": (6, 4, 10, 12), "south": (6, 6, 10, 11), "east": (10, 4, 5, 12)}),
    ((3, 10, 0), (13, 16, 16), {
        "up": (3, 0, 13, 16), "south": (3, 0, 13, 6), "east": (16, 0, 10, 16)}),
]
ANVIL_TEX = Image.open(TEX / "anvil.png").convert("RGBA")
TOP_TEX = Image.open(TEX / "anvil_top.png").convert("RGBA")
COS30, SIN30 = 0.8660254, 0.5


ELEV_Y = 1.12   # vertical exaggeration: a lower camera reveals the anvil waist
DEPTH = 0.42


def _proj(x, y, z, unit):
    """Y-up isometric-ish projection, tuned so the anvil's waist stays visible."""
    return ((x - z) * COS30 * unit, (x + z) * DEPTH * unit - y * ELEV_Y * unit)


def _affine_uv(canvas, tex, quad, uvs, shade, bright=1.0):
    """Fill quad (tl,tr,br,bl) by affine-mapping the uvs (one per corner)."""
    p0, p1, p2, p3 = quad
    (u0, v0), (u1, v1), (u2, v2), (u3, v3) = uvs
    # build M mapping (u,v)->(x,y) about p0, using the tr and bl corners
    ax, ay = p1[0] - p0[0], p1[1] - p0[1]
    bx, by = p3[0] - p0[0], p3[1] - p0[1]
    dux, dvy = u1 - u0, v3 - v0
    if abs(dux) < 1e-9 or abs(dvy) < 1e-9:
        return
    M = np.array([[ax / dux, bx / dvy], [ay / dux, by / dvy]], dtype=np.float64)
    if abs(np.linalg.det(M)) < 1e-9:
        return
    Mi = np.linalg.inv(M)
    xs = [q[0] for q in quad]
    ys = [q[1] for q in quad]
    x0, x1 = max(0, int(min(xs)) - 1), min(canvas.shape[1] - 1, int(max(xs)) + 2)
    y0, y1 = max(0, int(min(ys)) - 1), min(canvas.shape[0] - 1, int(max(ys)) + 2)
    if x1 <= x0 or y1 <= y0:
        return
    gx, gy = np.meshgrid(np.arange(x0, x1 + 1) - p0[0], np.arange(y0, y1 + 1) - p0[1])
    u = Mi[0, 0] * gx + Mi[0, 1] * gy + u0
    v = Mi[1, 0] * gx + Mi[1, 1] * gy + v0
    inside = (u >= min(u0, u2) - 1e-6) & (u <= max(u0, u2) + 1e-6) & \
             (v >= min(v0, v2) - 1e-6) & (v <= max(v0, v2) + 1e-6)
    if not inside.any():
        return
    tw, th = tex.size
    tx = np.clip(u.round().astype(int), 0, tw - 1)
    ty = np.clip(v.round().astype(int), 0, th - 1)
    src = np.asarray(tex, dtype=np.float64)[ty, tx]
    src[..., :3] = np.clip(src[..., :3] * shade * bright, 0, 255)
    a = (src[..., 3:4] / 255.0) * inside[..., None]
    dst = canvas[y0:y1 + 1, x0:x1 + 1].astype(np.float64)
    da = dst[..., 3:4] / 255.0
    oa = a + da * (1 - a)
    rgb = (src[..., :3] * a + dst[..., :3] * da * (1 - a)) / np.maximum(oa, 1e-6)
    canvas[y0:y1 + 1, x0:x1 + 1] = np.clip(
        np.concatenate([rgb, oa * 255], axis=2), 0, 255).astype(np.uint8)


def render_anvil(unit: float = 14.2, pad: int = 4, bright: float = 1.62) -> Image.Image:
    """Isometric render of the vanilla anvil block model, cropped to its bounds."""
    def P(x, y, z):
        return _proj(x, y, z, unit)

    parts = []
    for (fx, fy, fz), (tx, ty, tz), uv in ANVIL_MODEL:
        top = [P(fx, ty, fz), P(tx, ty, fz), P(tx, ty, tz), P(fx, ty, tz)]
        south = [P(fx, ty, tz), P(tx, ty, tz), P(tx, fy, tz), P(fx, fy, tz)]
        east = [P(tx, ty, fz), P(tx, ty, tz), P(tx, fy, tz), P(tx, fy, fz)]
        parts.append((top, south, east, uv))

    pts = [p for t, s, e, _ in parts for p in (t + s + e)]
    minx, maxx = min(p[0] for p in pts), max(p[0] for p in pts)
    miny, maxy = min(p[1] for p in pts), max(p[1] for p in pts)
    w, h = int(maxx - minx) + pad * 2, int(maxy - miny) + pad * 2
    canvas = np.zeros((h, w, 4), dtype=np.uint8)

    for top, south, east, uv in parts:
        def T(quad):
            return [(x - minx + pad, y - miny + pad) for x, y in quad]

        # up face
        u0, v0, u1, v1 = uv["up"]
        tex = TOP_TEX if (u0, v0, u1, v1) == (3, 0, 13, 16) else ANVIL_TEX
        _affine_uv(canvas, tex, T(top),
                   [(u0, v0), (u1, v0), (u1, v1), (u0, v1)], 1.0, bright)
        # east side
        u0, v0, u1, v1 = uv["east"]
        _affine_uv(canvas, ANVIL_TEX, T(east),
                   [(u0, v0), (u1, v0), (u1, v1), (u0, v1)], 0.62, bright)
        # south side (the front view of the anvil drawing)
        u0, v0, u1, v1 = uv["south"]
        _affine_uv(canvas, ANVIL_TEX, T(south),
                   [(u0, v0), (u1, v0), (u1, v1), (u0, v1)], 0.86, bright)
    return Image.fromarray(canvas, "RGBA")


def up(img: Image.Image, k: int) -> Image.Image:
    return img.resize((img.width * k, img.height * k), Image.NEAREST)


def backdrop() -> Image.Image:
    img = Image.new("RGBA", (S, S), (16, 15, 26, 255))
    d = ImageDraw.Draw(img)
    for i in range(0, 1024, 64):
        t = i / 1023
        c = (int(56 * (1 - t) + 13 * t), int(50 * (1 - t) + 11 * t), int(92 * (1 - t) + 23 * t))
        d.rectangle([0, i, S, i + 64], fill=(*c, 255))
    g = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    gd = ImageDraw.Draw(g)
    gd.ellipse([80, 520, 944, 1140], fill=(255, 118, 38, 100))
    gd.ellipse([220, 620, 804, 1060], fill=(255, 170, 80, 70))
    img.alpha_composite(g.filter(ImageFilter.GaussianBlur(80)))
    b = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    bd = ImageDraw.Draw(b)
    bd.ellipse([150, 30, 874, 754], fill=(148, 98, 255, 105))
    img.alpha_composite(b.filter(ImageFilter.GaussianBlur(64)))
    m = Image.new("L", (S, S), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, S - 1, S - 1], radius=224, fill=255)
    out = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    out.paste(img, (0, 0), m)
    ImageDraw.Draw(out).rounded_rectangle([6, 6, S - 7, S - 7], radius=220,
                                          outline=(255, 255, 255, 26), width=4)
    return out


def compose(ring_scale=40, ring_y=26, book_k=21, anvil_unit=14.2,
            anvil_pos=(350, 592), book_pos=(344, 116)) -> Image.Image:
    img = backdrop()
    ring = up(BARRIER, ring_scale)
    ring_pos = (S // 2 - ring.width // 2, ring_y)

    # --- paint order: book first, then the barrier over it, then the anvil ---
    bk = up(BOOK, book_k)
    bx, by = book_pos
    # layered aura: wide violet bloom + tight cyan core
    g = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    gd = ImageDraw.Draw(g)
    gd.ellipse([bx - 50, by - 50, bx + bk.width + 50, by + bk.height + 50],
               fill=(168, 118, 255, 120))
    img.alpha_composite(g.filter(ImageFilter.GaussianBlur(34)))
    img.alpha_composite(bk, (bx, by))

    # barrier sits ON TOP of the enchanted book: the ring edge clips the book's
    # corners and the slash crosses the sprite. Slight alpha keeps it readable.
    bar = ring.copy()
    bar.putalpha(bar.getchannel("A").point(lambda v: int(v * 0.90)))
    img.alpha_composite(bar, ring_pos)

    anvil = render_anvil(unit=anvil_unit)
    ax, ay = anvil_pos
    sh = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ImageDraw.Draw(sh).ellipse([ax + 10, ay + anvil.height - 40, ax + anvil.width - 10,
                                ay + anvil.height + 20], fill=(0, 0, 0, 135))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(18)))
    img.alpha_composite(anvil, (ax, ay))

    # gentle corner vignette
    v = Image.new("RGBA", (S, S), (7, 5, 14, 255))
    mask = Image.new("L", (S, S), 0)
    ImageDraw.Draw(mask).ellipse([-120, -120, S + 120, S + 120], fill=255)
    mask = Image.eval(mask.filter(ImageFilter.GaussianBlur(140)), lambda v: 255 - v)
    mask = Image.eval(mask, lambda v: int(v * 0.45))
    img.alpha_composite(Image.composite(v, Image.new("RGBA", (S, S), (0, 0, 0, 0)), mask))
    return img


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    im = compose()
    im.save(OUT / "logo-1024.png")
    for s in (512, 256, 128, 64):
        im.resize((s, s), Image.LANCZOS).save(OUT / f"logo-{s}.png")
    print("done")
