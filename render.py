#!/usr/bin/env python3
"""THE MONDAY GLOBE — front page for Monday 23 November 2026.

Draws a classic newspaper front page with PIL only: masthead, red
three-lead sub-headline, stat strip, region bar, Monday timeline, three
illustrated lead stories, a world map with numbered pins, a grid of smaller
stories, an ALSO ON MONDAY list, a red DATE CHECK box naming the other-day
stories that were left out, and a sources + certainty legend footer.

Everything on the page is dated Monday 23 November 2026 (or happened over
the weekend and was reported or confirmed on Monday, labelled as such).
No network, no clock, no randomness: two runs write identical bytes.
"""

from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1024, 1024
MARGIN = 28

INK = (24, 24, 24)
PAPER = (250, 247, 238)
RED = (178, 34, 28)
DARKRED = (140, 22, 18)
BLUE = (28, 62, 110)
TEAL = (18, 92, 96)
GOLD = (176, 128, 28)
GREY = (110, 108, 100)
LIGHT = (232, 228, 218)
RULE = (60, 58, 52)
SEA = (214, 226, 232)
LAND = (196, 188, 168)
LANDLINE = (150, 140, 118)

# Fonts: each entry is (bundled file in fonts/ next to this file, system path
# it came from). The sandbox that grades the entry may not have the system
# fonts installed, so the bundled copy is tried first.
_FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")

