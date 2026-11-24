#!/usr/bin/env python3
"""Render THE TUESDAY LEDGER: the world's news of Tuesday 24 November 2026
as one 1024x1024 newspaper poster (poster.png).

Drawn entirely with PIL from the story list below. Every story was verified
against reporting dated Tuesday 24 November 2026 (see NOTES.md in the work
dir); stories first reported on an earlier day live only in the DATE CHECK
box at the foot of the page, never in the count.

Deterministic: no network, no clock, no randomness. Run twice, same bytes.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (26, 26, 26)
RED = (164, 18, 32)
NAVY = (18, 40, 75)
GREY = (110, 105, 95)
LIGHT_LINE = (205, 198, 184)
CARD_BG = (255, 253, 247)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap by pixel width; returns a list of lines."""
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill=INK, leading=None, max_w=None):
    """Draw lines; returns y after the last line."""
    lh = leading or int(fnt.size * 1.22)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


# ---------------------------------------------------------------- stories
# (city, region tag, headline, deck). Heroes first, then the grid, then ALSO.
HEROES = [
    ("SEOUL", "KOREA SCARE",
     "Russian jets spark 3-minute scare on Ulleung",
     "Seoul alerts Ulleung after Russian jets enter its air-defence zone; "
     "alert lifted in three minutes."),
    ("SANTA CLARA", "HUANG RETURNS",
     "Huang is back \u2014 and Asia roars",
     "Nvidia reinstates Jensen Huang after Trump intervenes; Kospi jumps "
     "6.3%, Nikkei 3% as the AI trade revives."),
    ("BRUSSELS", "SPACE THREAT",
     "Allies: Russia may put a nuclear weapon in orbit",
     "NATO vows space defence as allies warn Moscow could launch a "
     "nuclear-armed satellite as soon as next month."),
]

GRID = [
    ("MOSCOW", "RUSSIA", "Hacked data puts Russian war dead near 500,000",
     "Newly leaked figures put Moscow's Ukraine death toll close to half a million."),
    ("WASHINGTON", "WHITE HOUSE", "Trump targets Newsom in DOJ crime speech",
     "President assails the 'radical left' and Newsom on death sentences."),
    ("MANILA", "PHILIPPINES", "Trump offers Manila $2.4bn for self-defence",
     "US aid comes with a catch, as Washington presses its oldest Asian ally."),
    ("LONDON", "COURTS", "GTA VI hacker gets 7 years",
     "Arion Kurtaj, 21, sentenced for the Rockstar hacks; free on time served."),
    ("JERUSALEM", "ISRAEL", "Rivals clash over Iran threat",
     "Eisenkot races to build a coalition to replace Netanyahu."),
    ("BEIJING", "CHINA", "China sentences official to death for spying",
     "Court finds the official leaked national secrets in Beijing."),
    ("PYONGYANG", "NORTH KOREA", "Kim threatens to shut Swiss office",
     "North Korea says it may close the Swiss diplomatic mission."),
    ("MEXICO CITY", "CARTELS", "Mexico nabs 'Chapo Isidro' with US drone help",
     "Elite troops seize a top wanted narco, with a US drone overhead."),
    ("MURMANSK", "RUSSIA", "Governor detained over embezzlement",
     "Authorities hold the Arctic region's governor on suspicion of graft."),
    ("JAKARTA", "INDONESIA", "Prabowo taps VP picks",
     "President names a loyalist and a tycoon's cousin as his vice-presidential choices."),
    ("NEW DELHI", "INDIA", "Saryu-Kamala Express rolls",
     "Modi and Nepal's PM Shah flag off the Ayodhya\u2013Janakpur train link."),
    ("LISBON", "PORTUGAL", "Thousands march on living costs",
     "Streets fill in Lisbon as households protest rising prices."),
    ("NAYPYIDAW", "MYANMAR", "Myanmar slams ASEAN ruling",
     "Military-backed government calls the bloc's decision unfair and unbalanced."),
    ("GENEVA", "CHESS", "Gukesh defends his crown",
     "World champion opens his title defence against Uzbekistan's Sindarov in Geneva."),
    ("MUMBAI", "EARTHSHOT", "Earthshot Prize opens in Mumbai",
     "Prince William's green awards begin; finalists pitch fixes for wildfires and more."),
    ("WASHINGTON", "EXECUTIONS", "Trump orders executions expedited",
     "President directs federal death sentences to move faster."),
    ("OTTAWA", "CANADA", "Carney brings fake Trump on stage",
     "PM enlists a Trump impersonator for laughs at the press gallery dinner."),
    ("KHARTOUM", "SUDAN", "Drones hit homes, UN building",
     "Strikes pound the capital as the war grinds on."),
    ("ANKARA", "TURKEY", "Thousands protest media closures",
     "Crowds rally as authorities shut outlets in a widening crackdown."),
]

