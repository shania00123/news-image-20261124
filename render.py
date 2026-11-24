#!/usr/bin/env python3
"""news-image-20261124 v2 — THE TUESDAY LEDGER, full-day edition.

Draws one 1024x1024 front page summing up the world's news of Tuesday
24 November 2026. Every story was verified against reporting published
on that day; stories first reported earlier live only in the DATE CHECK
box. Drawn entirely with PIL (stdlib + Pillow), no network at run time,
two runs write identical bytes.

Usage:  python3 render.py            # writes poster.png next to this file
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "poster.png")

# ---- palette ------------------------------------------------------------
PAPER   = (247, 243, 232)   # newsprint cream
INK     = (26, 26, 26)
MUTED   = (96, 90, 78)
RULE    = (180, 172, 152)
RED     = (176, 32, 32)
NAVY    = (31, 58, 95)
NAVY_D  = (22, 42, 70)
GOLD    = (176, 132, 32)
GREEN   = (28, 110, 60)
SKY     = (168, 205, 228)
SEA     = (58, 110, 150)
CARD    = (255, 255, 255)
CARD_BG = (250, 247, 238)
GREY_BG = (232, 228, 216)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def f_serif(s):
    return font("DejaVuSerif-Bold.ttf", s)


def f_serif_r(s):
    return font("DejaVuSerif.ttf", s)


def f_sans(s):
    return font("DejaVuSans.ttf", s)


def f_sans_b(s):
    return font("DejaVuSans-Bold.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
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


def fit_lines(draw, text, fnt, max_w, max_lines):
    """Wrap text, truncate to max_lines with an ellipsis if needed."""
    lines = wrap(draw, text, fnt, max_w)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        while lines and draw.textlength(lines[-1] + "…", font=fnt) > max_w:
            lines[-1] = lines[-1][:-1]
        lines[-1] = lines[-1].rstrip() + "…"
    return lines


def text_block(draw, x, y, lines, fnt, fill=INK, leading=None):
    """Draw lines; returns y just below the last line."""
    lh = leading or int(fnt.size * 1.22)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


# ---- the day's news (verified Tue 24 Nov 2026) -------------------------
# kind: icon key for the small drawn thumb. pin: (lon, lat) for the map.

HEROES = [
    dict(num=1, place="ULLEUNG ISLAND", kind="jets",
         head="Five Russian jets spark a 3-minute island scare",
         deck=("Seoul's first-ever air-raid alert over a possible "
               "intrusion; F-15Ks scramble."),
         pin=(130.9, 37.5)),
    dict(num=2, place="SANTA CLARA", kind="chip",
         head="Huang's hero welcome — then the rally fades",
         deck=("Up 31% Monday on his return as CEO; down 5% Tuesday "
               "as governance questions mount."),
         pin=(-121.0, 37.35)),
    dict(num=3, place="BRUSSELS", kind="satellite",
         head="Allies: Russia may put a nuclear weapon in orbit",
         deck=("The warning says a launch could come as soon as next month; "
               "NATO vows to defend space."),
         pin=(4.35, 50.85)),
]

GRID = [
    dict(num=4, place="BERLIN", kind="chart",
         head="German business mood hits a 3-year high",
         deck="Ifo 90.6, a seventh straight rise.",
         pin=(13.4, 52.5)),
    dict(num=5, place="MOSCOW", kind="skull",
         head="Hacked data puts Russia's war dead near 500,000",
         deck="New leak tallies the Ukraine war toll.",
         pin=(37.6, 55.75)),
    dict(num=6, place="BEIJING", kind="gavel",
         head="China probes a Politburo member",
         deck="Fourth top leader probed since 2025.",
         pin=(116.4, 39.9)),
    dict(num=7, place="GAZA CITY", kind="blast",
         head="Israeli strike kills a senior Hamas security chief",
         deck="Naeem Abu Nahel killed in Gaza City.",
         pin=(34.45, 31.5)),
    dict(num=8, place="ZAPORIZHZHIA", kind="blast",
         head="Russian attack kills 2, wounds 22",
         deck="Two children among the wounded.",
         pin=(35.14, 47.85)),
    dict(num=9, place="KYIV", kind="ship",
         head="Ukraine defends its strike on Russian ships off Libya",
         deck="Calls the attack self-defence, UN Charter.",
         pin=(30.5, 50.45)),
    dict(num=10, place="MANILA", kind="money",
         head="Trump offers the Philippines $2.4bn",
         deck="Self-defence aid — with a catch.",
         pin=(121.0, 14.6)),
    dict(num=11, place="MEXICO CITY", kind="drone",
         head="Mexico nabs 'Chapo Isidro' with a US drone overhead",
         deck="US drone helped capture the drug lord.",
         pin=(-99.1, 19.4)),
    dict(num=12, place="LONDON", kind="gavel",
         head="GTA VI hacker gets 7 years",
         deck="Walks free on time already served.",
         pin=(-0.13, 51.5)),
    dict(num=13, place="JERUSALEM", kind="flag",
         head="Israel rivals clash over the Iran threat",
         deck="Eisenkot has until 6 Dec to govern.",
         pin=(35.2, 31.77)),
    dict(num=14, place="WASHINGTON", kind="capitol",
         head="Trump targets Newsom in DOJ crime speech",
         deck="Crime speech attacks Democrats.",
         pin=(-77.0, 38.9)),
    dict(num=15, place="IOWA", kind="blast",
         head="Army to detonate unstable explosives Wed",
         deck="68 barrels of lead azide to be blown up.",
         pin=(-91.4, 40.9)),
    dict(num=16, place="LONDON", kind="shield",
         head="UK warns of Russian sabotage threat",
         deck="MI5 alerts firms backing Ukraine.",
         pin=(-2.4, 51.3)),
    dict(num=17, place="BAGHDAD", kind="oil",
         head="Iraq PM seizes Kurdistan's border crossings",
         deck="Baghdad to run the fields after probe.",
         pin=(44.4, 33.3)),
    dict(num=18, place="RAS AL KHAIMAH", kind="crash",
         head="Bus and truck crash kills 11",
         deck="Eleven dead, the ministry says.",
         pin=(55.9, 25.8)),
    dict(num=19, place="GENEVA", kind="chess",
         head="Gukesh opens his world chess defence",
         deck="Faces Javokhir Sindarov in Geneva.",
         pin=(6.14, 46.2)),
    dict(num=20, place="JAKARTA", kind="ballot",
         head="Prabowo taps VP picks",
         deck="Loyalist + tycoon's cousin named.",
         pin=(106.8, -6.2)),
    dict(num=21, place="NEW DELHI", kind="train",
         head="Saryu-Kamala Express rolls",
         deck="Modi, Nepal PM flag off the train.",
         pin=(77.2, 28.6)),
    dict(num=22, place="BEIJING", kind="gavel",
         head="China sentences an official to death for spying",
         deck="AP reports the sentence on Tuesday.",
         pin=(114.6, 39.9)),
]

ALSO = [
    (23, "WASHINGTON", "Rep. Jimmy Gomez resigns after ethics panel finds sexual misconduct"),
    (24, "WASHINGTON", "Storms and airline glitches threaten messy Thanksgiving travel"),
    (25, "PARIS", "Macron eyes constitutional changes to curb spending"),
    (26, "NEW YORK", "Ms Rachel protests US child immigration hearings"),
    (27, "BANGKOK", "Thai court upholds verdict for opposition lawmaker"),
    (28, "KATHMANDU", "Nepal PM in India for economic and energy talks"),
    (29, "BEIJING", "China state media hits back at 'deflation trap' warnings"),
    (30, "LONDON", "Don Toliver postpones O2 show; 89 showed symptoms"),
    (31, "SEOUL", "Bank of Korea seen raising rates on Thursday, poll finds"),
    (32, "MUMBAI", "Earthshot Prize opens in Mumbai on Tuesday evening"),
    (33, "WASHINGTON", "Trump orders executions expedited"),
    (34, "OTTAWA", "Carney brings fake Trump on stage at press gallery dinner"),
    (35, "KHARTOUM", "Drones hit homes and a UN building in Sudan's capital"),
    (36, "ANKARA", "Thousands protest media closures"),
    (37, "PYONGYANG", "Kim threatens to shut Swiss diplomatic office"),
    (38, "MURMANSK", "Governor detained over embezzlement"),
]

DATE_CHECK = [
    ("Nvidia board reinstates Huang", "MON 23 NOV", "Tue: the welcome + market fallout"),
    ("Ukraine sinks corvette Merkury off Libya", "SUN 22 NOV", "Tue: Kyiv defends it"),
    ("Russian cargo ship hit, Gulf of Finland", "SAT 21 NOV", "Tue: Zelenskyy confirms it"),
    ("Russia warns Estonia of 'open war'", "MON 23 NOV", ""),
    ("India–NZ Test ends in a draw", "MON 23 NOV", ""),
    ("COP31 talks collapse with no deal", "SUN 22 NOV", ""),
    ("Indonesia factory fire kills 24", "MON 23 NOV", ""),
    ("Verstappen wins Las Vegas GP", "SUN 22 NOV", ""),
    ("Alcaraz wins ATP Finals", "SUN 22 NOV", ""),
    ("Two US states sue SpaceX over Grok", "MON 23 NOV", ""),
]

NUMBERS = [
    ("5", "RUSSIAN JETS IN THE KADIZ"),
    ("500,000", "RUSSIAN WAR DEAD, HACKED DATA"),
    ("90.6", "GERMAN IFO, 3-YEAR HIGH"),
    ("+6.3%", "KOSPI, TUESDAY CLOSE"),
    ("$2.4BN", "US OFFER TO MANILA"),
    ("7", "YEARS FOR THE GTA VI HACKER"),
]

TIMELINE = [
    ("07:52 KST", "Ulleung alert: jets near island"),
    ("06:00 UTC", "Asia closes: Kospi +6.3%, Nikkei +3.9%"),
    ("08:00 UTC", "German Ifo 90.6, best in 3+ years"),
    ("12:03 UTC", "UK sanctions Houthis, 4 named"),
    ("13:00 UTC", "Nvidia −5.2% premarket"),
    ("15:00 UTC", "US consumer confidence due"),
]

MARKETS = [
    ("KOSPI", "+6.3%", "5,006.03", "TUE"),
    ("NIKKEI", "+3.9%", "58,644.63", "TUE"),
    ("TAIEX", "+9.1%", "40,122", "TUE"),
    ("HANG SENG", "−0.7%", "22,219.65", "TUE"),
    ("S&P 500", "+4.73%", "7,237.17", "MON"),
    ("NASDAQ", "+6.51%", "24,089.56", "MON"),
]

REGIONS = [
    ("ASIA-PACIFIC", 12),
    ("EUROPE", 11),
    ("AMERICAS", 9),
    ("MIDDLE EAST", 5),
    ("AFRICA", 1),
]


# ---- drawn art ----------------------------------------------------------
# All scenes are simple PIL geometry: no images, no fonts-as-pictures.

def jet(d, cx, cy, s, color, flip=False):
    """A small fighter-jet silhouette, pointing right (or left if flip)."""
    pts = [(cx - 14 * s, cy), (cx - 4 * s, cy - 4 * s), (cx + 12 * s, cy),
           (cx - 4 * s, cy + 4 * s)]
    if flip:
        pts = [(2 * cx - px, py) for px, py in pts]
    d.polygon(pts, fill=color)
    d.polygon([(cx - 8 * s, cy - 3 * s), (cx - 2 * s, cy - 9 * s),
               (cx + 1 * s, cy - 3 * s)], fill=color)
    d.polygon([(cx - 8 * s, cy + 3 * s), (cx - 2 * s, cy + 9 * s),
               (cx + 1 * s, cy + 3 * s)], fill=color)


def hero_jets(d, x, y, w, h):
    """Ulleung: dawn sea, island, Russian jets inbound, F-15K answering."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 228, 238))
    # sun low on the horizon
    d.ellipse([x + w - 78, y + 14, x + w - 34, y + 58], fill=(232, 170, 60))
    # sea
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=SEA)
    for i in range(5):
        yy = y + h * 0.62 + 12 + i * 9
        d.line([x + 8 + i * 17, yy, x + 60 + i * 40, yy], fill=(120, 165, 195), width=2)
    # island with lighthouse
    ix = x + w * 0.30
    d.polygon([(ix - 52, y + h * 0.62), (ix - 34, y + h * 0.34),
               (ix + 30, y + h * 0.34), (ix + 52, y + h * 0.62)],
              fill=(96, 128, 84))
    d.rectangle([ix - 4, y + h * 0.34 - 26, ix + 4, y + h * 0.34], fill=(240, 240, 235))
    d.ellipse([ix - 7, y + h * 0.34 - 33, ix + 7, y + h * 0.34 - 19], fill=RED)
    # alert ring around the island
    d.ellipse([ix - 62, y + h * 0.30 - 14, ix + 62, y + h * 0.30 + 74],
              outline=RED, width=3)
    # incoming jets (dark) and the answering F-15K (navy, opposite way)
    jet(d, x + w * 0.72, y + 34, 1.3, (60, 60, 60))
    jet(d, x + w * 0.86, y + 58, 1.1, (60, 60, 60))
    jet(d, x + w * 0.52, y + h * 0.72, 1.4, NAVY, flip=True)
    # "3 MIN" alert tag
    d.rectangle([x + 10, y + 10, x + 116, y + 32], fill=RED)
    d.text((x + 16, y + 14), "3-MIN ALERT", font=f_sans_b(12), fill=(255, 255, 255))