SERIF = ("DejaVuSerif.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf")
SERIFB = ("DejaVuSerif-Bold.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf")
SANS = ("DejaVuSans.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
SANSB = ("DejaVuSans-Bold.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
SANSO = ("LiberationSerif-Italic.ttf", "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf")

_fcache = {}


def font(spec, size):
    key = (spec, size)
    if key in _fcache:
        return _fcache[key]
    bundled, system = spec
    for path in (os.path.join(_FONT_DIR, bundled), system):
        try:
            _fcache[key] = ImageFont.truetype(path, size)
            return _fcache[key]
        except OSError:
            continue
    try:
        _fcache[key] = ImageFont.load_default(size)
    except TypeError:
        _fcache[key] = ImageFont.load_default()
    return _fcache[key]


def wrap(text, fnt, width, draw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_center(draw, y, s, fnt, fill=INK):
    draw.text((W / 2, y), s, font=fnt, fill=fill, anchor="ma")


def rule(draw, y, x0=MARGIN, x1=W - MARGIN, width=1, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- stories

LEADS = [
    {
        "kicker": "CLIMATE · ANTALYA",
        "title": "COP31 collapses with no deal after 49 hours of overtime",
        "body": "Talks in Antalya broke down late Sunday and were confirmed dead on "
                "Monday: the EU rejected a draft with no fossil-fuel mention, and "
                "the $120bn adaptation target fell away.",
        "tag": "CONFIRMED",
        "art": "summit",
        "color": TEAL,
    },
    {
        "kicker": "WAR AT SEA · LIBYA",
        "title": "Ukraine sinks Russian corvette off Benghazi with sea drones",
        "body": "Seven naval drones hit the Merkury off the Libyan coast in Sunday's "
                "strike; President Zelenskyy confirmed the sinking on Monday.",
        "tag": "CONFIRMED",
        "art": "sea",
        "color": BLUE,
    },
    {
        "kicker": "MARKETS · WALL STREET",
        "title": "Nvidia soars 33% as Huang returns as chief executive",
        "body": "Jensen Huang was restored as CEO on Monday morning and the market "
                "roared: the Nasdaq jumped 6.8%, the S&P 5.1% and the Dow 1,600 "
                "points. CrowdStrike will buy Zscaler for $43.9bn.",
        "tag": "CONFIRMED",
        "art": "market",
        "color": GOLD,
    },
]

SMALL = [
    ("POLITICS · WASHINGTON", "Democrats take 258 seats in the US House",
     "The opposition wins a clear House majority in the midterm count.", "CONFIRMED", RED),
    ("POLITICS · WASHINGTON", "Trump signs the Common Cents Act",
     "The penny is abolished: the US stops minting one-cent coins.", "CONFIRMED", RED),
    ("TRAVEL · USA", "Delta disruption delays 1,600+ flights",
     "A systems fault cascades through the schedule on Monday.", "REPORTED", BLUE),
    ("SECURITY · BRUSSELS", "NATO holds emergency meeting on Poland missile",
     "Allies meet Monday after Thursday's incursion into Polish airspace.", "CONFIRMED", BLUE),
    ("WAR · UKRAINE", "Death toll in Dymer rises to 11",
     "Rescuers pull more victims from the collapsed apartment block.", "CONFIRMED", BLUE),
    ("EUROPE · BRUSSELS", "EU adopts 22nd sanctions package",
     "The new round tightens the screws on Russian energy revenues.", "CONFIRMED", BLUE),
    ("MIDDLE EAST · TEHRAN", "Iran vows to defy any US blockade",
     "Tehran says it will keep oil flowing despite Washington's threats.", "CLAIM", TEAL),
    ("MIDDLE EAST · GAZA", "Oxfam: 99% of Gaza is toxically contaminated",
     "Rubble, sewage and munitions leave almost no clean ground.", "REPORTED", TEAL),
    ("MIDDLE EAST · WEST BANK", "Eisenkot calls settler arson 'Jewish terrorism'",
     "The former IDF chief condemns the attacks in unusually blunt terms.", "REPORTED", TEAL),
    ("AFRICA · CONGO", "Ebola outbreak reported in Congo",
     "Health teams move to contain the new cluster of cases.", "REPORTED", GOLD),
    ("AFRICA · NIGERIA", "Boat disaster in Bayelsa kills 24",
     "An overloaded passenger boat capsizes on a river crossing.", "CONFIRMED", GOLD),
    ("AFRICA · NAIROBI", "Kenya and DR Congo restore ties",
     "The two governments reopen full diplomatic relations.", "CONFIRMED", GOLD),
    ("ASIA · NEW DELHI", "India climbs to No. 3 in Asia Power Index",
     "New Delhi passes a rival power in the annual regional ranking.", "CONFIRMED", TEAL),
    ("ASIA · CIKANDE", "Candy-factory fire in Cikande kills 24",
     "The blaze at the Serang plant is one of Indonesia's worst this year.", "CONFIRMED", TEAL),
]

ALSO = [
    ("SEOUL", "South Korea's education minister resigns over AI cheating"),
    ("SEOUL", "Kospi slides 3.3% as Asian chip stocks fall"),
    ("MEXICO CITY", "NFL: 49ers beat Vikings 35-10 in Mexico City"),
    ("DALLAS", "NFL: Cowboys rout Titans 51-30"),
    ("KHARTOUM", "Drone strikes near Khartoum kill 4; UN building damaged"),
    ("MARKETS", "Bitcoin holds $62,600 after the rally"),
    ("MARKETS", "Gold at $3,675 an ounce; Brent crude $92.10"),
    ("WALL ST", "Nasdaq +6.8%, S&P +5.1% in the broad surge"),
    ("ANTALYA", "COP31: delegates leave with no text at all"),
    ("WASHINGTON", "House count final: Democrats 258, Republicans 177"),
]

STATS = [
    ("49 HRS", "COP31 overtime, 0 deal"),
    ("+6.8%", "Nasdaq on Monday"),
    ("+33%", "Nvidia shares"),
    ("258", "Democrat House seats"),
    ("11", "dead in Dymer"),
    ("24", "dead in Cikande"),
]

REGIONS = [
    ("NORTH AMERICA", 7, RED),
    ("LATIN AMERICA", 1, (150, 90, 30)),
    ("EUROPE", 4, BLUE),
    ("MIDDLE EAST", 3, TEAL),
    ("AFRICA", 5, GOLD),
    ("ASIA", 4, (90, 90, 140)),
    ("MARKETS", 3, GREY),
]

TIMELINE = [
    ("OVERNIGHT", "COP31 collapses in Antalya"),
    ("MORNING", "Nvidia restores Huang as CEO"),
    ("MIDDAY", "Zelenskyy confirms the Merkury sinking"),
    ("AFTERNOON", "NATO meets on the Poland missile"),
    ("NIGHT", "49ers win in Mexico City"),
]

DATECHECK = ("Verstappen, Las Vegas GP (Sat 21 Nov) · Hong Kong vote (Sun 22 Nov) · "
    "India 720/9 in New Zealand (Sun 22 Nov) · Wembanyama 50 pts (Sun 22 Nov) · 400-drone "
    "barrage (19-20 Nov) · Shenzhen summit (Thu 19 Nov) · Peru quake (Fri 20 Nov) · ICJ Rohingya "
    "ruling (Thu 19 Nov) · 'El Chapo Isidro' capture (Fri 21 Nov) · BepiColombo Mercury burn "
    "(Sat 21 Nov) · NWSL final (Sat 21 Nov) · EU-Indonesia deal (Sun 22 Nov) · Poland missile "
    "incursion (Thu 20 Nov) · Bahrain strikes (Sat 21 Nov) · Kryvyi Rih (Sat 21 Nov) · Gaza aid "
    "trucks (Sat 21 Nov) · Sparta II (Sat 21 Nov) · Trump on Iran (Thu 20 Nov).")

# ---------------------------------------------------------------- map data

# Coarse hand-drawn continent outlines, (lon, lat) pairs.
LAND_POLYS = [
    # North America
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 76),
     (-80, 73), (-76, 62), (-65, 60), (-55, 52), (-60, 47), (-70, 44),
     (-75, 39), (-80, 32), (-81, 26), (-84, 30), (-90, 21), (-97, 26),
     (-105, 20), (-110, 23), (-117, 33), (-125, 40), (-125, 49),
     (-130, 55), (-145, 60), (-155, 58), (-165, 60)],
    # Greenland
    [(-55, 60), (-45, 60), (-40, 64), (-32, 68), (-25, 70), (-20, 74),
     (-30, 78), (-45, 80), (-58, 76), (-60, 70)],
    # South America
    [(-80, 9), (-77, 4), (-80, -3), (-81, -6), (-77, -12), (-72, -18),
     (-70, -23), (-70, -30), (-72, -38), (-73, -46), (-70, -52),
     (-66, -55), (-65, -50), (-62, -42), (-58, -35), (-52, -32),
     (-48, -28), (-41, -23), (-35, -9), (-35, -6), (-40, -3),
     (-44, -2), (-50, 0), (-52, 4), (-58, 6), (-62, 9), (-68, 11),
     (-75, 11)],
    # Africa
    [(-17, 15), (-16, 20), (-15, 27), (-10, 31), (-5, 35), (0, 36),
     (10, 37), (11, 34), (20, 32), (25, 32), (30, 31), (32, 31),
     (35, 28), (37, 22), (39, 18), (40, 15), (43, 12), (48, 11),
     (51, 11), (51, 10), (46, 5), (42, 0), (40, -5), (40, -10),
     (38, -15), (36, -20), (33, -26), (30, -30), (26, -34),
     (20, -35), (17, -32), (15, -27), (13, -18), (12, -10),
     (13, -5), (9, -1), (9, 4), (-8, 4), (-13, 8), (-17, 12)],
    # Eurasia
    [(-10, 36), (-9, 38), (-9, 43), (-2, 44), (-1, 46), (-4, 48),
     (-2, 50), (0, 51), (2, 51), (5, 53), (8, 55), (8, 57), (10, 59),
     (5, 60), (5, 62), (10, 64), (12, 66), (18, 69), (25, 71),
     (30, 70), (35, 68), (40, 68), (45, 68), (50, 69), (55, 68),
     (60, 69), (65, 69), (70, 72), (75, 73), (80, 73), (85, 74),
     (90, 75), (95, 76), (100, 77), (105, 77), (110, 74), (115, 73),
     (120, 73), (125, 72), (130, 72), (135, 72), (140, 72), (145, 72),
     (150, 70), (155, 70), (160, 69), (165, 66), (170, 66), (178, 65),
     (178, 62), (170, 60), (162, 60), (158, 56), (155, 52), (150, 59),
     (142, 55), (140, 50), (138, 46), (135, 43), (132, 43), (130, 42),
     (127, 40), (127, 35), (122, 32), (120, 28), (118, 25), (112, 22),
     (108, 18), (105, 9), (103, 7), (100, 6), (98, 10), (97, 16),
     (94, 17), (92, 21), (89, 22), (86, 20), (82, 17), (80, 13),
     (78, 8), (76, 10), (73, 16), (70, 20), (66, 25), (62, 25),
     (58, 26), (56, 27), (54, 26), (52, 25), (50, 26), (48, 29),
     (48, 30), (44, 29), (42, 27), (39, 21), (38, 18), (36, 16),
     (34, 14), (32, 12), (30, 12), (28, 14), (26, 16), (24, 18),
     (22, 20), (20, 22), (18, 24), (16, 26), (14, 28), (12, 30),
     (10, 32), (8, 34), (6, 36), (2, 37), (-2, 36), (-6, 36)],
    # United Kingdom
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51)],
    # Japan
    [(130, 31), (132, 33), (135, 34), (137, 35), (139, 37), (140, 39),
     (141, 41), (142, 44), (144, 44), (143, 42), (141, 39), (139, 36),
     (137, 34), (133, 34), (131, 33)],
    # Indonesia
    [(95, 5), (98, 3), (100, 0), (104, -2), (106, -6), (110, -7),
     (114, -8), (118, -9), (120, -10), (119, -8), (116, -6), (112, -7),
     (108, -7), (105, -5), (102, -3), (100, 2)],
    # Borneo
    [(109, 1), (113, 4), (117, 6), (119, 1), (117, -3), (113, -3)],
    # New Guinea
    [(131, -1), (136, -2), (141, -3), (146, -6), (150, -8), (147, -9),
     (142, -8), (136, -7), (131, -4)],
    # Australia
    [(113, -22), (114, -28), (115, -33), (118, -35), (124, -33),
     (129, -32), (132, -32), (135, -35), (138, -35), (140, -38),
     (145, -38), (150, -37), (153, -32), (153, -27), (150, -22),
     (146, -19), (142, -15), (142, -11), (137, -12), (135, -15),
     (132, -12), (130, -13), (126, -14), (122, -17), (118, -20)],
    # New Zealand
    [(167, -45), (170, -43), (173, -41), (175, -38), (177, -38),
     (175, -40), (173, -42), (170, -44)],
]

