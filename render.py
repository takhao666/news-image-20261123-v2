#!/usr/bin/env python3
"""Render the 23 November 2026 world-news front page to entry.png.

Deterministic, offline, stdlib + Pillow. Run:  python3 render.py
Writes entry.png (1024x1024) next to this file.

News selection (each item verified against at least two independent
reports dated 22-23 Nov 2026; see README.md for the source list):
  1. COP31 climate talks collapse in Antalya (UN News, Reuters, CNN)
  2. Tankers struck in the Strait of Hormuz (CNN, IRNA, Al Jazeera)
  3. War spills over: Dymer flats hit near Kyiv; Russian ships hit
     off Finland and at Benghazi, Libya (Reuters, AP, Al Jazeera, CNN)
  4. Indonesia candy-factory fire, Banten (AP, Al Jazeera, CNA)
  5. Mexico captures cartel boss 'El Chapo Isidro' (AP, Japan Times)
  6. South Korea education minister quits over AI cheating (Yonhap, CNA)
  7. Nepal PM Balendra Shah meets PM Modi in Delhi, Mon 23 Nov
     (The Hindu, Times of India)
  Ticker: BepiColombo reaches Mercury (ESA); Peru 6.7 quake, 1 dead;
     Nigeria funeral boat capsizes, 24 dead.
"""
import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (17, 17, 17)
WHITE = (255, 255, 255)
RED = (178, 34, 34)
TEAL = (0, 110, 105)
ORANGE = (196, 88, 16)
BLUE = (24, 74, 150)
DARK = (38, 38, 38)
GREY = (90, 86, 78)

F_SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
F_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
F_SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
F_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap using real text widths."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit(draw, text, fnt_path, size, width):
    """Shrink font until text fits width (never below 10)."""
    while size > 10:
        f = font(fnt_path, size)
        if draw.textlength(text, font=f) <= width:
            return f
        size -= 1
    return font(fnt_path, 10)


def globe(d, cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(58, 130, 190),
              outline=INK, width=3)
    # land blobs
    d.ellipse([cx - r + 14, cy - r + 22, cx - r + 66, cy - r + 62],
              fill=(72, 150, 80))
    d.ellipse([cx - 6, cy + 6, cx + r - 12, cy + r - 26], fill=(72, 150, 80))
    d.ellipse([cx + r - 52, cy - r + 30, cx + r - 8, cy - r + 66],
              fill=(72, 150, 80))
    # crack: no deal
    d.line([cx - r + 18, cy - r + 70, cx + r - 30, cy + r - 44],
           fill=RED, width=5)
    d.line([cx - r + 40, cy + r - 30, cx - r + 66, cy + 8],
           fill=RED, width=4)


def tanker(d, x, y, s):
    # hull
    d.polygon([(x, y + 34 * s), (x + 150 * s, y + 34 * s),
               (x + 138 * s, y + 52 * s), (x + 10 * s, y + 52 * s)],
              fill=(40, 40, 48))
    d.rectangle([x + 18 * s, y + 8 * s, x + 48 * s, y + 34 * s],
                fill=(120, 30, 30))
    d.rectangle([x + 56 * s, y + 14 * s, x + 84 * s, y + 34 * s],
                fill=(200, 160, 40))
    d.rectangle([x + 92 * s, y + 14 * s, x + 120 * s, y + 34 * s],
                fill=(200, 160, 40))
    # explosion burst
    cx, cy = x + 132 * s, y + 6 * s
    for dx, dy, r in [(0, 0, 16), (-16, -8, 10), (14, -10, 11),
                      (-12, 10, 9), (16, 8, 9), (0, -18, 9)]:
        d.ellipse([cx + dx * s - r * s, cy + dy * s - r * s,
                   cx + dx * s + r * s, cy + dy * s + r * s],
                  fill=(240, 140, 20))
    # waves
    for i in range(3):
        d.arc([x + i * 52 * s, y + 56 * s, x + (i + 1) * 52 * s, y + 72 * s],
              0, 180, fill=(58, 130, 190), width=4)