def hero_chip(d, x, y, w, h):
    """Santa Clara: a chip on a chart that rockets up, then turns down."""
    d.rectangle([x, y, x + w, y + h], fill=(18, 30, 46))
    # grid
    for i in range(1, 6):
        yy = y + i * h // 6
        d.line([x + 6, yy, x + w - 6, yy], fill=(44, 62, 88), width=1)
    # Monday surge (green) then Tuesday fade (red)
    pts_up = [(x + 16, y + h - 26), (x + 90, y + h - 52), (x + 150, y + 34),
              (x + 205, y + 22)]
    d.line(pts_up, fill=(64, 200, 120), width=4, joint="curve")
    d.line([(x + 205, y + 22), (x + 268, y + 52), (x + w - 14, y + 66)],
           fill=RED, width=4, joint="curve")
    d.polygon([(x + 196, y + 14), (x + 214, y + 14), (x + 205, y + 30)],
              fill=(64, 200, 120))
    # chip in the corner
    cx, cy = x + w - 74, y + h - 52
    d.rectangle([cx - 26, cy - 26, cx + 26, cy + 26], fill=(36, 58, 92),
                outline=(120, 170, 220), width=2)
    d.rectangle([cx - 12, cy - 12, cx + 12, cy + 12], fill=(64, 200, 120))
    for k in range(3):
        d.line([cx - 26, cy - 14 + k * 14, cx - 34, cy - 14 + k * 14],
               fill=(120, 170, 220), width=2)
        d.line([cx + 26, cy - 14 + k * 14, cx + 34, cy - 14 + k * 14],
               fill=(120, 170, 220), width=2)
    d.text((x + 14, y + 12), "+31.5% MON", font=f_sans_b(15), fill=(64, 200, 120))
    d.text((x + 14, y + 34), "−5.2% TUE PRE", font=f_sans_b(15), fill=(255, 110, 110))