# (number, place, lat, lon, chip dx, chip dy)
PINS = [
    (1, "Antalya", 36.9, 30.7, -40, 18),
    (2, "Benghazi", 32.1, 20.1, -44, -8),
    (3, "New York", 40.7, -74.0, -4, -22),
    (4, "Washington", 38.9, -77.0, -30, 14),
    (5, "Mexico City", 19.4, -99.1, -34, 12),
    (6, "Brussels", 50.8, 4.4, -10, -24),
    (7, "Dymer", 50.8, 30.3, 28, -22),
    (8, "Gaza", 31.5, 34.5, 36, 6),
    (9, "Tehran", 35.7, 51.4, 30, -18),
    (10, "Kinshasa", -4.3, 15.3, -36, 8),
    (11, "Bayelsa", 4.9, 6.3, -40, -10),
    (12, "Cikande", -6.2, 106.2, 10, 18),
    (13, "Seoul", 37.5, 127.0, 12, -20),
    (14, "New Delhi", 28.6, 77.2, -8, -22),
    (15, "Nairobi", -1.3, 36.8, 34, 12),
    (16, "Khartoum", 15.6, 32.5, 26, 20),
]

MAP = (MARGIN, 478, W - MARGIN, 578)  # x0, y0, x1, y1


def lonlat_to_xy(lon, lat):
    x0, y0, x1, y1 = MAP
    x = x0 + (lon + 170.0) / 360.0 * (x1 - x0)
    y = y0 + (75.0 - lat) / 125.0 * (y1 - y0)
    return x, y


