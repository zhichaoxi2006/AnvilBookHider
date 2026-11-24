#!/usr/bin/env python3
"""Anvil Book Hider - wide banner (Modrinth / CurseForge / GitHub social).

Reuses the finished square logo and lays it out with a bilingual wordmark.
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUT = Path(__file__).resolve().parent
LOGO = OUT / "logo-1024.png"

W, H = 1280, 720
FONT_EN = r"C:\Windows\Fonts\segoeuib.ttf"
FONT_EN_R = r"C:\Windows\Fonts\segoeui.ttf"
FONT_SC = r"C:\Windows\Fonts\NotoSansSC-VF.ttf"


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def background() -> Image.Image:
    img = Image.new("RGBA", (W, H), (13, 12, 22, 255))
    d = ImageDraw.Draw(img)
    for i in range(0, H, 8):
        t = i / (H - 1)
        c = (int(46 * (1 - t) + 12 * t), int(40 * (1 - t) + 11 * t), int(78 * (1 - t) + 20 * t))
        d.rectangle([0, i, W, i + 8], fill=(*c, 255))
    g = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(g)
    gd.ellipse([-60, 40, 640, 760], fill=(140, 90, 255, 120))
    gd.ellipse([120, 300, 700, 820], fill=(255, 120, 40, 80))
    img.alpha_composite(g.filter(ImageFilter.GaussianBlur(90)))
    for y in range(0, H, 32):
        for x in range(0, W, 32):
            if ((x // 32) * 7 + (y // 32) * 11) % 13 == 0:
                d.rectangle([x, y, x + 3, y + 3], fill=(255, 255, 255, 10))
    return img


def build() -> Image.Image:
    img = background()
    logo = Image.open(LOGO).convert("RGBA").resize((470, 470), Image.LANCZOS)
    img.alpha_composite(logo, (60, 125))

    d = ImageDraw.Draw(img)
    tx = 570
    title = font(FONT_EN, 62)
    sub = font(FONT_EN_R, 29)
    sc = font(FONT_SC, 29)
    chip_font = font(FONT_EN_R, 21)

    d.text((tx, 200), "Anvil Book Hider", font=title, fill=(246, 243, 255, 255))
    d.rectangle([tx + 4, 288, tx + 4 + 320, 295], fill=(240, 65, 79, 255))

    d.text((tx + 4, 330), "Hides configured enchantments", font=sub, fill=(206, 198, 240, 255))
    d.text((tx + 4, 372), "from the anvil display in JEI", font=sub, fill=(206, 198, 240, 255))
    d.text((tx + 4, 452), "把指定的附魔从 JEI 的铁砧配方中隐藏", font=sc, fill=(176, 166, 212, 255))

    chips = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(chips)
    x = tx + 4
    for label in ("NeoForge 1.21.1", "JEI 19.x", "Client-side"):
        bb = d.textbbox((0, 0), label, font=chip_font)
        w = bb[2] - bb[0] + 36
        cd.rounded_rectangle([x, 540, x + w, 590], radius=10, fill=(255, 255, 255, 16),
                             outline=(255, 255, 255, 30), width=2)
        cd.text((x + 18, 553), label, font=chip_font, fill=(216, 208, 246, 255))
        x += w + 14
    img.alpha_composite(chips)

    d.rounded_rectangle([0, 0, W - 1, H - 1], radius=0, outline=(255, 255, 255, 18), width=3)
    return img


if __name__ == "__main__":
    im = build()
    im.convert("RGB").save(OUT / "banner-1280x720.png")
    print("done")