def hero_satellite(d, x, y, w, h):
    """Brussels: a satellite with a red star, ringed orbit, NATO shield."""
    d.rectangle([x, y, x + w, y + h], fill=(12, 16, 34))
    for sx, sy, sr in [(30, 22, 2), (90, 44, 1), (150, 18, 2), (210, 52, 1),
                        (260, 26, 2), (300, 70, 1), (60, 78, 1), (180, 84, 1)]:
        d.ellipse([x + sx - sr, y + sy - sr, x + sx + sr, y + sy + sr],
                  fill=(255, 255, 255))
    # orbit ring
    d.ellipse([x + 40, y - 30, x + w - 40, y + h + 10], outline=(90, 120, 170),
              width=2)
    # satellite body + panels
    cx, cy = x + w // 2, y + h // 2 - 14
    d.rectangle([cx - 52, cy - 10, cx - 16, cy + 10], fill=(70, 110, 170))
    d.rectangle([cx + 16, cy - 10, cx + 52, cy + 10], fill=(70, 110, 170))
    d.rectangle([cx - 16, cy - 16, cx + 16, cy + 16], fill=(200, 200, 200),
                outline=NAVY, width=2)
    d.line([cx - 16, cy, cx - 52, cy], fill=(150, 180, 210), width=2)
    d.line([cx + 16, cy, cx + 52, cy], fill=(150, 180, 210), width=2)
    # red star on the body
    star = [(cx, cy - 9), (cx + 3, cy - 2), (cx + 10, cy - 2), (cx + 4, cy + 3),
            (cx + 6, cy + 10), (cx, cy + 5), (cx - 6, cy + 10), (cx - 4, cy + 3),
            (cx - 10, cy - 2), (cx - 3, cy - 2)]
    d.polygon(star, fill=RED)
    # dish below
    d.polygon([(cx - 6, cy + 16), (cx + 6, cy + 16), (cx + 14, cy + 30),
               (cx - 14, cy + 30)], fill=(150, 180, 210))
    d.text((x + 12, y + h - 26), "NUCLEAR IN ORBIT?", font=f_sans_b(14),
           fill=(255, 220, 120))


