#!/usr/bin/env python3
"""SOLARFLASH SF-1 — catalogue photograph of an impossible gadget.

A solar-powered torch that only works in daylight. Drawn entirely with
PIL: studio backdrop, soft shadow, the torch (gunmetal body, solar panel,
silver bezel, glowing lens), a beam spilling out of frame to the right,
and exactly one accessory — the sunglasses you need to use it.
Deterministic, no network, no randomness.
"""
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1024, 1024

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
F_BOLD = ImageFont.truetype(f"{FONT_DIR}/DejaVuSans-Bold.ttf", 54)
F_SPEC = ImageFont.truetype(f"{FONT_DIR}/DejaVuSans.ttf", 30)
F_SMALL = ImageFont.truetype(f"{FONT_DIR}/DejaVuSans.ttf", 24)
F_BODY = ImageFont.truetype(f"{FONT_DIR}/DejaVuSans-Bold.ttf", 22)
F_TAG = ImageFont.truetype(f"{FONT_DIR}/DejaVuSans-Bold.ttf", 20)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def backdrop():
    """Soft studio gradient: warm light grey at top to near-white floor."""
    img = Image.new("RGB", (W, H))
    px = img.load()
    for y in range(H):
        t = y / (H - 1)
        c = lerp((232, 231, 226), (250, 249, 246), t)
        for x in range(W):
            px[x, y] = c
    # faint radial light behind the product
    glow = Image.new("L", (W, H), 0)
    gd = ImageDraw.Draw(glow)
    gd.ellipse([180, 180, 900, 780], fill=26)
    glow = glow.filter(ImageFilter.GaussianBlur(140))
    img = Image.composite(Image.new("RGB", (W, H), (255, 255, 252)), img, glow)
    return img


def rounded(draw, box, radius, **kw):
    draw.rounded_rectangle(box, radius=radius, **kw)


def draw_shadow(img):
    """Soft contact shadow under torch and sunglasses."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse([205, 505, 845, 545], fill=(60, 58, 52, 110))
    d.ellipse([295, 700, 505, 728], fill=(60, 58, 52, 90))
    layer = layer.filter(ImageFilter.GaussianBlur(10))
    img.alpha_composite(layer)


def draw_beam(img):
    """Warm beam cone from the lens, fading to the right edge."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x0, y0 = 838, 436  # lens centre
    # cone widening to the right edge
    steps = 90
    for i in range(steps):
        x = x0 + (W - x0) * i / steps
        half = 10 + (115 - 10) * i / steps
        alpha = int(200 * (1 - i / steps) ** 1.2)
        d.rectangle([x, y0 - half, x + 3, y0 + half],
                    fill=(255, 206, 100, alpha))
    # hot glow at the lens
    for r in range(52, 0, -1):
        a = int(200 * (1 - r / 52))
        d.ellipse([x0 - r, y0 - r, x0 + r, y0 + r],
                  fill=(255, 230, 150, a))
    layer = layer.filter(ImageFilter.GaussianBlur(3))
    img.alpha_composite(layer)