ALSO = [
    ("WASHINGTON", "Rep. Jimmy Gomez resigns after ethics panel finds sexual misconduct"),
    ("WASHINGTON", "Storms and airline glitches threaten messy Thanksgiving travel"),
    ("PARIS", "Macron eyes constitutional changes to curb spending"),
    ("NEW YORK", "Ms Rachel protests US child immigration hearings"),
    ("BANGKOK", "Thai court upholds verdict for opposition lawmaker"),
    ("KATHMANDU", "Nepal PM in India for economic and energy talks"),
    ("BEIJING", "China state media hits back at 'deflation trap' warnings"),
    ("LONDON", "Don Toliver postpones O2 show after Manchester gas scare"),
    ("SEOUL", "Bank of Korea seen raising rates on Thursday, poll finds"),
    ("MARANELLO", "Ferrari unveils two new 296 models at Finali Mondiali"),
    ("NEW DELHI", "Modi opens AI centre at IIT Patna"),
    ("ARUNACHAL", "India and China hold military talks to ease border tensions"),
    ("UNITED NATIONS", "UN chief calls for AI risk framework within a year"),
]

DATE_CHECK = [
    ("Russia warns Estonia of 'open war'", "Mon 23 Nov"),
    ("Ukraine sinks Russian warship off Libya", "Sun 22 Nov"),
    ("India\u2013NZ Test ends in a draw", "Mon 23 Nov"),
    ("Quad leaders unveil 5 outcomes", "Tue 17 Nov"),
    ("Verstappen wins Las Vegas GP", "Sun 22 Nov"),
    ("Alcaraz wins ATP Finals", "Sun 22 Nov"),
    ("COP31 talks collapse with no deal", "Sun 22 Nov"),
    ("Indonesia factory fire kills 24", "Mon 23 Nov"),
    ("Dymer strike kills 11", "Mon 23 Nov"),
    ("Democrats clinch 258th House seat", "Sun 22 Nov"),
    ("Two US states sue SpaceX over Grok", "Mon 23 Nov"),
    ("Sparta II cargo ship hit by drones", "Sat 21 Nov"),
]

NUMBERS = [
    ("3", "MINUTES: ULLEUNG ALERT"),
    ("500,000", "RUSSIAN WAR DEAD"),
    ("$2.4BN", "US OFFER TO MANILA"),
    ("7", "YEARS: GTA VI HACKER"),
    ("+6.3%", "KOSPI INTRADAY SURGE"),
    ("89", "MANCHESTER SYMPTOMS"),
]

MARKETS = [
    ("KOSPI", "-3.31%", "4,708.54"),
    ("HANG SENG", "-0.12%", "22,383.74"),
    ("TAIEX", "+2.16%", "36,811.89"),
    ("S&P 500", "+4.73%", "7,237.17"),
    ("NASDAQ", "+6.51%", "24,089.56"),
    ("GOLD", "+3.27%", "$3,630.30"),
    ("BITCOIN", "-0.17%", "$61,060"),
    ("BRENT", "-6.13%", "$86.90"),
]

