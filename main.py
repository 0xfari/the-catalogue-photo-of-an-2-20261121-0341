#!/usr/bin/env python3
"""SOLARFLASH SF-1 — catalogue photograph of an impossible gadget.

A solar-powered torch that only works in daylight. Drawn as a clean studio
catalogue shot: gunmetal torch, glowing lens, warm beam spilling out of
frame, navy solar panel on its back, red power button, and one accessory —
the sunglasses you need to use it.

Deterministic, no network, no randomness. Writes entry.png to
MAKEFUN_OUTPUT_DIR (or /output).
"""

import os

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W = H = 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def vertical_gradient(size, top, bottom):
    img = Image.new("RGB", size)
    d = ImageDraw.Draw(img)
    w, h = size
    for y in range(h):
        d.line([(0, y), (w, y)], fill=lerp(top, bottom, y / max(h - 1, 1)))
    return img


def soft_ellipse(layer, box, fill, blur):
    tmp = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    ImageDraw.Draw(tmp).ellipse(box, fill=fill)
    tmp = tmp.filter(ImageFilter.GaussianBlur(blur))
    layer.alpha_composite(tmp)


def rounded(draw, box, radius, **kw):
    draw.rounded_rectangle(box, radius=radius, **kw)


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)

    # --- studio backdrop: pale grey gradient, slightly darker at the floor.
    img = vertical_gradient((W, H), (243, 244, 245), (214, 217, 220))
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)

    # --- floor shadow under the torch and under the sunglasses.
    soft_ellipse(overlay, (150, 560, 830, 610), (60, 64, 70, 90), 18)
    soft_ellipse(overlay, (600, 712, 900, 742), (60, 64, 70, 80), 14)

    # --- warm beam spilling out of the right edge, from the lens.
    beam = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(beam)
    bd.polygon([(812, 452), (1024, 380), (1024, 620), (812, 548)],
               fill=(255, 196, 90, 150))
    bd.polygon([(812, 470), (1024, 430), (1024, 570), (812, 530)],
               fill=(255, 214, 130, 185))
    beam = beam.filter(ImageFilter.GaussianBlur(10))
    overlay.alpha_composite(beam)
    # hot core of the beam right at the lens, plus a soft halo around it
    soft_ellipse(overlay, (790, 440, 900, 560), (255, 226, 150, 170), 22)
    soft_ellipse(overlay, (748, 408, 872, 592), (255, 210, 110, 70), 30)

    # --- torch body: gunmetal, horizontal, head on the right.
    body = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bdd = ImageDraw.Draw(body)
    rounded(bdd, (180, 440, 800, 560), radius=58, fill=(74, 80, 88, 255))
    rounded(bdd, (180, 440, 800, 500), radius=58, fill=(96, 103, 112, 255))
    # top highlight strip and bottom shade for a manufactured look
    rounded(bdd, (200, 448, 780, 466), radius=9, fill=(150, 158, 168, 255))
    rounded(bdd, (200, 534, 780, 552), radius=9, fill=(52, 57, 64, 255))
    # grip rings near the tail
    for x in (232, 258, 284):
        bdd.rectangle((x, 442, x + 10, 558), fill=(58, 63, 71, 255))
    # tail cap
    rounded(bdd, (180, 452, 214, 548), radius=16, fill=(60, 65, 73, 255))
    overlay.alpha_composite(body)

    # --- solar panel on the back of the body, on a small bracket.
    panel = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pd = ImageDraw.Draw(panel)
    pd.rectangle((330, 428, 352, 446), fill=(52, 57, 64, 255))  # bracket
    pd.rectangle((540, 428, 562, 446), fill=(52, 57, 64, 255))  # bracket
    rounded(pd, (300, 372, 592, 432), radius=10,
            fill=(24, 42, 84, 255), outline=(150, 158, 168, 255), width=3)
    for x in range(348, 592, 48):  # panel grid, vertical
        pd.line([(x, 376), (x, 428)], fill=(120, 140, 190, 255), width=2)
    for y in (392, 412):  # panel grid, horizontal
        pd.line([(304, y), (588, y)], fill=(120, 140, 190, 255), width=2)
    # sun glint on the panel
    pd.polygon([(320, 376), (380, 376), (340, 428), (304, 428)],
               fill=(90, 120, 180, 90))
    overlay.alpha_composite(panel)

    # --- red power button on top of the body.
    btn = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    btd = ImageDraw.Draw(btn)
    btd.ellipse((636, 420, 672, 444), fill=(178, 34, 34, 255),
                outline=(120, 18, 18, 255), width=2)
    btd.ellipse((644, 424, 660, 434), fill=(226, 90, 90, 255))
    overlay.alpha_composite(btn)

    # --- head: silver bezel ring + glowing lens.
    head = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(head)
    rounded(hd, (768, 428, 846, 572), radius=24,
            fill=(196, 200, 206, 255), outline=(140, 146, 154, 255), width=3)
    hd.ellipse((792, 448, 838, 552), fill=(255, 240, 190, 255),
               outline=(255, 214, 120, 255), width=4)
    hd.ellipse((802, 462, 828, 538), fill=(255, 252, 235, 255))
    overlay.alpha_composite(head)

    # --- the one accessory: sunglasses, resting below the torch.
    acc = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ad = ImageDraw.Draw(acc)
    rounded(ad, (620, 648, 748, 706), radius=22, fill=(22, 22, 24, 255))
    rounded(ad, (772, 648, 900, 706), radius=22, fill=(22, 22, 24, 255))
    ad.line([(748, 668), (772, 668)], fill=(22, 22, 24, 255), width=10)
    ad.line([(620, 660), (596, 640)], fill=(22, 22, 24, 255), width=8)
    ad.line([(900, 660), (924, 640)], fill=(22, 22, 24, 255), width=8)
    # lens glints
    ad.line([(648, 700), (700, 656)], fill=(120, 130, 145, 255), width=5)
    ad.line([(800, 700), (852, 656)], fill=(120, 130, 145, 255), width=5)
    overlay.alpha_composite(acc)

    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    d = ImageDraw.Draw(img)

    # --- catalogue typography (DejaVu). Text belongs to the product only.
    f_head = font("DejaVuSans.ttf", 30)
    f_name = font("DejaVuSans-Bold.ttf", 64)
    f_spec = font("DejaVuSans.ttf", 30)
    f_price = font("DejaVuSans-Bold.ttf", 44)

    d.text((64, 52), "L U M E N   ·   S T U D I O   C A T A L O G U E   2 0 2 6",
           font=f_head, fill=(90, 94, 100))
    d.line([(64, 100), (960, 100)], fill=(150, 155, 160), width=2)
    d.text((64, 812), "SOLARFLASH SF-1", font=f_name, fill=(38, 42, 48))
    d.text((64, 890), "Solar-powered torch · works only in daylight",
           font=f_spec, fill=(80, 84, 90))
    d.text((64, 928), "0 lumens after sunset · no batteries, ever",
           font=f_spec, fill=(80, 84, 90))
    d.text((800, 812), "£49.99", font=f_price, fill=(38, 42, 48))

    img.save(os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