HERO_SCENES = {"jets": hero_jets, "chip": hero_chip, "satellite": hero_satellite}


def thumb(d, x, y, w, h, kind):
    """A small drawn icon for a grid card, on a tinted tile."""
    tints = {"jets": (214, 228, 238), "chip": (18, 30, 46), "satellite": (12, 16, 34),
             "chart": (222, 236, 222), "skull": (238, 228, 222), "gavel": (232, 228, 216),
             "blast": (246, 226, 214), "ship": (214, 228, 238), "money": (222, 238, 222),
             "drone": (228, 232, 240), "flag": (238, 226, 226), "capitol": (226, 230, 240),
             "shield": (226, 230, 240), "oil": (240, 232, 214), "crash": (246, 226, 214),
             "chess": (236, 232, 222), "ballot": (232, 228, 240), "train": (228, 232, 240)}
    d.rectangle([x, y, x + w, y + h], fill=tints.get(kind, GREY_BG))
    cx, cy = x + w // 2, y + h // 2
    if kind == "chart":
        d.line([(x + 6, y + h - 10), (x + 16, y + h - 22), (x + 26, y + 16),
                (x + 38, y + 10)], fill=GREEN, width=3, joint="curve")
        d.polygon([(x + 32, y + 8), (x + 40, y + 8), (x + 36, y + 16)], fill=GREEN)
    elif kind == "skull":
        d.ellipse([cx - 10, cy - 11, cx + 10, cy + 7], fill=(250, 250, 250),
                  outline=INK, width=2)
        d.ellipse([cx - 6, cy - 4, cx - 2, cy + 1], fill=INK)
        d.ellipse([cx + 2, cy - 4, cx + 6, cy + 1], fill=INK)
        d.rectangle([cx - 6, cy + 7, cx + 6, cy + 13], fill=(250, 250, 250),
                    outline=INK, width=2)
    elif kind == "gavel":
        d.rectangle([cx - 14, cy - 8, cx + 14, cy - 2], fill=(120, 84, 40))
        d.rectangle([cx - 3, cy - 2, cx + 3, cy + 12], fill=(120, 84, 40))
        d.rectangle([cx - 12, cy + 12, cx + 12, cy + 16], fill=(90, 64, 30))
    elif kind == "blast":
        for a in range(8):
            import math
            ang = a * 3.14159 / 4
            d.line([cx, cy, cx + int(15 * math.cos(ang)), cy + int(15 * math.sin(ang))],
                   fill=(220, 120, 30), width=3)
        d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=(220, 60, 30))
    elif kind == "ship":
        d.polygon([(cx - 16, cy + 2), (cx + 16, cy + 2), (cx + 11, cy + 12),
                   (cx - 11, cy + 12)], fill=NAVY)
        d.rectangle([cx - 2, cy - 12, cx + 2, cy + 2], fill=INK)
        d.polygon([(cx + 2, cy - 12), (cx + 12, cy - 4), (cx + 2, cy - 4)],
                  fill=RED)
        d.line([x + 4, cy + 16, x + w - 4, cy + 16], fill=SEA, width=2)
    elif kind == "money":
        d.rectangle([cx - 15, cy - 9, cx + 15, cy + 9], fill=(120, 180, 120),
                    outline=GREEN, width=2)
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(240, 240, 220))
        d.text((cx - 3, cy - 7), "$", font=f_sans_b(11), fill=GREEN)
    elif kind == "drone":
        d.ellipse([cx - 13, cy - 6, cx - 5, cy + 2], fill=INK)
        d.ellipse([cx + 5, cy - 6, cx + 13, cy + 2], fill=INK)
        d.ellipse([cx - 13, cy + 6, cx - 5, cy + 14], fill=INK)
        d.ellipse([cx + 5, cy + 6, cx + 13, cy + 14], fill=INK)
        d.rectangle([cx - 7, cy - 4, cx + 7, cy + 8], fill=(90, 90, 90))
    elif kind == "flag":
        d.rectangle([cx - 10, cy - 14, cx - 8, cy + 14], fill=INK)
        d.polygon([(cx - 8, cy - 14), (cx + 12, cy - 9), (cx - 8, cy - 4)],
                  fill=RED)
    elif kind == "capitol":
        d.polygon([(cx - 12, cy + 12), (cx, cy - 12), (cx + 12, cy + 12)],
                  fill=(200, 200, 200), outline=INK, width=1)
        d.rectangle([cx - 14, cy + 12, cx + 14, cy + 16], fill=INK)
        d.ellipse([cx - 6, cy - 12, cx + 6, cy - 4], fill=(200, 200, 200),
                  outline=INK, width=1)
    elif kind == "shield":
        d.polygon([(cx, cy - 13), (cx + 11, cy - 8), (cx + 11, cy + 2),
                   (cx, cy + 14), (cx - 11, cy + 2), (cx - 11, cy - 8)],
                  fill=NAVY)
        d.text((cx - 4, cy - 6), "!", font=f_sans_b(13), fill=(255, 255, 255))
    elif kind == "oil":
        d.polygon([(cx, cy - 14), (cx + 9, cy + 2), (cx + 6, cy + 12),
                   (cx - 6, cy + 12), (cx - 9, cy + 2)], fill=(40, 40, 40))
        d.ellipse([cx - 4, cy + 2, cx + 4, cy + 10], fill=(240, 240, 220))
    elif kind == "crash":
        d.rectangle([cx - 14, cy - 4, cx - 2, cy + 8], fill=(200, 60, 60))
        d.rectangle([cx + 2, cy - 2, cx + 14, cy + 8], fill=(60, 90, 140))
        d.polygon([(cx - 2, cy - 10), (cx + 2, cy - 4), (cx - 2, cy - 4)],
                  fill=GOLD)
        d.ellipse([cx - 10, cy + 8, cx - 4, cy + 14], fill=INK)
        d.ellipse([cx + 6, cy + 8, cx + 12, cy + 14], fill=INK)
    elif kind == "chess":
        d.rectangle([cx - 12, cy - 12, cx + 12, cy + 12], fill=(250, 250, 250),
                    outline=INK, width=2)
        d.line([cx, cy - 12, cx, cy + 12], fill=INK, width=1)
        d.line([cx - 12, cy, cx + 12, cy], fill=INK, width=1)
        d.ellipse([cx - 9, cy - 9, cx - 3, cy - 3], fill=INK)
        d.ellipse([cx + 3, cy + 3, cx + 9, cy + 9], fill=INK)
    elif kind == "ballot":
        d.rectangle([cx - 12, cy - 10, cx + 12, cy + 12], fill=(250, 250, 250),
                    outline=INK, width=2)
        d.line([cx - 8, cy + 2, cx - 2, cy + 8], fill=RED, width=3)
        d.line([cx - 2, cy + 8, cx + 9, cy - 6], fill=RED, width=3)
    elif kind == "train":
        d.rectangle([cx - 13, cy - 10, cx + 13, cy + 10], fill=NAVY)
        d.rectangle([cx - 9, cy - 6, cx - 1, cy + 0], fill=SKY)
        d.rectangle([cx + 1, cy - 6, cx + 9, cy + 0], fill=SKY)
        d.line([x + 2, cy + 13, x + w - 2, cy + 13], fill=INK, width=2)
    elif kind == "jets":
        jet(d, cx, cy, 0.9, (60, 60, 60))
    elif kind == "chip":
        d.rectangle([cx - 11, cy - 11, cx + 11, cy + 11], fill=(36, 58, 92),
                    outline=(120, 170, 220), width=2)
        d.rectangle([cx - 5, cy - 5, cx + 5, cy + 5], fill=(64, 200, 120))
    elif kind == "satellite":
        d.rectangle([cx - 14, cy - 4, cx - 5, cy + 4], fill=(70, 110, 170))
        d.rectangle([cx + 5, cy - 4, cx + 14, cy + 4], fill=(70, 110, 170))
        d.rectangle([cx - 5, cy - 6, cx + 5, cy + 6], fill=(200, 200, 200),
                    outline=NAVY, width=1)