def draw_torch(img):
    d = ImageDraw.Draw(img, "RGBA")
    # body: gunmetal cylinder with top highlight and bottom shade
    body = [200, 380, 760, 492]
    rounded(d, body, 55, fill=(52, 56, 62, 255))
    rounded(d, [200, 380, 760, 408], 55, fill=(88, 94, 102, 255))
    rounded(d, [200, 380, 760, 392], 55, fill=(120, 126, 134, 255))
    rounded(d, [200, 470, 760, 492], 55, fill=(30, 32, 36, 255))
    # tail cap ring
    rounded(d, [200, 380, 232, 492], 28, fill=(38, 41, 46, 255))
    d.rectangle([226, 380, 236, 492], fill=(150, 155, 162, 255))
    # power button on top
    d.ellipse([300, 366, 332, 384], fill=(178, 182, 188, 255))
    d.ellipse([306, 370, 326, 380], fill=(196, 40, 32, 255))
    # solar panel on top of the body
    panel = [380, 352, 700, 380]
    d.rectangle(panel, fill=(24, 38, 66, 255))
    for cx in range(380, 700, 40):
        d.line([cx, 352, cx, 380], fill=(120, 150, 200, 255), width=2)
    d.line([380, 366, 700, 366], fill=(120, 150, 200, 255), width=2)
    d.rectangle(panel, outline=(200, 210, 225, 255), width=2)
    # mounting brackets joining the panel to the body
    d.rectangle([420, 380, 436, 392], fill=(60, 64, 70, 255))
    d.rectangle([644, 380, 660, 392], fill=(60, 64, 70, 255))
    # brand on the body
    d.text((420, 424), "SOLARFLASH", font=F_BODY, fill=(235, 236, 238, 255))
    d.text((640, 428), "SF-1", font=F_BODY, fill=(170, 174, 180, 255))
    # bezel: tapered silver head
    d.polygon([(760, 372), (838, 392), (838, 480), (760, 500)],
              fill=(196, 200, 205, 255))
    d.polygon([(760, 372), (838, 392), (838, 410), (760, 392)],
              fill=(225, 228, 232, 255))
    d.polygon([(760, 480), (838, 462), (838, 480), (760, 500)],
              fill=(150, 154, 160, 255))
    # lens ring + glass
    d.ellipse([822, 396, 862, 476], fill=(140, 144, 150, 255))
    d.ellipse([826, 400, 858, 472], fill=(255, 246, 210, 255))
    d.ellipse([832, 408, 852, 464], fill=(255, 255, 240, 255))


def draw_sunglasses(img):
    """Exactly one accessory: dark sunglasses, slightly angled."""
    d = ImageDraw.Draw(img, "RGBA")
    # temples, angled gently outwards
    d.line([310, 652, 272, 640], fill=(70, 70, 74, 255), width=8)
    d.line([478, 652, 516, 640], fill=(70, 70, 74, 255), width=8)
    # lenses, larger and framed so they read as sunglasses
    d.rounded_rectangle([292, 640, 392, 716], radius=34,
                        fill=(30, 30, 34, 255),
                        outline=(120, 122, 126, 255), width=4)
    d.rounded_rectangle([396, 640, 496, 716], radius=34,
                        fill=(30, 30, 34, 255),
                        outline=(120, 122, 126, 255), width=4)
    # bridge
    d.line([392, 672, 396, 672], fill=(70, 70, 74, 255), width=8)
    # glints
    d.line([306, 654, 344, 654], fill=(205, 210, 215, 255), width=5)
    d.line([410, 654, 448, 654], fill=(205, 210, 215, 255), width=5)


def draw_text(img):
    d = ImageDraw.Draw(img, "RGBA")
    cx = W // 2
    # catalogue header, small and quiet
    tag = "LUMEN  ·  STUDIO CATALOGUE 2026"
    bb = d.textbbox((0, 0), tag, font=F_TAG)
    d.text((cx - (bb[2] - bb[0]) // 2, 92), tag, font=F_TAG,
           fill=(120, 118, 112, 255))
    # product name
    name = "SOLARFLASH SF-1"
    bb = d.textbbox((0, 0), name, font=F_BOLD)
    d.text((cx - (bb[2] - bb[0]) // 2, 780), name, font=F_BOLD,
           fill=(38, 38, 36, 255))
    # spec lines — product text, never an explanation of the joke
    specs = [
        "Solar-powered torch  ·  works only in daylight",
        "0 lumens after sunset  ·  no batteries, ever",
    ]
    y = 856
    for line in specs:
        bb = d.textbbox((0, 0), line, font=F_SPEC)
        d.text((cx - (bb[2] - bb[0]) // 2, y), line, font=F_SPEC,
               fill=(96, 94, 90, 255))
        y += 42
    price = "£49.99"
    bb = d.textbbox((0, 0), price, font=F_SMALL)
    d.text((cx - (bb[2] - bb[0]) // 2, 946), price, font=F_SMALL,
           fill=(38, 38, 36, 255))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    img = backdrop().convert("RGBA")
    draw_shadow(img)
    draw_beam(img)
    draw_torch(img)
    draw_sunglasses(img)
    draw_text(img)
    img.convert("RGB").save(os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