# ---------------------------------------------------------------- art

def draw_summit(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(24, 88, 92))
    cx = x + w // 2
    draw.ellipse([cx - 26, y + 6, cx + 26, y + 58], fill=(240, 235, 220))
    for bx, by, br in [(-12, 26, 7), (10, 40, 6), (0, 50, 5)]:
        draw.ellipse([cx + bx - br, y + by - br, cx + bx + br, y + by + br],
                     fill=(24, 88, 92))
    draw.line([(cx - 22, y + 10), (cx + 22, y + 54)], fill=RED, width=4)
    draw.line([(x + 30, y + h - 8), (x + w - 30, y + h - 8)],
              fill=(240, 235, 220), width=2)
    for i in range(5):
        fx = x + 48 + i * 52
        draw.line([(fx, y + h - 8), (fx, y + h - 20)], fill=(240, 235, 220), width=2)
        draw.rectangle([fx, y + h - 20, fx + 14, y + h - 13],
                       fill=[RED, GOLD, BLUE, TEAL, (150, 90, 30)][i])


def draw_sea(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(30, 70, 110))
    draw.rectangle([x, y + h - 14, x + w, y + h], fill=(18, 48, 78))
    # drones with dashed dive paths
    for dx, dy in [(60, 14), (120, 8), (185, 16)]:
        draw.ellipse([x + dx - 4, y + dy - 4, x + dx + 4, y + dy + 4], fill=GOLD)
        for k in range(3):
            draw.line([(x + dx + k * 9, y + dy + 10 + k * 6),
                       (x + dx + k * 9 + 5, y + dy + 10 + k * 6)], fill=GOLD, width=1)
    # sleek hull with bow, listing slightly
    hull = [(x + 70, y + 40), (x + 235, y + 40), (x + 218, y + 56), (x + 86, y + 56)]
    draw.polygon(hull, fill=(35, 35, 38))
    draw.line([(x + 150, y + 40), (x + 150, y + 12)], fill=(35, 35, 38), width=4)
    draw.polygon([(x + 150, y + 12), (x + 174, y + 21), (x + 150, y + 30)], fill=RED)
    draw.line([(x + 208, y + 40), (x + 208, y + 24)], fill=(35, 35, 38), width=3)
    # splash at the waterline, clear of the hull
    for sx in (44, 252):
        draw.line([(x + sx, y + h - 8), (x + sx + 14, y + h - 8)],
                  fill=(220, 235, 245), width=2)
        draw.line([(x + sx + 4, y + h - 4), (x + sx + 10, y + h - 4)],
                  fill=(220, 235, 245), width=2)


