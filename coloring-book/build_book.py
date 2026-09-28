"""Build the KDP interior PDF, cover PDF and art prompt list.

    python3 build_book.py

Art: put one image per design in art/ named 01.png ... 30.png (jpg also works)
and the front-cover picture as art/cover.png. Missing images print as a dashed
placeholder box, so the book can be previewed before all art is ready.
"""
import os, re, math
from PIL import Image, ImageOps
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader

from content import BOOK, DESIGNS, BLESSING, STYLE
from verses import verse

HERE = os.path.dirname(os.path.abspath(__file__))
ART, OUT = os.path.join(HERE, "art"), os.path.join(HERE, "output")
TMP = os.path.join(HERE, "build", "art_bw")
for d in (OUT, TMP):
    os.makedirs(d, exist_ok=True)

for name, file in [("Display", "LuckiestGuy-Regular.ttf"), ("Body", "Andika-Regular.ttf"),
                   ("BodyBold", "Andika-Bold.ttf"), ("Hand", "PatrickHand-Regular.ttf")]:
    pdfmetrics.registerFont(TTFont(name, os.path.join(HERE, "fonts", file)))

W, H = 8.5 * inch, 11 * inch
INSIDE, OUTSIDE, TOP, BOTTOM = 0.75 * inch, 0.5 * inch, 0.5 * inch, 0.5 * inch
PAPER_THICKNESS = 0.002252  # inches per page, KDP white paper
GRAY = (0.55, 0.55, 0.55)


# ---------------------------------------------------------------- text helpers
def pretty(s):
    """Straight quotes -> curly apostrophes for print."""
    return s.replace("'", "’")


def verse_text(item):
    """Exact WEB text, divine name shown as 'the LORD', trimmed to the excerpt."""
    b, c, v = item["ref"]
    full = verse(b, c, v).replace("Yahweh", "the LORD")
    full = full.replace("’", "'").replace("‘", "").replace("“", "").replace("”", "")
    full = re.sub(r"\s+", " ", full)
    full = re.sub(r"(^|[.!?:] )the LORD", lambda m: m.group(1) + "The LORD", full)
    ex = item.get("excerpt", full)
    for piece in ex.split(" ... "):
        if piece not in full:
            raise SystemExit(f"Excerpt not found in {item['label']}:\n  {piece!r}\n  in {full!r}")
    text = ex.replace(" ... ", " … ")
    if text[0].islower():
        text = "…" + text
    if text[-1] in ",;:":
        text = text[:-1] + "…"
    return pretty(text)


def wrap(text, font, size, width):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if pdfmetrics.stringWidth(trial, font, size) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_lines(text, font, width, max_size, min_size, max_lines):
    if font == "Display":
        text = text.upper()
    size = max_size
    while size > min_size:
        lines = wrap(text, font, size, width)
        if len(lines) <= max_lines and all(pdfmetrics.stringWidth(l, font, size) <= width for l in lines):
            return lines, size
        size -= 0.5
    return wrap(text, font, min_size, width), min_size


def outline_text(c, lines, font, size, cx, top, leading=1.08, stroke=1.6):
    """Hollow letters kids can color in."""
    c.saveState()
    c.setLineWidth(stroke)
    c.setLineJoin(1)
    y = top - size * 0.82
    lines = [l.upper() for l in lines]
    for line in lines:
        t = c.beginText()
        t.setTextRenderMode(1)
        t.setFont(font, size)
        t.setTextOrigin(cx - pdfmetrics.stringWidth(line, font, size) / 2, y)
        t.textLine(line)
        c.drawText(t)
        y -= size * leading
    c.restoreState()
    return top - size * leading * len(lines)