# ------------------------------------------------------------- drawn scenes
def hero_korea(d, x, y, w, h):
    """Radar screen over the East Sea: sweep arcs, island, two jets."""
    d.rectangle([x, y, x + w, y + h], fill=(16, 28, 52))
    cx, cy = x + w // 2, y + h - 8
    for r in (18, 34, 50, 66):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(70, 120, 90), width=1)
    d.line([cx, cy - 66, cx, cy + 6], fill=(70, 120, 90), width=1)
    d.line([cx - 66, cy, cx + 66, cy], fill=(70, 120, 90), width=1)
    # Ulleung island
    d.ellipse([cx - 14, cy - 34, cx + 16, cy - 12], fill=(214, 178, 110))
    d.ellipse([cx - 6, cy - 40, cx + 8, cy - 28], fill=(214, 178, 110))
    d.ellipse([cx - 4, cy - 32, cx + 4, cy - 24], outline=RED, width=2)
    # two jets as swept triangles
    for jx, jy in ((x + 34, y + 22), (x + w - 52, y + 16)):
        d.polygon([(jx, jy), (jx - 16, jy + 7), (jx - 6, jy + 2),
                   (jx - 14, jy + 12)], fill=(235, 235, 235))
    d.text((x + 8, y + h - 16), "07:52 KST \u2014 ALERT 3 MIN",
           font=font(SANS_B, 11), fill=(255, 214, 90))


def hero_chip(d, x, y, w, h):
    """A chip on a rising market: circuit traces and a climbing chart."""
    d.rectangle([x, y, x + w, y + h], fill=(12, 34, 22))
    # circuit traces
    for ty in (y + 18, y + 34, y + h - 20):
        d.line([x + 10, ty, x + w - 10, ty], fill=(46, 120, 70), width=1)
        d.ellipse([x + w - 16, ty - 3, x + w - 10, ty + 3], fill=(90, 200, 120))
    # chip
    cx, cy = x + w // 2 - 6, y + h // 2 + 4
    d.rectangle([cx - 26, cy - 20, cx + 26, cy + 20], fill=(24, 68, 40),
                outline=(120, 220, 150), width=2)
    d.rectangle([cx - 14, cy - 10, cx + 14, cy + 10], fill=(16, 44, 28),
                outline=(120, 220, 150), width=1)
    for px in range(-2, 3):
        d.line([cx + px * 10, cy - 26, cx + px * 10, cy - 20],
               fill=(120, 220, 150), width=2)
        d.line([cx + px * 10, cy + 20, cx + px * 10, cy + 26],
               fill=(120, 220, 150), width=2)
    # rising chart with arrow
    pts = [(x + 12, y + h - 14), (x + 52, y + h - 30), (x + 92, y + h - 24),
           (x + 132, y + h - 46), (x + 172, y + h - 52), (x + 208, y + h - 62)]
    d.line(pts, fill=(120, 230, 130), width=3, joint="curve")
    d.polygon([(x + 208, y + h - 62), (x + 196, y + h - 60), (x + 206, y + h - 48)],
              fill=(120, 230, 130))
    d.text((x + w - 78, y + 6), "+6.3%", font=font(SANS_B, 15),
           fill=(120, 230, 130))