# ---- simplified world map ----------------------------------------------
# Rough continent polygons (lon, lat) — recognisable, not precise.
CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-125, 72), (-110, 68), (-95, 69), (-85, 66),
     (-80, 62), (-75, 58), (-70, 45), (-75, 35), (-80, 26), (-85, 29),
     (-90, 21), (-97, 16), (-105, 20), (-115, 29), (-125, 40), (-125, 49),
     (-140, 60), (-155, 58), (-165, 60)],
    # South America
    [(-80, 10), (-75, 5), (-60, 5), (-50, 0), (-40, -5), (-35, -10),
     (-40, -20), (-48, -28), (-58, -38), (-65, -45), (-70, -55), (-73, -40),
     (-72, -20), (-80, -5)],
    # Europe
    [(-10, 36), (-9, 43), (-2, 48), (-4, 50), (2, 51), (5, 53), (8, 57),
     (10, 59), (18, 56), (21, 55), (24, 59), (28, 60), (30, 65), (32, 70),
     (40, 68), (45, 60), (40, 52), (35, 46), (30, 46), (28, 44), (23, 40),
     (19, 42), (12, 44), (8, 44), (3, 42), (0, 39)],
    # Africa
    [(-6, 35), (10, 37), (20, 32), (30, 31), (35, 28), (43, 12), (51, 11),
     (48, 0), (40, -10), (35, -20), (32, -29), (26, -34), (19, -35),
     (15, -27), (12, -18), (9, -1), (-8, 4), (-16, 12), (-17, 20), (-15, 30)],
    # Asia
    [(40, 68), (50, 70), (60, 72), (70, 73), (80, 73), (90, 75), (105, 77),
     (120, 73), (135, 72), (150, 70), (160, 66), (170, 66), (178, 65),
     (170, 60), (162, 56), (158, 52), (150, 59), (142, 50), (140, 40),
     (135, 35), (130, 33), (127, 40), (122, 38), (120, 30), (115, 22),
     (110, 20), (108, 12), (105, 9), (100, 7), (98, 10), (95, 16), (92, 21),
     (89, 22), (86, 20), (80, 13), (77, 8), (74, 20), (70, 23), (66, 25),
     (61, 25), (57, 26), (52, 28), (50, 30), (48, 29), (44, 30), (40, 36),
     (36, 36), (35, 42), (40, 46), (42, 52), (45, 60)],
    # Australia
    [(114, -22), (122, -14), (130, -12), (136, -12), (142, -11), (146, -19),
     (150, -23), (153, -27), (150, -37), (140, -38), (135, -35), (129, -32),
     (124, -33), (118, -35), (114, -32)],
]