# ---------------------------------------------------------------- season icons
def icon(c, season, x, y, r):
    """Small outlined season badge (colorable), centered at x, y."""
    c.saveState()
    c.setLineWidth(1.4)
    c.setLineCap(1)
    c.circle(x, y, r * 1.35)
    if season == "winter":                                     # snowflake
        for k in range(6):
            a = math.radians(90 + k * 60)
            ex, ey = x + r * math.cos(a), y + r * math.sin(a)
            c.line(x, y, ex, ey)
            for side in (-1, 1):
                b = a + side * math.radians(40)
                mx, my = x + r * 0.6 * math.cos(a), y + r * 0.6 * math.sin(a)
                c.line(mx, my, mx + r * 0.3 * math.cos(b), my + r * 0.3 * math.sin(b))
    elif season == "spring":                                   # flower
        for k in range(5):
            a = math.radians(90 + k * 72)
            c.circle(x + r * 0.55 * math.cos(a), y + r * 0.55 * math.sin(a), r * 0.38)
        c.setFillColorRGB(1, 1, 1)
        c.circle(x, y, r * 0.28, fill=1)
    elif season == "summer":                                   # sun
        c.circle(x, y, r * 0.45)
        for k in range(8):
            a = math.radians(k * 45)
            c.line(x + r * 0.62 * math.cos(a), y + r * 0.62 * math.sin(a),
                   x + r * 0.95 * math.cos(a), y + r * 0.95 * math.sin(a))
    else:                                                      # leaf
        p = c.beginPath()
        p.moveTo(x - r * 0.8, y - r * 0.8)
        p.curveTo(x - r * 0.9, y + r * 0.4, x + r * 0.2, y + r * 0.9, x + r * 0.85, y + r * 0.85)
        p.curveTo(x + r * 0.9, y - r * 0.2, x - r * 0.3, y - r * 0.9, x - r * 0.8, y - r * 0.8)
        c.drawPath(p)
        c.line(x - r * 0.8, y - r * 0.8, x + r * 0.5, y + r * 0.5)
    c.restoreState()


def margins(page_no):
    """Odd pages are right-hand pages: inside margin on the left."""
    left = INSIDE if page_no % 2 == 1 else OUTSIDE
    right = OUTSIDE if page_no % 2 == 1 else INSIDE
    return left, W - right


# ---------------------------------------------------------------- art
def find_art(stem):
    for ext in (".png", ".jpg", ".jpeg", ".webp"):
        p = os.path.join(ART, stem + ext)
        if os.path.exists(p):
            return p
    return None


def clean_bw(path, threshold=170):
    """Force pure black & white line art (removes gray tints from AI images)."""
    out = os.path.join(TMP, os.path.splitext(os.path.basename(path))[0] + ".png")
    im = Image.open(path).convert("L")
    im = im.point(lambda p: 255 if p > threshold else 0).convert("1")
    im.save(out, dpi=(300, 300))
    return out, im.size


WARNINGS = []


def draw_art(c, stem, x, y, w, h, label, scene, bw=True):
    path = find_art(stem)
    if path:
        img_path, (pw, ph) = clean_bw(path) if bw else (path, Image.open(path).size)
        scale = min(w / pw, h / ph)
        dw, dh = pw * scale, ph * scale
        dpi = pw / (dw / inch)
        if dpi < 250:
            WARNINGS.append(f"{os.path.basename(path)} prints at only {dpi:.0f} DPI "
                            f"(needs ~300; make it at least {int(w / inch * 300)}x{int(h / inch * 300)} px)")
        c.drawImage(ImageReader(img_path), x + (w - dw) / 2, y + (h - dh) / 2, dw, dh)
        return True
    c.saveState()
    c.setStrokeColorRGB(*GRAY)
    c.setDash(6, 5)
    c.roundRect(x, y, w, h, 14)
    c.setFillColorRGB(*GRAY)
    c.setFont("BodyBold", 16)
    c.drawCentredString(x + w / 2, y + h / 2 + 20, label)
    c.setFont("Body", 11)
    for i, line in enumerate(wrap(scene, "Body", 11, w - 60)):
        c.drawCentredString(x + w / 2, y + h / 2 - 4 - i * 14, line)
    c.restoreState()
    return False


# ---------------------------------------------------------------- pages
def blank(c, page_no):
    c.saveState()
    c.setFillColorRGB(0.75, 0.75, 0.75)
    c.setFont("Body", 8)
    c.drawCentredString(W / 2, BOTTOM, "This page is left blank so your markers don't bleed through.")
    c.restoreState()
    c.showPage()


def title_page(c):
    x0, x1 = margins(1)
    cx = (x0 + x1) / 2
    y = outline_text(c, [BOOK["title"]], "Display", 50, cx, H - 2.6 * inch, stroke=2)
    c.setFont("Body", 17)
    for i, l in enumerate(wrap(BOOK["subtitle"], "Body", 17, x1 - x0 - 60)):
        c.drawCentredString(cx, y - 30 - i * 22, l)
    c.setFont("BodyBold", 14)
    c.drawCentredString(cx, y - 100, BOOK["ages"])
    for k, s in enumerate(["winter", "spring", "summer", "fall"]):
        icon(c, s, cx + (k - 1.5) * 70, H / 2 - 40, 18)
    c.setFont("Body", 14)
    c.drawCentredString(cx, 1.6 * inch, "by " + BOOK["author"])
    c.showPage()