def building_hit(d, x, y, s):
    # apartment block, corner collapsed
    d.rectangle([x, y, x + 110 * s, y + 96 * s], fill=(150, 148, 140),
                outline=INK, width=2)
    d.polygon([(x + 110 * s, y), (x + 110 * s, y + 96 * s),
               (x + 78 * s, y + 96 * s), (x + 96 * s, y + 52 * s),
               (x + 82 * s, y + 30 * s)], fill=(60, 58, 52))
    for r in range(3):
        for c in range(3):
            d.rectangle([x + 10 * s + c * 26 * s, y + 10 * s + r * 28 * s,
                         x + 26 * s + c * 26 * s, y + 26 * s + r * 28 * s],
                        fill=(250, 220, 130))
    # drone
    d.ellipse([x + 128 * s, y + 6 * s, x + 148 * s, y + 26 * s],
              fill=(40, 40, 48))
    d.line([x + 120 * s, y + 2 * s, x + 156 * s, y + 2 * s], fill=INK, width=3)
    d.line([x + 120 * s, y + 30 * s, x + 156 * s, y + 30 * s], fill=INK, width=3)


def factory_fire(d, x, y, s):
    d.rectangle([x, y + 30 * s, x + 130 * s, y + 92 * s],
                fill=(140, 138, 130), outline=INK, width=2)
    for i in range(3):  # sawtooth roof
        d.polygon([(x + i * 44 * s, y + 30 * s),
                   (x + (i + 1) * 44 * s, y + 30 * s),
                   (x + (i + 1) * 44 * s, y + 12 * s)], fill=(90, 88, 82))
    d.rectangle([x + 12 * s, y + 52 * s, x + 34 * s, y + 92 * s],
                fill=(250, 220, 130))
    d.rectangle([x + 52 * s, y + 52 * s, x + 74 * s, y + 92 * s],
                fill=(250, 220, 130))
    # flame + smoke
    cx = x + 104 * s
    d.polygon([(cx - 16 * s, y + 34 * s), (cx, y - 6 * s),
               (cx + 16 * s, y + 34 * s)], fill=(240, 120, 10))
    d.polygon([(cx - 8 * s, y + 34 * s), (cx, y + 12 * s),
               (cx + 8 * s, y + 34 * s)], fill=(250, 200, 40))
    for dx, dy, r in [(-14, -18, 9), (4, -28, 11), (18, -16, 8)]:
        d.ellipse([cx + dx * s - r * s, y + dy * s - r * s,
                   cx + dx * s + r * s, y + dy * s + r * s],
                  fill=(120, 118, 112))


def badge(d, x, y, s):
    cx, cy, r = x + 60 * s, y + 42 * s, 34 * s
    pts = []
    import math
    for i in range(10):
        ang = math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.55
        pts.append((cx + rr * math.cos(ang), cy - rr * math.sin(ang)))
    d.polygon(pts, fill=(196, 150, 30), outline=INK)
    d.ellipse([cx - 14 * s, cy - 14 * s, cx + 14 * s, cy + 14 * s],
              fill=(247, 243, 234), outline=INK, width=2)
    d.text((cx, cy), "$", font=font(F_SANS_B, int(22 * s)),
           fill=INK, anchor="mm")
    # handcuff link
    d.ellipse([x + 8 * s, y + 74 * s, x + 34 * s, y + 98 * s],
              outline=INK, width=4)
    d.ellipse([x + 118 * s, y + 74 * s, x + 144 * s, y + 98 * s],
              outline=INK, width=4)
    d.line([x + 34 * s, y + 86 * s, x + 118 * s, y + 86 * s], fill=INK, width=4)