def lonlat_to_xy(lon, lat, x0, y0, x1, y1):
    x = x0 + (lon + 170.0) / 360.0 * (x1 - x0)
    y = y0 + (85.0 - lat) / 140.0 * (y1 - y0)
    return x, y


def draw_map(d, x0, y0, x1, y1, pins):
    """Ocean, continents, numbered pins for heroes + grid stories."""
    d.rectangle([x0, y0, x1, y1], fill=(206, 224, 238))
    for poly in CONTINENTS:
        pts = [lonlat_to_xy(lon, lat, x0, y0, x1, y1) for lon, lat in poly]
        d.polygon(pts, fill=(226, 216, 188), outline=(150, 140, 110))
    # graticule
    for lon in range(-150, 181, 30):
        gx, _ = lonlat_to_xy(lon, 0, x0, y0, x1, y1)
        d.line([gx, y0, gx, y1], fill=(190, 210, 228), width=1)
    # pins, with a declutter pass: try offsets in order, take the first
    # spot at least 17 px from every pin already placed.
    placed = []
    offsets = [(0, 0), (17, -9), (-17, -9), (17, 9), (-17, 9), (0, -18),
               (0, 18), (26, 0), (-26, 0), (26, -18), (-26, -18)]
    for num, lon, lat in pins:
        px, py = lonlat_to_xy(lon, lat, x0, y0, x1, y1)
        ox, oy = 0, 0
        for cand in offsets:
            cx, cy = px + cand[0], py + cand[1]
            if all((cx - qx) ** 2 + (cy - qy) ** 2 >= 17 ** 2
                   for (qx, qy) in placed):
                ox, oy = cand
                break
        else:
            ox, oy = offsets[-1]
        placed.append((px + ox, py + oy))
        if ox or oy:
            d.line([px, py, px + ox, py + oy], fill=RED, width=1)
        cx, cy = px + ox, py + oy
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=RED,
                  outline=(255, 255, 255), width=2)
        lbl = str(num)
        tw = d.textlength(lbl, font=f_sans_b(9))
        d.text((cx - tw / 2, cy - 6), lbl, font=f_sans_b(9), fill=(255, 255, 255))