def copyright_page(c):
    x0, x1 = margins(2)
    lines = [
        f"{BOOK['title']}: {BOOK['subtitle']}",
        f"Copyright © {BOOK['year']} {BOOK['author']}. All rights reserved.",
        "",
        "No part of this book may be reproduced without written permission from the",
        "author, except that parents and teachers may copy pages for use at home or in class.",
        "",
        "Scripture quotations are from the World English Bible (public domain),",
        "with the divine name shown as “the LORD.” Some verses are shortened for young readers.",
        "",
        "Illustrations created with AI assistance and reviewed by the author.",
    ]
    c.setFont("Body", 9.5)
    y = 2.6 * inch
    for l in lines:
        c.drawString(x0, y, pretty(l))
        y -= 13
    c.showPage()


def belongs_page(c, page_no):
    x0, x1 = margins(page_no)
    cx = (x0 + x1) / 2
    y = outline_text(c, ["This book", "belongs to"], "Display", 54, cx, H - 2 * inch, stroke=2)
    c.setLineWidth(1.5)
    c.line(x0 + 50, y - 90, x1 - 50, y - 90)
    c.setFont("Hand", 20)
    c.drawCentredString(cx, y - 150, pretty("I am a child of God, made in His image!"))
    c.setFont("Body", 11)
    c.drawCentredString(cx, y - 172, "(1 John 3:1)")
    # frame to draw a self-portrait
    c.setFont("BodyBold", 13)
    c.drawCentredString(cx, 3.9 * inch, "Draw yourself here!")
    c.roundRect(cx - 1.6 * inch, 0.9 * inch, 3.2 * inch, 2.8 * inch, 16)
    c.showPage()


def grownups_page(c, page_no):
    x0, x1 = margins(page_no)
    cx = (x0 + x1) / 2
    y = outline_text(c, ["A note for", "grown-ups"], "Display", 40, cx, H - 1.4 * inch)
    text = [
        "Children begin forming beliefs about who they are very early. This book helps them "
        "build confidence on the truest foundation there is: God created them in His image, "
        "loves them, and made them on purpose (Genesis 1:27).",
        "The book follows the seasons of the year, from winter to fall. Each page has a Bible "
        "truth in big letters for your child to color, a Bible verse to read together, a "
        "picture of kids at school, at home, at the park and out in the neighborhood, and a "
        "few lines for notes.",
        "Ideas for using it:",
        "•  Color one page a week and read its verse out loud together each day.",
        "•  Ask: “When could you remember this truth this week?” Write the answer on the note lines.",
        "•  Let younger children dictate their thoughts while you write them down.",
        "•  Use crayons or colored pencils. With markers, slip a sheet of paper behind the page.",
    ]
    c.setFont("Body", 13)
    y -= 20
    for para in text:
        for l in wrap(pretty(para), "Body", 13, x1 - x0 - 20):
            c.drawString(x0 + 10, y, l)
            y -= 18
        y -= 10
    c.showPage()


def design_page(c, page_no, n, d):
    x0, x1 = margins(page_no)
    cx, width = (x0 + x1) / 2, x1 - x0
    top = H - TOP

    # season badge + design number
    icon(c, d["season"], x1 - 22, top - 22, 14)
    c.setFont("Body", 9)
    c.setFillColorRGB(*GRAY)
    c.drawString(x0, top - 10, f"{n} of {len(DESIGNS)}")
    c.setFillColorRGB(0, 0, 0)

    # truth headline (hollow letters to color)
    lines, size = fit_lines(pretty(d["truth"]), "Display", width - 110, 38, 26, 2)
    y = outline_text(c, lines, "Display", size, cx, top - 4)

    # verse + notes from the bottom up
    notes_h, n_lines = 88, 3
    notes_y = BOTTOM
    c.setFont("Hand", 15)
    c.drawString(x0 + 4, notes_y + notes_h - 16, "What this truth means to me:")
    c.setLineWidth(0.8)
    for i in range(n_lines):
        ly = notes_y + notes_h - 42 - i * 22
        c.line(x0 + 4, ly, x1 - 4, ly)

    vtext = verse_text(d)
    vlines, vsize = fit_lines("“" + vtext + "”", "Body", width - 40, 14, 11, 3)
    box_h = len(vlines) * vsize * 1.3 + vsize + 22
    box_y = notes_y + notes_h + 10
    c.setLineWidth(1.4)
    c.roundRect(x0, box_y, width, box_h, 12)
    ty = box_y + box_h - 12 - vsize
    c.setFont("Body", vsize)
    for l in vlines:
        c.drawCentredString(cx, ty, l)
        ty -= vsize * 1.3
    c.setFont("BodyBold", vsize)
    c.drawCentredString(cx, ty - 2, "— " + d["label"])

    # art fills the middle
    art_top, art_bottom = y - 8, box_y + box_h + 12
    draw_art(c, f"{n:02d}", x0, art_bottom, width, art_top - art_bottom,
             f"Design {n}: place art/{n:02d}.png here", d["scene"])
    c.showPage()
    return (width / inch, (art_top - art_bottom) / inch)