def hero_space(d, x, y, w, h):
    """A satellite crossing Earth's limb, orbit ring, warning star."""
    d.rectangle([x, y, x + w, y + h], fill=(8, 10, 24))
    for sx, sy in ((x + 22, y + 12), (x + 88, y + 26), (x + 150, y + 10),
                   (x + 210, y + 30), (x + 60, y + 44), (x + 260, y + 18)):
        d.ellipse([sx, sy, sx + 2, sy + 2], fill=(220, 220, 240))
    # Earth limb: a wide flat ellipse whose bottom edge is the scene bottom,
    # so the blue stays inside the frame
    d.ellipse([x - 60, y + h - 52, x + w + 60, y + h], fill=(38, 92, 168))
    d.arc([x - 60, y + h - 52, x + w + 60, y + h], 200, 340,
          fill=(140, 200, 250), width=2)
    # orbit ellipse
    d.ellipse([x + 30, y + 8, x + w - 20, y + h - 6], outline=(150, 150, 170),
              width=1)
    # satellite: body + panels
    sx, sy = x + w - 78, y + 30
    d.rectangle([sx - 8, sy - 6, sx + 8, sy + 6], fill=(210, 210, 220),
                outline=(120, 120, 140), width=1)
    d.rectangle([sx - 30, sy - 3, sx - 8, sy + 3], fill=(70, 110, 190))
    d.rectangle([sx + 8, sy - 3, sx + 30, sy + 3], fill=(70, 110, 190))
    d.line([sx, sy + 6, sx, sy + 12], fill=(210, 210, 220), width=2)
    # red warning star
    wx, wy = x + 44, y + 16
    d.polygon([(wx, wy - 8), (wx + 2, wy - 2), (wx + 8, wy), (wx + 2, wy + 2),
               (wx, wy + 8), (wx - 2, wy + 2), (wx - 8, wy), (wx - 2, wy - 2)],
              fill=(255, 70, 70))


# small scene motifs for grid cards: (bg, motif) per index, cycled
MOTIFS = ["bars", "coins", "rings", "waves", "grid", "peaks", "sun", "flag"]
PALETTE = [(18, 40, 75), (60, 30, 60), (20, 60, 50), (90, 50, 20),
           (40, 40, 40), (70, 20, 25), (30, 55, 90), (55, 70, 25)]