# ---- layout -------------------------------------------------------------
MARGIN = 12


def draw_masthead(d):
    d.text((MARGIN, 8), "FULL-DAY EDITION", font=f_sans_b(12), fill=RED)
    right = "TUESDAY 24 NOVEMBER 2026"
    tw = d.textlength(right, font=f_sans_b(12))
    d.text((W - MARGIN - tw, 8), right, font=f_sans_b(12), fill=INK)
    title = "THE TUESDAY LEDGER"
    tf = f_serif(46)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 24), title, font=tf, fill=INK)
    d.line([MARGIN, 86, W - MARGIN, 86], fill=INK, width=3)
    d.line([MARGIN, 90, W - MARGIN, 90], fill=INK, width=1)
    sub = "THE WORLD IN ONE DAY  —  38 STORIES, EVERY ONE VERIFIED AGAINST TUESDAY'S REPORTING"
    sf = f_sans_b(11)
    tw = d.textlength(sub, font=sf)
    d.text(((W - tw) / 2, 96), sub, font=sf, fill=NAVY)


def draw_numbers(d):
    y0, y1 = 112, 148
    d.rectangle([MARGIN, y0, W - MARGIN, y1], fill=CARD)
    d.rectangle([MARGIN, y0, W - MARGIN, y1], outline=RULE, width=1)
    cw = (W - 2 * MARGIN) / 6
    for i, (num, label) in enumerate(NUMBERS):
        x = MARGIN + i * cw
        nf = f_serif(21)
        tw = d.textlength(num, font=nf)
        d.text((x + (cw - tw) / 2, y0 + 3), num, font=nf, fill=RED)
        lf = f_sans_b(8)
        tw = d.textlength(label, font=lf)
        d.text((x + (cw - tw) / 2, y0 + 26), label, font=lf, fill=MUTED)
        if i:
            d.line([x, y0 + 5, x, y1 - 5], fill=RULE, width=1)


def draw_timeline(d):
    y0 = 152
    d.text((MARGIN, y0), "THE DAY IN UTC", font=f_sans_b(10), fill=RED)
    col_w = (W - 2 * MARGIN - 130) / 3
    x0 = MARGIN + 130
    for i, (t, txt) in enumerate(TIMELINE):
        col, row = i % 3, i // 3
        x = x0 + col * col_w
        y = y0 + row * 13
        d.text((x, y), t, font=f_sans_b(10), fill=NAVY)
        tw = d.textlength(t + " ", font=f_sans_b(10))
        lines = fit_lines(d, txt, f_sans(10), col_w - tw - 6, 1)
        d.text((x + tw, y), lines[0] if lines else "", font=f_sans(10), fill=INK)


def draw_hero(d, story, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=CARD)
    d.rectangle([x, y, x + w, y + h], outline=RULE, width=1)
    HERO_SCENES[story["kind"]](d, x + 1, y + 1, w - 2, 104)
    ty = y + 110
    d.text((x + 8, ty), "%d · %s" % (story["num"], story["place"]),
           font=f_sans_b(11), fill=RED)
    lines = fit_lines(d, story["head"], f_sans_b(16), w - 16, 2)
    ty = text_block(d, x + 8, ty + 16, lines, f_sans_b(16), leading=19)
    dlines = fit_lines(d, story["deck"], f_sans(11), w - 16, 2)
    text_block(d, x + 8, ty + 3, dlines, f_sans(11), fill=MUTED, leading=13)


def draw_grid_card(d, story, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=CARD_BG)
    d.rectangle([x, y, x + w, y + h], outline=RULE, width=1)
    thumb(d, x + 4, y + 4, 44, h - 8, story["kind"])
    tx = x + 52
    tw = w - 56
    d.text((tx, y + 3), "%d · %s" % (story["num"], story["place"]),
           font=f_sans_b(9), fill=RED)
    lines = fit_lines(d, story["head"], f_sans_b(10), tw, 2)
    text_block(d, tx, y + 14, lines, f_sans_b(10), leading=11)
    dlines = fit_lines(d, story["deck"], f_sans(9), tw, 1)
    if dlines:
        d.text((tx, y + h - 13), dlines[0], font=f_sans(9), fill=MUTED)


def draw_legend_cell(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NAVY_D)
    lines = ["HOW TO READ",
             "1–22 pinned on the map.",
             "ALSO lists 16 more.",
             "DATE CHECK holds stories",
             "from earlier days."]
    yy = y + 5
    for i, ln in enumerate(lines):
        f = f_sans_b(9) if i == 0 else f_sans(9)
        d.text((x + 8, yy), ln, font=f, fill=(255, 255, 255))
        yy += 9 if i else 11