def exam_ai(d, x, y, s):
    d.rectangle([x + 14 * s, y + 4 * s, x + 96 * s, y + 96 * s],
                fill=WHITE, outline=INK, width=2)
    for i in range(4):
        d.line([x + 26 * s, y + (20 + i * 14) * s, x + 84 * s, y + (20 + i * 14) * s],
               fill=(120, 118, 112), width=3)
    d.line([x + 26 * s, y + 76 * s, x + 60 * s, y + 76 * s], fill=RED, width=4)
    # chip
    d.rectangle([x + 104 * s, y + 56 * s, x + 148 * s, y + 96 * s],
                fill=(40, 40, 48), outline=INK, width=2)
    for i in range(3):
        d.line([x + 112 * s, y + (66 + i * 10) * s, x + 140 * s, y + (66 + i * 10) * s],
               fill=(120, 200, 120), width=2)
    d.line([x + 96 * s, y + 10 * s, x + 150 * s, y + 52 * s], fill=RED, width=4)


def flags(d, x, y, s):
    # Nepal (crimson) and India (saffron/white/green) flags
    d.line([x + 16 * s, y + 6 * s, x + 16 * s, y + 96 * s], fill=INK, width=3)
    d.line([x + 96 * s, y + 6 * s, x + 96 * s, y + 96 * s], fill=INK, width=3)
    d.polygon([(x + 16 * s, y + 6 * s), (x + 66 * s, y + 20 * s),
               (x + 16 * s, y + 36 * s)], fill=(220, 20, 60))
    d.polygon([(x + 16 * s, y + 36 * s), (x + 58 * s, y + 48 * s),
               (x + 16 * s, y + 60 * s)], fill=(220, 20, 60))
    d.rectangle([x + 96 * s, y + 6 * s, x + 148 * s, y + 20 * s],
                fill=(255, 153, 51))
    d.rectangle([x + 96 * s, y + 20 * s, x + 148 * s, y + 34 * s],
                fill=WHITE, outline=INK, width=1)
    d.rectangle([x + 96 * s, y + 34 * s, x + 148 * s, y + 48 * s],
                fill=(19, 136, 8))
    d.ellipse([x + 116 * s, y + 22 * s, x + 128 * s, y + 32 * s],
              outline=(0, 0, 136), width=2)