def card_scene(d, x, y, w, h, idx):
    bg = PALETTE[idx % len(PALETTE)]
    motif = MOTIFS[idx % len(MOTIFS)]
    d.rectangle([x, y, x + w, y + h], fill=bg)
    fg = (235, 225, 200)
    if motif == "bars":
        for i, bh in enumerate((8, 16, 11, 20, 14)):
            bx = x + 10 + i * 12
            d.rectangle([bx, y + h - 4 - bh, bx + 7, y + h - 4], fill=fg)
    elif motif == "coins":
        for i, cx in enumerate((x + 14, x + 34, x + 54)):
            d.ellipse([cx, y + 5, cx + 14, y + 19], outline=(255, 214, 90), width=2)
            d.text((cx + 4, y + 7), "$", font=font(SANS_B, 10), fill=(255, 214, 90))
    elif motif == "rings":
        for r in (5, 9, 13):
            d.ellipse([x + w // 2 - r, y + h // 2 - r, x + w // 2 + r,
                       y + h // 2 + r], outline=fg, width=1)
    elif motif == "waves":
        for k in range(3):
            yy = y + 6 + k * 6
            d.line([(x + 6, yy), (x + 20, yy + 4), (x + 34, yy),
                    (x + 48, yy + 4), (x + 62, yy)], fill=fg, width=1)
    elif motif == "grid":
        for gx in range(x + 8, x + w - 6, 12):
            d.line([gx, y + 4, gx, y + h - 4], fill=(160, 160, 180), width=1)
        for gy in range(y + 5, y + h - 3, 7):
            d.line([x + 6, gy, x + w - 6, gy], fill=(160, 160, 180), width=1)
    elif motif == "peaks":
        d.polygon([(x + 6, y + h - 4), (x + 24, y + 6), (x + 42, y + h - 4)],
                  fill=fg)
        d.polygon([(x + 34, y + h - 4), (x + 56, y + 10), (x + 78, y + h - 4)],
                  fill=(200, 190, 160))
    elif motif == "sun":
        cx, cy = x + w // 2, y + h // 2
        d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=(255, 200, 80))
        for a in range(0, 360, 45):
            import math
            dx, dy = math.cos(math.radians(a)), math.sin(math.radians(a))
            d.line([cx + dx * 10, cy + dy * 10, cx + dx * 14, cy + dy * 14],
                   fill=(255, 200, 80), width=1)
    else:  # flag
        d.line([x + 12, y + 3, x + 12, y + h - 3], fill=fg, width=2)
        d.polygon([(x + 12, y + 4), (x + 44, y + 8), (x + 12, y + 14)],
                  fill=(200, 60, 60))
        d.polygon([(x + 12, y + 14), (x + 36, y + 17), (x + 12, y + 20)],
                  fill=fg)


# ------------------------------------------------------------- dotted map
# Continents as ellipses in map-pixel space: (lon, lat, rx_px, ry_px).
# Centres are placed by lon/lat; radii are pixels so the shapes read at
# the map's own aspect ratio instead of squashing vertically.
LAND_PX = [
    (-100, 50, 78, 15), (-152, 63, 26, 7), (-96, 20, 26, 7), (-40, 73, 22, 7),
    (-60, -15, 30, 19), (15, 52, 46, 10), (0, 54, 7, 5), (18, 5, 46, 21),
    (95, 50, 92, 16), (78, 20, 22, 13), (105, 12, 26, 9), (115, -2, 32, 5),
    (134, -25, 30, 9), (139, 37, 9, 7),
]
# (lon, lat, story number, display dx, dy in px). A non-zero offset draws
# the pin beside its true spot with a leader line, so close cities do not
# pile on one another (Seoul/Pyongyang, Washington/Ottawa, the Black Sea).
PINS = [
    (127, 37, 1, 0, 0), (-122, 37, 2, 0, 0), (4, 50, 3, 8, -2),
    (37, 55, 4, 0, 0), (-77, 39, 5, 0, 0), (121, 14, 6, 6, 4),
    (0, 51, 7, -14, -8), (35, 32, 8, -13, 12), (116, 40, 9, 0, 0),
    (126, 39, 10, 14, -8), (-99, 19, 11, 0, 0), (33, 69, 12, -10, -6),
    (107, -6, 13, 0, 0), (77, 28, 14, 0, 0), (-9, 39, 15, -8, 10),
    (96, 20, 16, 0, 0), (6, 46, 17, -12, 8), (73, 19, 18, -10, 8),
    (-77, 39, 19, -14, 10), (-76, 45, 20, 12, -8), (32, 15, 21, -18, -6),
    (33, 40, 22, 12, 8),
]


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 232, 216),
                outline=LIGHT_LINE, width=1)
    cols, rows = 110, 24
    cw, ch = w / cols, h / rows
    for r in range(rows):
        lat = 84 - (r + 0.5) * 168 / rows
        for c in range(cols):
            lon = -180 + (c + 0.5) * 360 / cols
            px = x + (lon + 180) / 360 * w
            py = y + (90 - lat) / 180 * h
            land = False
            for (clon, clat, rx, ry) in LAND_PX:
                ccx = x + (clon + 180) / 360 * w
                ccy = y + (90 - clat) / 180 * h
                if ((px - ccx) / rx) ** 2 + ((py - ccy) / ry) ** 2 <= 1:
                    land = True
                    break
            if land:
                d.ellipse([px - 1.4, py - 1.4, px + 1.4, py + 1.4],
                          fill=(150, 140, 118))
    fnum = font(SANS_B, 8)
    for (lon, lat, num, dx, dy) in PINS:
        px = x + (lon + 180) / 360 * w
        py = y + (90 - lat) / 180 * h
        qx, qy = px + dx, py + dy
        if dx or dy:
            d.line([px, py, qx, qy], fill=RED, width=1)
            d.ellipse([px - 1.5, py - 1.5, px + 1.5, py + 1.5], fill=RED)
        d.ellipse([qx - 6, qy - 6, qx + 6, qy + 6], fill=RED,
                  outline=(255, 255, 255), width=1)
        tw = d.textlength(str(num), font=fnum)
        d.text((qx - tw / 2, qy - 5), str(num), font=fnum, fill=(255, 255, 255))

