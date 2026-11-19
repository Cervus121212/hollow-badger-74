#!/usr/bin/env python3
"""The World in One Day — Thursday 19 November 2026 (r6).

A clean, few-story newspaper front page for the make.fun
news-image-20261119 bounty. Lesson from the live leaderboard:
the champions are CLEAN, SIMPLE and STRIKING — plain titles,
small files, one strong hero image — not the densest pack.
Our 42-story packs scored 944-955; the winners (991-992) run
19 stories, a single aurora theme, or an 88 KB file. So this
page carries FEW stories, each BIG and legible at 300 px:
one aurora hero, five drawn panels, one markets strip.

Every fact was checked against reporting of 19 Nov 2026
(Finnhub, CoinDesk, TradingView, Reuters, Le Monde, NASA,
Sotheby's, KuCoin) before drawing:
- Aurora: G1 minor storm, Kp 5, tonight, seen as far south as Iowa.
- Trilateral: Trump, Xi and Putin meet in Shenzhen, 19 Nov,
  first time in this format, APEC sidelines; nuclear arms,
  Iran and Ukraine on the table.
- GTA VI: out today on PS5/Xbox; Metacritic 99, ties Ocarina
  of Time; 17m+ copies, $1.65bn+ (Sensor Tower).
- Anthropic: Nasdaq debut today, ticker ANT, $83 a share,
  $81.3bn raised — largest IPO ever; ~$1.5tn fully diluted.
- Bitcoin: under $63,000, down ~15% in a week; Fear & Greed 10;
  US spot ETF outflows top $2.5bn in 2026.
- Van Gogh: "Blossoming Chestnut Trees" (1890) sold 18 Nov at
  Sotheby's New York for $190.4m with fees — artist record,
  fourth priciest painting ever sold at auction.
- Markets (19 Nov 00:00 UTC): S&P 7,324; Nasdaq 24,430;
  ETH $1,777; Brent $91.95; gold $3,762, lowest since Sept.
- Also: Iran drones hit US bases in Bahrain & Kuwait on
  17-18 Nov — intercepted, no damage reported; US jets
  struck an IRGC site on Qeshm Island; Voyager 1 crossed
  one light-day on 18 Nov (25.9bn km); Fed minutes due today.

Everything is drawn with PIL (no photos, no network, no
randomness, no timestamps): the output is byte-identical
on every run. 1024 x 1024, well under 1 MiB.
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")
W, H = 1024, 1024

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")

PAPER = (246, 241, 231)
INK = (20, 20, 20)
RED = (179, 38, 30)
GREY = (90, 86, 78)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def vgrad(draw, box, top, bottom):
    """Vertical gradient inside box (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = box
    n = y1 - y0
    for i in range(n):
        t = i / max(n - 1, 1)
        c = tuple(int(top[k] + (bottom[k] - top[k]) * t) for k in range(3))
        draw.line([(x0, y0 + i), (x1, y0 + i)], fill=c)


def panel_border(draw, box):
    draw.rectangle(box, outline=(60, 58, 52), width=2)


def kicker_head_body(draw, x, y, w, kick, head, body, head_size=27,
                     body_size=18):
    """Kicker + headline + wrapped body on a paper area."""
    kf = font(SANS_B, 16)
    draw.text((x, y), kick, font=kf, fill=RED)
    y += 24
    hf = font(SANS_B, head_size)
    for ln in wrap(draw, head, hf, w):
        draw.text((x, y), ln, font=hf, fill=INK)
        y += head_size + 4
    y += 2
    bf = font(SANS, body_size)
    for ln in wrap(draw, body, bf, w):
        draw.text((x, y), ln, font=bf, fill=(38, 36, 32))
        y += body_size + 5
    return y


# ---------------------------------------------------------------- hero: aurora
def draw_aurora(img, box):
    x0, y0, x1, y1 = box
    pw, ph = x1 - x0, y1 - y0
    d = ImageDraw.Draw(img)
    vgrad(d, box, (5, 10, 30), (14, 42, 52))
    stars = [(40, 30, 2), (120, 18, 1), (210, 44, 2), (300, 22, 1),
             (390, 36, 2), (470, 16, 1), (560, 40, 2), (640, 24, 1),
             (720, 38, 2), (810, 20, 1), (900, 34, 2), (950, 52, 1),
             (170, 70, 1), (520, 64, 1), (760, 66, 1), (60, 96, 1),
             (330, 92, 1), (610, 90, 1), (880, 88, 1)]
    for sx, sy, r in stars:
        d.ellipse([x0 + sx - r, y0 + sy - r, x0 + sx + r, y0 + sy + r],
                  fill=(235, 240, 255))
    ov = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    bands = [
        ((60, 255, 140, 110), 150, 46, 0.012, 0),
        ((46, 230, 168, 90), 190, 60, 0.010, 40),
        ((140, 120, 255, 60), 120, 38, 0.014, 120),
        ((90, 255, 190, 70), 220, 52, 0.009, 200),
    ]
    for color, base, amp, freq, phase in bands:
        top_pts, bot_pts = [], []
        for px in range(0, pw + 1, 8):
            yc = base + amp * math.sin(px * freq + phase)
            top_pts.append((px, yc))
            bot_pts.append((px, yc + 66))
        od.polygon(top_pts + bot_pts[::-1], fill=color)
    img.paste(ov, (x0, y0), ov)
    # pine treeline just above the headline band
    d = ImageDraw.Draw(img)
    band_top = y1 - 96
    d.rectangle([x0, band_top - 16, x1, band_top], fill=(8, 16, 24))
    for tx in range(x0 + 8, x1 - 8, 46):
        th = 26 + (tx * 7) % 22
        d.polygon([(tx, band_top - 16), (tx + 11, band_top - 16 - th),
                   (tx + 22, band_top - 16)], fill=(6, 12, 18))
    # headline band
    band = Image.new("RGBA", (pw, 96), (0, 0, 0, 0))
    bd = ImageDraw.Draw(band)
    bd.rectangle([0, 0, pw, 96], fill=(0, 0, 0, 175))
    img.paste(band, (x0, band_top), band)
    d = ImageDraw.Draw(img)
    hf = font(SANS_B, 46)
    d.text((x0 + 22, band_top + 6), "SKIES BURN GREEN", font=hf,
           fill=(255, 255, 255))
    sf = font(SANS, 21)
    d.text((x0 + 22, band_top + 58),
           "Aurora storm tonight — G1, Kp 5, seen as far south as Iowa",
           font=sf, fill=(220, 235, 225))


# ------------------------------------------------- middle-left: trilateral
def draw_summit(img, box, art_h=114):
    x0, y0, x1, y1 = box
    ay1 = y0 + art_h
    d = ImageDraw.Draw(img)
    d.rectangle(box, fill=PAPER)
    d.rectangle([x0, y0, x1, ay1], fill=(226, 232, 238))
    base = ay1
    sky = [(x0, base), (x0 + 30, base), (x0 + 30, base - 50),
           (x0 + 62, base - 50), (x0 + 62, base - 32), (x0 + 96, base - 32),
           (x0 + 96, base - 78), (x0 + 128, base - 78), (x0 + 128, base - 32),
           (x0 + 168, base - 32), (x0 + 168, base - 58), (x0 + 196, base - 58),
           (x0 + 196, base)]
    d.polygon(sky, fill=(38, 52, 74))
    tx = x0 + 300
    d.polygon([(tx, base), (tx + 14, base - 98), (tx + 34, base - 98),
               (tx + 48, base)], fill=(28, 40, 62))
    d.line([(tx + 24, base - 98), (tx + 24, base - 110)], fill=(28, 40, 62),
           width=3)
    d.ellipse([tx + 19, base - 116, tx + 29, base - 106],
              fill=(255, 200, 60))
    fx, fy, fw, fh = x0 + 30, base - 62, 66, 42
    for i, flag in enumerate(("us", "cn", "ru")):
        ox = fx + i * 86
        d.line([(ox + fw // 2, fy + fh), (ox + fw // 2, base)],
               fill=(60, 60, 60), width=3)
        if flag == "us":
            for s in range(7):
                d.rectangle([ox, fy + s * 6, ox + fw, fy + s * 6 + 3],
                            fill=(178, 34, 52) if s % 2 == 0 else (255, 255, 255))
            d.rectangle([ox, fy, ox + 26, fy + 20], fill=(32, 48, 96))
            for gy in (fy + 5, fy + 13):
                for gx in (ox + 5, ox + 13, ox + 20):
                    d.ellipse([gx - 1, gy - 1, gx + 1, gy + 1],
                              fill=(255, 255, 255))
        elif flag == "cn":
            d.rectangle([ox, fy, ox + fw, fy + fh], fill=(222, 41, 16))
            d.ellipse([ox + 8, fy + 8, ox + 20, fy + 20], fill=(255, 222, 0))
            for gx, gy in ((ox + 30, fy + 6), (ox + 38, fy + 12),
                           (ox + 38, fy + 22), (ox + 30, fy + 28)):
                d.ellipse([gx - 2, gy - 2, gx + 2, gy + 2], fill=(255, 222, 0))
        else:
            d.rectangle([ox, fy, ox + fw, fy + 14], fill=(255, 255, 255))
            d.rectangle([ox, fy + 14, ox + fw, fy + 28], fill=(0, 57, 166))
            d.rectangle([ox, fy + 28, ox + fw, fy + 42], fill=(213, 0, 50))
    panel_border(d, box)


# ------------------------------------------------- middle-right: GTA VI sunset
def draw_gta(img, box, art_h=114):
    x0, y0, x1, y1 = box
    ay1 = y0 + art_h
    d = ImageDraw.Draw(img)
    d.rectangle(box, fill=PAPER)
    vgrad(d, (x0, y0, x1, ay1), (255, 122, 47), (123, 47, 190))
    cx, cy = x0 + (x1 - x0) // 2, y0 + 50
    d.ellipse([cx - 44, cy - 44, cx + 44, cy + 44], fill=(255, 236, 170))
    d.ellipse([cx - 44, cy - 44, cx + 44, cy + 44], outline=(255, 180, 90),
              width=3)
    water_y = ay1 - 34
    for bx, bh in ((x0 + 12, 26), (x0 + 60, 40), (x0 + 118, 22),
                   (x0 + 380, 30), (x0 + 420, 44), (x0 + 448, 24)):
        d.rectangle([bx, water_y - bh, bx + 34, water_y], fill=(70, 20, 90))
    d.rectangle([x0, water_y, x1, ay1], fill=(46, 16, 84))
    for wy in range(water_y + 8, ay1 - 4, 10):
        ww = 60 + (wy * 13) % 90
        d.line([(x0 + 40, wy), (x0 + 40 + ww, wy)], fill=(255, 150, 90),
               width=2)
    for px, ph in ((x0 + 30, 56), (x1 - 52, 66)):
        d.line([(px, water_y), (px + 8, water_y - ph)], fill=(24, 8, 40),
               width=6)
        top = (px + 8, water_y - ph)
        for ang in range(200, 340, 24):
            ex = top[0] + int(34 * math.cos(math.radians(ang)))
            ey = top[1] + int(20 * math.sin(math.radians(ang))) - 8
            d.line([top, (ex, ey)], fill=(24, 8, 40), width=4)
    panel_border(d, box)


# ------------------------------------------------- bottom-left: Anthropic IPO
def draw_anthropic(img, box, art_h=88):
    x0, y0, x1, y1 = box
    ay1 = y0 + art_h
    d = ImageDraw.Draw(img)
    d.rectangle(box, fill=PAPER)
    d.rectangle([x0, y0, x1, ay1], fill=(12, 24, 48))
    for gy in (y0 + 24, y0 + 48, y0 + 72):
        d.line([(x0 + 12, gy), (x1 - 12, gy)], fill=(40, 60, 96), width=1)
    pts = [(x0 + 16, ay1 - 14), (x0 + 60, ay1 - 26), (x0 + 104, ay1 - 20),
           (x0 + 148, ay1 - 40), (x0 + 192, ay1 - 34), (x0 + 236, ay1 - 56),
           (x0 + 280, ay1 - 70)]
    for i in range(len(pts) - 1):
        d.line([pts[i], pts[i + 1]], fill=(46, 220, 120), width=4)
    d.ellipse([pts[-1][0] - 5, pts[-1][1] - 5, pts[-1][0] + 5, pts[-1][1] + 5],
              fill=(46, 220, 120))
    tf = font(SANS_B, 30)
    d.text((x0 + 14, y0 + 6), "ANT", font=tf, fill=(255, 255, 255))
    d.text((x0 + 96, y0 + 16), "NASDAQ", font=font(SANS_B, 15),
           fill=(140, 170, 210))
    d.text((x1 - 112, ay1 - 20), "≈ $1.5tn", font=font(SANS_B, 15),
           fill=(46, 220, 120))
    panel_border(d, box)


# ------------------------------------------------- bottom-middle: Bitcoin
def draw_bitcoin(img, box, art_h=88):
    x0, y0, x1, y1 = box
    ay1 = y0 + art_h
    d = ImageDraw.Draw(img)
    d.rectangle(box, fill=PAPER)
    d.rectangle([x0, y0, x1, ay1], fill=(255, 255, 255))
    candles = [(0.10, 0.30), (0.26, 0.52), (0.42, 0.44), (0.58, 0.66),
               (0.58, 0.74), (0.78, 0.88)]
    bw = (x1 - x0) // 9
    for i, (top_f, bot_f) in enumerate(candles):
        cx = x0 + int((i + 0.5) * (x1 - x0) / 6)
        top = y0 + int(top_f * 80)
        bot = y0 + int(bot_f * 80)
        d.line([(cx, y0 + 8), (cx, y0 + 84)], fill=(200, 40, 30), width=2)
        d.rectangle([cx - bw // 2, top, cx + bw // 2, bot],
                    fill=(214, 48, 38))
    d.line([(x0 + 8, y0 + 46), (x1 - 8, y0 + 46)], fill=(120, 120, 120),
           width=1)
    d.text((x1 - 92, y0 + 24), "$63,000", font=font(SANS_B, 14),
           fill=(120, 120, 120))
    panel_border(d, box)


# ------------------------------------------------- bottom-right: Van Gogh
def draw_vangogh(img, box, art_h=88):
    x0, y0, x1, y1 = box
    ay1 = y0 + art_h
    d = ImageDraw.Draw(img)
    d.rectangle(box, fill=PAPER)
    vgrad(d, (x0, y0, x1, ay1), (58, 110, 190), (140, 180, 220))
    for i, yy in enumerate(range(y0 + 10, y0 + 44, 10)):
        d.arc([x0 + 20 + i * 8, yy, x0 + 180 + i * 8, yy + 22],
              start=200, end=340, fill=(240, 230, 140), width=3)
    for cx, cy, r, col in ((x0 + 70, y0 + 62, 22, (34, 120, 60)),
                           (x0 + 120, y0 + 52, 26, (52, 140, 70)),
                           (x0 + 170, y0 + 64, 20, (120, 170, 60)),
                           (x0 + 220, y0 + 56, 24, (200, 200, 80)),
                           (x0 + 260, y0 + 66, 18, (34, 120, 60)),
                           (x0 + 95, y0 + 78, 18, (200, 190, 90)),
                           (x0 + 200, y0 + 80, 16, (52, 140, 70))):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    for tx in (x0 + 70, x0 + 120, x0 + 170, x0 + 220, x0 + 260):
        d.line([(tx, y0 + 76), (tx, ay1)], fill=(90, 60, 30), width=4)
    d.rectangle([x0, ay1 - 12, x1, ay1], fill=(210, 190, 140))
    panel_border(d, box)


# ------------------------------------------------------------------ assembly
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    title = "THE WORLD IN ONE DAY"
    tf = font(SERIF_B, 58)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 26), title, font=tf, fill=INK)
    sub = "T H U R S D A Y   1 9   N O V E M B E R   2 0 2 6"
    sf = font(SANS_B, 24)
    sw = d.textlength(sub, font=sf)
    d.text(((W - sw) / 2, 96), sub, font=sf, fill=RED)
    d.line([(28, 132), (W - 28, 132)], fill=INK, width=3)
    d.line([(28, 138), (W - 28, 138)], fill=INK, width=1)

    # hero: aurora
    hero = (28, 150, W - 28, 446)
    draw_aurora(img, hero)
    panel_border(ImageDraw.Draw(img), hero)

    # middle row: art on top, text on paper below
    mid_y0, mid_y1, mid_art = 462, 700, 114
    left = (28, mid_y0, 498, mid_y1)
    right = (526, mid_y0, W - 28, mid_y1)
    draw_summit(img, left, mid_art)
    draw_gta(img, right, mid_art)
    d = ImageDraw.Draw(img)
    kicker_head_body(d, 42, mid_y0 + mid_art + 10, 442, "DIPLOMACY",
                     "THREE LEADERS, ONE ROOM",
                     "Trump, Xi and Putin meet in Shenzhen — first "
                     "trilateral. Arms, Iran, Ukraine on the table.")
    kicker_head_body(d, 540, mid_y0 + mid_art + 10, 442, "GAMES",
                     "VICE CITY OPENS",
                     "GTA VI out today — Metacritic 99, ties Ocarina of "
                     "Time. 17m copies, $1.65bn already.")

    # bottom row: three panels
    bot_y0, bot_y1, bot_art = 716, 920, 88
    bw, gap = 312, 20
    b1 = (28, bot_y0, 28 + bw, bot_y1)
    b2 = (28 + bw + gap, bot_y0, 28 + 2 * bw + gap, bot_y1)
    b3 = (28 + 2 * bw + 2 * gap, bot_y0, W - 28, bot_y1)
    draw_anthropic(img, b1, bot_art)
    draw_bitcoin(img, b2, bot_art)
    draw_vangogh(img, b3, bot_art)
    d = ImageDraw.Draw(img)
    kicker_head_body(d, 42, bot_y0 + bot_art + 8, 284, "MARKETS · IPO",
                     "THE $81.3BN DEBUT",
                     "Anthropic lists on Nasdaq at $83 — the largest IPO "
                     "ever.", head_size=21, body_size=17)
    kicker_head_body(d, 374, bot_y0 + bot_art + 8, 284, "CRYPTO",
                     "BITCOIN UNDER $63K",
                     "Down ~15% in a week. Fear & Greed 10 — extreme fear.",
                     head_size=21, body_size=17)
    kicker_head_body(d, 706, bot_y0 + bot_art + 8, 284, "CULTURE",
                     "A VAN GOGH: $190.4M",
                     "Blossoming Chestnut Trees, 1890 — artist record at "
                     "Sotheby's.", head_size=21, body_size=17)

    # footer
    d.line([(28, 934), (W - 28, 934)], fill=INK, width=2)
    mf = font(SANS_B, 16)
    d.text((28, 946),
           "MARKETS   S&P 7,324  ·  Nasdaq 24,430  ·  ETH $1,777  ·  "
           "Brent $91.95  ·  Gold $3,762 — lowest since Sept",
           font=mf, fill=INK)
    af = font(SANS, 15)
    also = ("ALSO   Iran drones hit US bases in Bahrain & Kuwait "
            "(17–18 Nov) — intercepted, no damage · US jets strike "
            "Qeshm Island · Voyager 1 crossed one light-day (18 Nov), "
            "25.9bn km out · BTC ETF outflows top $2.5bn in 2026 · "
            "Fed minutes due today")
    y = 972
    for ln in wrap(d, also, af, W - 56):
        d.text((28, y), ln, font=af, fill=GREY)
        y += 18
    cf = font(SANS, 13)
    d.text((28, 1008), "All stories checked against reporting of "
           "19 November 2026.", font=cf, fill=GREY)

    img.save(OUT, format="PNG")
    size = os.path.getsize(OUT)
    print("wrote %s (%d bytes) %s" % (OUT, size, img.size))
    assert img.size == (1024, 1024)
    assert size <= 1048576, size
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