def draw_panel(d, box, color, tag, headline, body, icon):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=WHITE, outline=(200, 194, 182), width=2)
    d.rectangle([x0, y0, x1, y0 + 7], fill=color)
    tx = x0 + 14
    ty = y0 + 16
    f_tag = font(F_SANS_B, 17)
    d.text((tx, ty), tag, font=f_tag, fill=color)
    # Icon zone: fixed 72px box at the top-right; text wraps clear of it.
    icon(d, x1 - 86, y0 + 16, 0.46)
    text_w = (x1 - x0) - 28 - 84
    f_head = font(F_SERIF_B, 25)
    lines = wrap(d, headline, f_head, text_w)
    hy = ty + 28
    for ln in lines[:2]:
        d.text((tx, hy), ln, font=f_head, fill=INK)
        hy += 29
    f_body = font(F_SANS, 18)
    blines = wrap(d, body, f_body, text_w)
    by = hy + 4
    for ln in blines[:3]:
        d.text((tx, by), ln, font=f_body, fill=(52, 50, 46))
        by += 22


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    f_kick = font(F_SANS_B, 19)
    d.text((26, 22), "THE WORLD IN ONE DAY  •  WORLD NEWS",
           font=f_kick, fill=GREY)
    f_date = fit(d, "MONDAY 23 NOVEMBER 2026", F_SERIF_B, 62, 972)
    d.text((26, 46), "MONDAY 23 NOVEMBER 2026", font=f_date, fill=INK)
    d.rectangle([26, 118, 998, 123], fill=RED)
    d.rectangle([26, 127, 998, 129], fill=INK)

    # ---- lead story: COP31 ----
    lx0, ly0, lx1, ly1 = 26, 140, 998, 352
    d.rectangle([lx0, ly0, lx1, ly1], fill=WHITE,
                outline=(200, 194, 182), width=2)
    d.rectangle([lx0, ly0, lx1, ly0 + 7], fill=TEAL)
    d.text((46, 158), "CLIMATE  •  ANTALYA", font=font(F_SANS_B, 20),
           fill=TEAL)
    f_lead = font(F_SERIF_B, 52)
    d.text((46, 186), "COP31 COLLAPSES", font=f_lead, fill=INK)
    f_dek = font(F_SANS, 23)
    dek = ("Nearly 200 nations leave Antalya with no climate pact — "
           "fossil-fuel wording blocked the deal.")
    for i, ln in enumerate(wrap(d, dek, f_dek, 680)):
        d.text((46, 252 + i * 29), ln, font=f_dek, fill=(52, 50, 46))
    d.text((46, 318), "UN chief: “deeply disappointed” — the longest COP on record",
           font=font(F_SERIF, 20), fill=GREY)
    globe(d, 840, 250, 82)
    # NO DEAL ribbon across the globe
    rib = Image.new("RGBA", (260, 44), (0, 0, 0, 0))
    rd = ImageDraw.Draw(rib)
    rd.rectangle([0, 0, 260, 44], fill=(178, 34, 34, 255))
    rd.text((130, 22), "NO DEAL", font=font(F_SANS_B, 26),
            fill=WHITE, anchor="mm")
    rib = rib.rotate(-16, expand=True, resample=Image.BICUBIC)
    img.paste(rib, (712, 232), rib)

    # ---- grid of five stories ----
    gx, gy = 26, 364
    cw, ch, gap = 480, 188, 12
    panels = [
        (ORANGE, "MIDDLE EAST", "TANKERS HIT IN HORMUZ",
         "At least three tankers struck by projectiles; two more hit "
         "mines. The Iran–US war at sea escalates.", tanker),
        (BLUE, "WAR IN EUROPE", "WAR SPILLS OVER",
         "Russian drone hits flats near Kyiv — 14 missing, 3 dead. "
         "Russian ships hit off Finland and in Libya.", building_hit),
        (RED, "DISASTER  •  INDONESIA", "FACTORY FIRE: DOZENS MISSING",
         "3 dead in a blaze at a candy factory in Banten; rescuers "
         "search for about 36 workers.", factory_fire),
        ((36, 110, 60), "MEXICO", "“EL CHAPO ISIDRO” CAPTURED",
         "FBI most-wanted cartel boss seized in Sinaloa; 11 killed "
         "in the firefight.", badge),
        ((110, 60, 140), "AI & EXAMS  •  SOUTH KOREA",
         "MINISTER QUITS OVER AI CHEATING",
         "Education chief resigns after 111 device cases in the "
         "Suneung entrance exam.", exam_ai),
        ((200, 120, 20), "DIPLOMACY  •  TODAY", "NEPAL PM MEETS MODI TODAY",
         "Balendra Shah's first Delhi visit: energy, rail and trade "
         "talks in New Delhi.", flags),
    ]
    for i, (color, tag, head, body, icon) in enumerate(panels):
        r, c = divmod(i, 2)
        box = (gx + c * (cw + gap), gy + r * (ch + gap),
               gx + c * (cw + gap) + cw, gy + r * (ch + gap) + ch)
        draw_panel(d, box, color, tag, head, body, icon)

    # ---- ticker ----
    ty0 = 952
    d.rectangle([26, ty0, 998, ty0 + 40], fill=DARK)
    f_tick = fit(d, "ALSO:  BepiColombo reaches Mercury   •   Peru 6.7 quake "
                  "kills 1   •   Nigeria boat sinks, 24 dead",
                 F_SANS_B, 20, 940)
    tick = ("ALSO:  BepiColombo reaches Mercury   •   Peru 6.7 quake "
            "kills 1   •   Nigeria boat sinks, 24 dead")
    d.text((512, ty0 + 20), tick, font=f_tick, fill=WHITE, anchor="mm")
    d.text((26, 998), "Compiled 23 Nov 2026 from UN News, Reuters, AP, AFP, "
           "Yonhap, Al Jazeera and ESA.", font=font(F_SANS, 14), fill=GREY)

    img.save("entry.png", format="PNG")


if __name__ == "__main__":
    main()