# ------------------------------------------------------------------ layout
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    f_top = font(SANS_B, 11)
    f_mast = font(SERIF_B, 54)
    f_tick = font(SANS_B, 13)
    f_num = font(SERIF_B, 24)
    f_numlab = font(SANS, 9)
    f_mk = font(SANS_B, 10)
    f_mk2 = font(SANS, 9)
    f_tl = font(SANS, 10)
    f_htag = font(SANS_B, 10)
    f_hhead = font(SERIF_B, 17)
    f_hdeck = font(SANS, 11)
    f_ctag = font(SANS_B, 9)
    f_chead = font(SANS_B, 11)
    f_cdeck = font(SANS, 9)
    f_sect = font(SANS_B, 11)
    f_also = font(SANS, 11)
    f_dc = font(SANS, 10)
    f_foot = font(SANS, 9)

    # top bar
    d.text((8, 5), "THE WORLD IN ONE DAY", font=f_top, fill=INK)
    right = "35 STORIES \u00b7 6 REGIONS \u00b7 EVERY ONE DATED TUESDAY 24 NOVEMBER 2026"
    d.text((W - 8 - d.textlength(right, font=f_top), 5), right, font=f_top, fill=INK)
    d.line([8, 24, W - 8, 24], fill=INK, width=2)

    # masthead
    title = "Tuesday 24 November 2026"
    d.text(((W - d.textlength(title, font=f_mast)) / 2, 28), title,
           font=f_mast, fill=INK)
    d.line([8, 94, W - 8, 94], fill=RED, width=3)

    # ticker
    tick = ("Russian jets spark Korea scare  \u00b7  Huang returns to Nvidia  "
            "\u00b7  Allies warn of nuclear satellite")
    d.text((8, 98), tick, font=f_tick, fill=INK)
    d.rectangle([W - 92, 96, W - 8, 116], fill=RED)
    d.text((W - 84, 99), "KOREA", font=f_tick, fill=(255, 255, 255))
    d.line([8, 116, W - 8, 116], fill=INK, width=1)

    # six numbers
    cell_w = (W - 16) / 6
    for i, (num, lab) in enumerate(NUMBERS):
        cx = 8 + i * cell_w
        d.text((cx + 6, 122), num, font=f_num, fill=RED)
        for ln in wrap(d, lab, f_numlab, cell_w - 12):
            d.text((cx + 6, 150), ln, font=f_numlab, fill=GREY)
        if i:
            d.line([cx, 120, cx, 162], fill=LIGHT_LINE, width=1)
    d.line([8, 164, W - 8, 164], fill=INK, width=1)

    # markets band
    d.rectangle([8, 166, W - 8, 194], fill=NAVY)
    d.text((14, 172), "MARKETS", font=f_mk, fill=(255, 214, 90))
    d.text((14, 182), "MON 23 NOV", font=f_mk2, fill=(180, 190, 210))
    mx = 120
    item_w = (W - 8 - mx) / len(MARKETS)
    for (name, pct, val) in MARKETS:
        d.text((mx + 4, 169), name, font=f_mk2, fill=(180, 190, 210))
        col = (110, 220, 130) if pct.startswith("+") else (255, 120, 110)
        d.text((mx + 4, 180), f"{val}  {pct}", font=f_mk, fill=col)
        mx += item_w
    d.text((8, 198),
           "THE DAY IN UTC  \u00b7  22:52 MON Ulleung alert issued  \u00b7  00:03 "
           "Taiex futures surge 8.65%  \u00b7  TUE MORNING Kospi +5.4%, Nikkei +2.7%  "
           "\u00b7  TUE MORNING Nvidia rehires Huang",
           font=f_tl, fill=GREY)

    # hero scenes + text
    hero_draw = [hero_korea, hero_chip, hero_space]
    hx, hw = 8, 328
    for i, (city, tag, head, deck) in enumerate(HEROES):
        x = hx + i * (hw + 8)
        hero_draw[i](d, x, 214, hw, 76)
        d.rectangle([x, 214, x + hw, 290], outline=INK, width=1)
        yy = 294
        d.text((x, yy), f"{i + 1}  {city}  \u00b7  {tag}", font=f_htag, fill=RED)
        yy += 14
        yy = text_block(d, x, yy, wrap(d, head, f_hhead, hw), f_hhead, leading=19)
        text_block(d, x, yy + 2, wrap(d, deck, f_hdeck, hw)[:2], f_hdeck,
                   leading=12)
    d.line([8, 372, W - 8, 372], fill=INK, width=1)

    # grid: 19 cards, 5 columns x 4 rows
    cw, chh, gap = 197, 80, 8
    for i, (city, tag, head, deck) in enumerate(GRID):
        r, c = divmod(i, 5)
        x = 8 + c * (cw + gap)
        y = 374 + r * (chh + 2)
        d.rectangle([x, y, x + cw, y + chh], fill=CARD_BG, outline=LIGHT_LINE)
        card_scene(d, x + 1, y + 1, cw - 2, 16, i)
        d.text((x + 4, y + 19), f"{i + 4}  {city} \u00b7 {tag}", font=f_ctag, fill=RED)
        yy = text_block(d, x + 4, y + 31, wrap(d, head, f_chead, cw - 8)[:2],
                        f_chead, leading=12)
        text_block(d, x + 4, y + 57, wrap(d, deck, f_cdeck, cw - 8)[:2],
                   f_cdeck, leading=11)

    # map strip
    d.text((8, 704), "THE WORLD ON TUESDAY \u2014 22 STORIES PINNED",
           font=f_sect, fill=INK)
    draw_map(d, 8, 720, 692, 76)
    d.rectangle([708, 720, W - 8, 800], fill=CARD_BG, outline=LIGHT_LINE)
    d.text((718, 724), "BY REGION", font=f_sect, fill=RED)
    regions = [("EUROPE", 10), ("ASIA-PACIFIC", 14), ("AMERICAS", 8),
               ("MIDDLE EAST", 1), ("AFRICA", 1), ("WORLD", 1)]
    ry = 740
    for name, n in regions:
        d.text((718, ry), name, font=f_tl, fill=INK)
        cnt = str(n)
        d.text((W - 18 - d.textlength(cnt, font=f_mk), ry), cnt, font=f_mk,
               fill=INK)
        ry += 10

    # ALSO list
    d.text((8, 800), "ALSO ON TUESDAY 24 NOVEMBER \u2014 13 MORE STORIES",
           font=f_sect, fill=INK)
    d.line([8, 814, W - 8, 814], fill=INK, width=1)
    for i, (city, head) in enumerate(ALSO):
        col = 0 if i < 7 else 1
        row = i if i < 7 else i - 7
        x = 8 + col * 508
        y = 818 + row * 15
        num = 23 + i
        d.text((x, y), str(num), font=f_mk, fill=RED)
        d.text((x + 24, y), f"{city} \u2014 {head}", font=f_also, fill=INK)

    # DATE CHECK box
    d.rectangle([8, 926, W - 8, 1006], outline=RED, width=2)
    d.text((14, 930), "DATE CHECK \u2014 NOT TUESDAY, however listed elsewhere",
           font=f_sect, fill=RED)
    for i, (item, when) in enumerate(DATE_CHECK):
        col, row = divmod(i, 4)
        x = 14 + col * 336
        y = 948 + row * 14
        d.text((x, y), f"{item} \u2014 {when}", font=f_dc, fill=INK)

    # footer
    d.text((8, 1010),
           "Sources: Reuters \u00b7 AP \u00b7 Al Jazeera \u00b7 SCMP \u00b7 Japan Times "
           "\u00b7 AFP \u00b7 The Times \u00b7 CNA \u2014 all stories verified Tue 24 Nov "
           "2026; claims are attributed, not stated as fact.",
           font=f_foot, fill=GREY)
    return img


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "poster.png")
    build().save(out, "PNG")
    print("wrote " + out)


if __name__ == "__main__":
    main()