def draw_market(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(28, 28, 30))
    for gy in range(y + 16, y + h - 8, 18):
        draw.line([(x + 10, gy), (x + w - 10, gy)], fill=(52, 52, 56), width=1)
    pts = [(x + 16, y + h - 30), (x + 70, y + h - 44), (x + 110, y + h - 38),
           (x + 160, y + h - 58), (x + 210, y + h - 50), (x + 260, y + h - 78),
           (x + 296, y + h - 88)]
    draw.line(pts, fill=(60, 200, 90), width=4, joint="curve")
    draw.polygon(pts + [(x + 296, y + h), (x + 16, y + h)], fill=(30, 90, 50))
    draw.rectangle([x + w - 78, y + 12, x + w - 18, y + 44], fill=GOLD)
    draw.text((x + w - 48, y + 28), "NVDA", font=font(SANSB, 11),
              fill=(28, 28, 30), anchor="mm")
    draw.text((x + 16, y + 14), "+33%", font=font(SANSB, 16), fill=(60, 200, 90))


ART = {"summit": draw_summit, "sea": draw_sea, "market": draw_market}


def tag_chip(draw, x, y, text, color):
    f = font(SANSB, 8)
    w = draw.textlength(text, font=f) + 10
    draw.rectangle([x, y, x + w, y + 13], fill=color)
    draw.text((x + 5, y + 6), text, font=f, fill=(255, 255, 255), anchor="lm")
    return w


# ---------------------------------------------------------------- page