def blessing_page(c, page_no):
    x0, x1 = margins(page_no)
    cx = (x0 + x1) / 2
    c.setLineWidth(3)
    c.roundRect(x0, BOTTOM, x1 - x0, H - TOP - BOTTOM, 24)
    c.setLineWidth(1)
    c.roundRect(x0 + 10, BOTTOM + 10, x1 - x0 - 20, H - TOP - BOTTOM - 20, 18)
    y = outline_text(c, ["I finished my", "coloring book!"], "Display", 44, cx, H - 1.5 * inch, stroke=2)
    c.setFont("Hand", 20)
    c.drawCentredString(cx, y - 40, "Presented to")
    c.line(x0 + 80, y - 90, x1 - 80, y - 90)
    c.setFont("Body", 14)
    for i, l in enumerate(wrap(pretty("You are made in God’s image, wonderfully made, "
                                      "and loved by Him every season of the year."),
                               "Body", 14, x1 - x0 - 120)):
        c.drawCentredString(cx, y - 140 - i * 20, l)
    for k, s in enumerate(["winter", "spring", "summer", "fall"]):
        icon(c, s, cx + (k - 1.5) * 70, H / 2 - 50, 18)
    c.setFont("BodyBold", 18)
    c.drawCentredString(cx, 3.3 * inch, "“" + verse_text(BLESSING) + "”")
    c.setFont("Body", 13)
    c.drawCentredString(cx, 3.3 * inch - 22, "— " + BLESSING["label"])
    c.setFont("Hand", 16)
    c.drawString(x0 + 50, 1.5 * inch, "Date: ______________")
    c.drawRightString(x1 - 50, 1.5 * inch, "Signed: ______________")
    c.showPage()


# ---------------------------------------------------------------- builders
def build_interior():
    path = os.path.join(OUT, "interior.pdf")
    c = canvas.Canvas(path, pagesize=(W, H))
    c.setTitle(BOOK["title"])
    c.setAuthor(BOOK["author"])
    title_page(c)                        # p1
    copyright_page(c)                    # p2
    belongs_page(c, 3)                   # p3
    blank(c, 4)                          # p4
    grownups_page(c, 5)                  # p5
    blank(c, 6)                          # p6
    page = 7
    art_size = None
    for n, d in enumerate(DESIGNS, 1):   # every design on a right-hand page, blank back
        art_size = design_page(c, page, n, d)
        blank(c, page + 1)
        page += 2
    blessing_page(c, page)
    blank(c, page + 1)
    page += 1
    c.save()
    return path, page, art_size