def draw_map_section(d):
    y0 = 650
    d.text((MARGIN, y0), "THE WORLD ON TUESDAY — 22 STORIES PINNED",
           font=f_sans_b(12), fill=INK)
    map_x0, map_y0, map_x1, map_y1 = MARGIN, y0 + 16, 756, 782
    pins = [(s["num"], s["pin"][0], s["pin"][1]) for s in HEROES + GRID]
    draw_map(d, map_x0, map_y0, map_x1, map_y1, pins)
    # region tally panel
    px0, py0, px1, py1 = 768, y0 + 16, W - MARGIN, 782
    d.rectangle([px0, py0, px1, py1], fill=CARD)
    d.rectangle([px0, py0, px1, py1], outline=RULE, width=1)
    d.text((px0 + 10, py0 + 6), "WHERE THE NEWS WAS", font=f_sans_b(11), fill=INK)
    yy = py0 + 26
    for name, count in REGIONS:
        d.text((px0 + 10, yy), name, font=f_sans_b(10), fill=INK)
        bw = (px1 - px0 - 118 - 30) * count / 12.0
        d.rectangle([px0 + 118, yy + 2, px0 + 118 + bw, yy + 10], fill=NAVY)
        d.text((px1 - 24, yy), str(count), font=f_sans_b(11), fill=RED)
        yy += 17


def draw_also(d):
    y0 = 784
    d.text((MARGIN, y0), "ALSO ON TUESDAY", font=f_sans_b(12), fill=INK)
    d.line([MARGIN + 150, y0 + 8, W - MARGIN, y0 + 8], fill=RULE, width=1)
    col_w = (W - 2 * MARGIN) / 2
    for i, (num, place, txt) in enumerate(ALSO):
        col, row = i % 2, i // 2
        x = MARGIN + col * col_w
        y = y0 + 14 + row * 12
        head = "%d · %s — " % (num, place)
        hw = d.textlength(head, font=f_sans_b(10))
        d.text((x, y), head, font=f_sans_b(10), fill=NAVY)
        lines = fit_lines(d, txt, f_sans(10), col_w - hw - 4, 1)
        d.text((x + hw, y), lines[0] if lines else "", font=f_sans(10), fill=INK)


def draw_date_check(d):
    y0 = 894
    d.text((MARGIN, y0), "DATE CHECK — NOT TUESDAY, KEPT OUT OF THE COUNT",
           font=f_sans_b(11), fill=RED)
    col_w = (W - 2 * MARGIN) / 2
    for i, (txt, when, note) in enumerate(DATE_CHECK):
        col, row = i % 2, i // 2
        x = MARGIN + col * col_w
        y = y0 + 12 + row * 11
        s = "%s — %s" % (txt, when)
        if note:
            s += " · " + note
        lines = fit_lines(d, s, f_sans(8), col_w - 4, 1)
        d.text((x, y), lines[0] if lines else "", font=f_sans(8), fill=MUTED)


def draw_markets(d):
    y0 = 964
    d.rectangle([MARGIN, y0, W - MARGIN, H - 6], fill=NAVY_D)
    d.text((MARGIN + 8, y0 + 4), "MARKETS — TUESDAY CLOSES IN ASIA, MONDAY IN NEW YORK",
           font=f_sans_b(10), fill=(255, 220, 120))
    cw = (W - 2 * MARGIN - 16) / 6
    for i, (name, chg, val, day) in enumerate(MARKETS):
        x = MARGIN + 8 + i * cw
        d.text((x, y0 + 18), "%s — %s" % (name, day), font=f_sans_b(9),
               fill=(200, 210, 230))
        d.text((x, y0 + 30), "%s  %s" % (chg, val), font=f_sans_b(11),
               fill=(255, 255, 255))
    foot = ("Nvidia +31.5% Mon to $165.05, −5.2% premarket Tue  ·  Gold $3,630.30  ·  "
            "Brent $86.90 (Mon)  ·  Sources: Reuters, AP, AFP, Yonhap, SCMP, Japan Times, ifo, Xinhua")
    d.text((MARGIN + 8, y0 + 46), foot, font=f_sans(8), fill=(180, 190, 210))


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    draw_numbers(d)
    draw_timeline(d)
    # heroes: 3 panels, y 180–376
    hw = (W - 2 * MARGIN - 2 * 10) // 3
    for i, story in enumerate(HEROES):
        draw_hero(d, story, MARGIN + i * (hw + 10), 180, hw, 196)
    gw = (W - 2 * MARGIN - 3 * 8) // 4
    for i, story in enumerate(GRID):
        row, col = divmod(i, 4)
        draw_grid_card(d, story, MARGIN + col * (gw + 8), 380 + row * 54,
                       gw, 52)
    draw_legend_cell(d, MARGIN + 3 * (gw + 8), 380 + 4 * 54, gw, 52)
    draw_map_section(d)
    draw_also(d)
    draw_date_check(d)
    draw_markets(d)
    return img


def main():
    img = build()
    img.save(OUT, format="PNG", optimize=True)
    print("wrote %s (%d bytes)" % (OUT, os.path.getsize(OUT)))


if __name__ == "__main__":
    main()