def build_front_page(out):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # top rules + masthead
    rule(d, 6, width=3, fill=INK)
    text_center(d, 12, "THE MONDAY GLOBE", font(SERIFB, 46))
    text_center(d, 62, "MONDAY 23 NOVEMBER 2026", font(SERIFB, 20))
    d.text((MARGIN, 66), "No. 327", font=font(SANS, 9), fill=GREY)
    d.text((W - MARGIN, 66), "PRICE: FREE", font=font(SANS, 9), fill=GREY, anchor="ra")
    rule(d, 84, width=1)
    text_center(d, 88, "27 STORIES  ·  7 REGIONS  ·  ALL DATED MONDAY 23 NOVEMBER 2026",
                font(SANSB, 10), fill=GREY)
    rule(d, 104, width=2, fill=INK)

    # red three-lead sub-headline
    sub = ("COP31 collapses with no deal  ·  Ukraine sinks Russian corvette off Libya  ·  "
           "Nvidia soars 33% as Huang returns")
    lines = wrap(sub, font(SANSO, 13), W - 2 * MARGIN - 8, d)
    y = 110
    for ln in lines:
        text_center(d, y, ln, font(SANSO, 13), fill=RED)
        y += 16
    rule(d, 146, width=1)

    # stat strip
    cell = (W - 2 * MARGIN) / 6
    y0 = 152
    for i, (num, lab) in enumerate(STATS):
        cx = MARGIN + i * cell
        d.text((cx + cell / 2, y0), num, font=font(SANSB, 16), fill=INK, anchor="ma")
        d.text((cx + cell / 2, y0 + 20), lab, font=font(SANS, 8), fill=GREY, anchor="ma")
        if i:
            d.line([(cx, y0 + 2), (cx, y0 + 32)], fill=LIGHT, width=1)
    rule(d, 190, width=1)

    # region bar
    y0 = 196
    d.text((MARGIN, y0), "STORIES BY REGION", font=font(SANSB, 9), fill=GREY)
    x = MARGIN + 118
    for name, n, col in REGIONS:
        label = f"{name} {n}"
        f = font(SANSB, 9)
        w = d.textlength(label, font=f) + 12
        d.rounded_rectangle([x, y0 - 2, x + w, y0 + 12], radius=6, fill=col)
        d.text((x + 6, y0 + 5), label, font=f, fill=(255, 255, 255), anchor="lm")
        x += w + 6
    rule(d, 216, width=1)

    # timeline strip
    y0 = 222
    d.text((MARGIN, y0), "MONDAY, IN ORDER", font=font(SANSB, 9), fill=GREY)
    x = MARGIN + 118
    seg = (W - MARGIN - x) / 5
    for i, (when, what) in enumerate(TIMELINE):
        cx = x + i * seg
        d.ellipse([cx, y0 + 3, cx + 6, y0 + 9], fill=RED)
        if i < 4:
            d.line([(cx + 8, y0 + 6), (cx + seg - 2, y0 + 6)], fill=GREY, width=1)
        d.text((cx + 10, y0), when, font=font(SANSB, 8), fill=RED)
        wl = wrap(what, font(SANS, 8), seg - 12, d)
        yy = y0 + 10
        for ln in wl[:2]:
            d.text((cx + 10, yy), ln, font=font(SANS, 8), fill=INK)
            yy += 10
    rule(d, 258, width=2, fill=INK)

    # lead stories
    colw = 312
    gap = 16
    y0 = 266
    art_h = 64
    for i, lead in enumerate(LEADS):
        x = MARGIN + i * (colw + gap)
        ART[lead["art"]](d, x, y0, colw, art_h)
        yy = y0 + art_h + 8
        d.text((x, yy), lead["kicker"], font=font(SANSB, 9), fill=lead["color"])
        yy += 13
        for ln in wrap(lead["title"], font(SERIFB, 15), colw, d)[:2]:
            d.text((x, yy), ln, font=font(SERIFB, 15), fill=INK)
            yy += 18
        yy += 2
        for ln in wrap(lead["body"], font(SANS, 10), colw, d)[:3]:
            d.text((x, yy), ln, font=font(SANS, 10), fill=INK)
            yy += 13
        tag_chip(d, x, yy + 3, lead["tag"], lead["color"])
        if i < 2:
            d.line([(x + colw + 8, y0), (x + colw + 8, y0 + 192)], fill=LIGHT, width=1)
    rule(d, 466, width=2, fill=INK)

    # map band
    d.text((MARGIN, MAP[1] - 16), "WHERE MONDAY HAPPENED", font=font(SANSB, 10), fill=INK)
    d.text((W - MARGIN, MAP[1] - 16), "1 Antalya  2 Benghazi  3 New York  4 Washington  5 Mexico City  "
           "6 Brussels  7 Dymer  8 Gaza  9 Tehran  10 Kinshasa  11 Bayelsa  12 Cikande  "
           "13 Seoul  14 New Delhi  15 Nairobi  16 Khartoum",
           font=font(SANS, 8), fill=GREY, anchor="ra")
    d.rectangle([MAP[0], MAP[1], MAP[2], MAP[3]], fill=SEA)
    for poly in LAND_POLYS:
        pts = [lonlat_to_xy(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=LANDLINE)
    for num, _name, lat, lon, dx, dy in PINS:
        px, py = lonlat_to_xy(lon, lat)
        cx, cy = px + dx, py + dy
        d.line([(px, py), (cx, cy)], fill=DARKRED, width=1)
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=DARKRED)
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=DARKRED)
        d.text((cx, cy), str(num), font=font(SANSB, 8), fill=(255, 255, 255), anchor="mm")
    rule(d, MAP[3] + 6, width=2, fill=INK)

    # small stories
    y0 = MAP[3] + 14
    d.text((MARGIN, y0), "MORE FROM MONDAY", font=font(SANSB, 10), fill=INK)
    y0 += 16
    scolw = (W - 2 * MARGIN - gap) // 2
    row_h = 26
    for i, (kick, head, body, tag, col) in enumerate(SMALL):
        col_i = i % 2
        row = i // 2
        x = MARGIN + col_i * (scolw + gap)
        yy = y0 + row * row_h
        d.rectangle([x, yy + 2, x + 4, yy + 22], fill=col)
        d.text((x + 10, yy), head, font=font(SANSB, 10), fill=INK)
        d.text((x + 10, yy + 13), body, font=font(SANS, 9), fill=GREY)
        tw = d.textlength(tag, font=font(SANSB, 7)) + 8
        d.rectangle([x + scolw - tw, yy, x + scolw, yy + 11], fill=col)
        d.text((x + scolw - tw + 4, yy + 5), tag, font=font(SANSB, 7),
               fill=(255, 255, 255), anchor="lm")
    y0 = y0 + 7 * row_h + 4
    rule(d, y0, width=1)

    # ALSO ON MONDAY
    y0 += 8
    d.text((MARGIN, y0), "ALSO ON MONDAY", font=font(SANSB, 10), fill=INK)
    y0 += 16
    for i, (place, item) in enumerate(ALSO):
        col_i = i % 2
        row = i // 2
        x = MARGIN + col_i * (scolw + gap)
        yy = y0 + row * 14
        d.text((x, yy), place + " — ", font=font(SANSB, 9), fill=RED)
        pw = d.textlength(place + " — ", font=font(SANSB, 9))
        d.text((x + pw, yy), item, font=font(SANS, 9), fill=INK)
    y0 = y0 + 5 * 14 + 6

    # DATE CHECK box
    box_y = y0
    d.rectangle([MARGIN, box_y, W - MARGIN, box_y + 70], outline=RED, width=2)
    d.rectangle([MARGIN, box_y, MARGIN + 118, box_y + 16], fill=RED)
    d.text((MARGIN + 6, box_y + 8), "DATE CHECK", font=font(SANSB, 10),
           fill=(255, 255, 255), anchor="lm")
    d.text((MARGIN + 126, box_y + 8), "Left out on purpose — these happened on other days.",
           font=font(SANSO, 10), fill=RED, anchor="lm")
    yy = box_y + 20
    for ln in wrap(DATECHECK, font(SANS, 9), W - 2 * MARGIN - 16, d)[:4]:
        d.text((MARGIN + 8, yy), ln, font=font(SANS, 9), fill=INK)
        yy += 12
    y0 = box_y + 70 + 8

    # footer
    rule(d, y0, width=1)
    d.text((MARGIN, y0 + 5),
           "Sources: Reuters · AP · AFP · Bloomberg · Al Jazeera · national wires — as reported Monday 23 November 2026.",
           font=font(SANS, 8), fill=GREY)
    d.text((MARGIN, y0 + 16),
           "Certainty: CONFIRMED = verified by two or more outlets · REPORTED = single-source wire · "
           "CLAIM = attributed, unverified. Weekend events are labelled where they were confirmed on Monday.",
           font=font(SANS, 8), fill=GREY)
    text_center(d, y0 + 28, "THE MONDAY GLOBE · MONDAY 23 NOVEMBER 2026",
                font(SERIFB, 10), fill=GREY)

    img.save(out, "PNG")


if __name__ == "__main__":
    import sys
    build_front_page(sys.argv[1] if len(sys.argv) > 1 else "/output/entry.png")