def build_cover(pages):
    bleed = 0.125
    spine = pages * PAPER_THICKNESS
    cw, ch = (2 * 8.5 + spine + 2 * bleed) * inch, (11 + 2 * bleed) * inch
    path = os.path.join(OUT, "cover.pdf")
    c = canvas.Canvas(path, pagesize=(cw, ch))
    front_x = (bleed + 8.5 + spine) * inch
    safe = 0.375 * inch
    c.setFillColorRGB(0.99, 0.91, 0.94)   # soft pink background, full bleed
    c.rect(0, 0, cw, ch, stroke=0, fill=1)
    c.setFillColorRGB(0, 0, 0)

    # front cover: full-color art if supplied, title on top
    fx0, fx1 = front_x + safe, front_x + 8.5 * inch - safe
    fcx = (fx0 + fx1) / 2
    draw_art(c, "cover", fx0, 1.3 * inch, fx1 - fx0, 6.4 * inch,
             "Front cover art: place art/cover.png here",
             "full-color picture of smiling girls and boys playing together outdoors", bw=False)
    c.setFillColorRGB(0, 0, 0)
    tlines, tsize = fit_lines(BOOK["title"], "Display", fx1 - fx0, 64, 40, 2)
    y = ch - bleed * inch - 0.7 * inch
    for l in tlines:
        c.setFont("Display", tsize)
        c.drawCentredString(fcx, y - tsize * 0.8, l)
        y -= tsize * 1.05
    c.setFont("BodyBold", 17)
    for l in wrap(BOOK["subtitle"], "BodyBold", 17, fx1 - fx0 - 40):
        c.drawCentredString(fcx, y - 22, l)
        y -= 22
    c.setFont("BodyBold", 16)
    c.drawCentredString(fcx, 0.95 * inch, f"30 Bible Truth Coloring Pages  •  {BOOK['ages']}")

    # back cover
    bx0, bx1 = (bleed * inch) + safe, (bleed + 8.5) * inch - safe
    bcx = (bx0 + bx1) / 2
    c.setFont("Display", 30)
    c.drawCentredString(bcx, ch - 1.4 * inch, "Made on purpose. Loved by God.")
    blurb = ("Help your child grow in confidence rooted in God's truth! Every page pairs a "
             "Bible truth in big letters to color with a real Bible verse, a joyful picture of "
             "kids at school, at the park, riding bikes, playing sports and around the "
             "neighborhood, and lines to write what the truth means to them. The pages follow "
             "the seasons of the year, from snowy winter to pumpkin-picking fall.")
    c.setFont("Body", 14)
    y = ch - 2.1 * inch
    for l in wrap(pretty(blurb), "Body", 14, bx1 - bx0 - 30):
        c.drawCentredString(bcx, y, l)
        y -= 20
    y -= 16
    for b in ["30 single-sided designs, so markers won't bleed onto the next picture",
              "Big 8.5 x 11 inch pages",
              "Girls and boys at school, in the park and around the neighborhood",
              "Space for notes on every page",
              "A “this book belongs to” page and a completion certificate"]:
        c.drawString(bx0 + 40, y, "•  " + pretty(b))
        y -= 22
    c.setFont("Hand", 18)
    c.drawCentredString(bcx, y - 20, pretty("“I am fearfully and wonderfully made.” — Psalm 139:14"))
    # KDP places the barcode here (bottom right of back cover), keep it empty
    c.saveState()
    c.setFillColorRGB(1, 1, 1)
    c.setStrokeColorRGB(*GRAY)
    c.setDash(4, 4)
    bw_, bh_ = 2 * inch, 1.2 * inch
    c.rect(bx1 - bw_, 0.25 * inch + bleed * inch, bw_, bh_, fill=1)
    c.setFillColorRGB(*GRAY)
    c.setFont("Body", 8)
    c.drawCentredString(bx1 - bw_ / 2, 0.25 * inch + bleed * inch + bh_ / 2, "KDP barcode area (leave empty)")
    c.restoreState()
    c.save()
    return path, spine, cw / inch, ch / inch


def build_prompts(art_size):
    aw, ah = art_size
    ratio = f"{aw / ah:.2f}:1 (about {round(aw * 10)}:{round(ah * 10)})"
    out = [f"# Art prompts for “{BOOK['title']}”", "",
           f"Make each image landscape, ratio about {ratio}. The picture area is "
           f"{aw:.1f} x {ah:.1f} inches, so aim for at least {int(aw * 300)} x {int(ah * 300)} pixels "
           "(upscale if your tool makes smaller images).",
           "Save them as `art/01.png` ... `art/30.png`, then rebuild the book.", "",
           "Check every image: 5 fingers per hand, two feet, eyes and faces look right, "
           "no gray shading, no stray text or letters.", "",
           "**Style (already added to every prompt below):**", "", f"> {STYLE}", ""]
    season = None
    for n, d in enumerate(DESIGNS, 1):
        if d["season"] != season:
            season = d["season"]
            out += [f"## {season.title()}", ""]
        out += [f"### {n:02d}. {pretty(d['truth'])} ({d['label']})", "",
                "```", f"{d['scene']}, {season} season, {STYLE}", "```", ""]
    out += ["## Front cover (full color)", "",
            "```",
            "bright cheerful full-color children's book cover illustration, diverse smiling girls "
            "and boys playing together outdoors, riding bikes, playing ball, flying a kite, "
            "sunny park and neighborhood, soft sky with a few clouds, empty sky area at the top "
            "for a title, no text, no words, cute cartoon style, correct anatomy",
            "```", ""]
    path = os.path.join(HERE, "ART_PROMPTS.md")
    open(path, "w").write("\n".join(out))
    return path


if __name__ == "__main__":
    interior, pages, art_size = build_interior()
    cover, spine, cw, ch = build_cover(pages)
    prompts = build_prompts(art_size)
    have = sum(1 for n in range(1, len(DESIGNS) + 1) if find_art(f"{n:02d}"))
    print(f"interior: {interior}  ({pages} pages)")
    print(f"cover:    {cover}  ({cw:.3f} x {ch:.3f} in, spine {spine:.3f} in)")
    print(f"prompts:  {prompts}")
    print(f"art found: {have}/{len(DESIGNS)} designs, cover: {'yes' if find_art('cover') else 'no'}")
    for w in WARNINGS:
        print("WARNING:", w)
