#!/usr/bin/env python3
"""Generate the SVG diagrams in docs/assets/diagrams/.

Run from the repo root:  python3 scripts/build_diagrams.py

Style rules (keep them when adding diagrams):
- Grayscale only, so pages print cleanly on any printer.
- Every SVG has its own opaque white background, so it reads the same in
  the site's light and dark themes.
- Mock frames are 16:9 (960x540). The tag in the top-left corner uses the
  exact names from the Stream Deck and SuperJoy labels.
- No real lyrics, names or church details. Unknown values say "TBD".
"""

from math import cos, radians, sin
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "docs" / "assets" / "diagrams"

# ---------- Palette (grayscale) ----------
INK = "#1a1a1a"     # text, outlines
DARK = "#4d4d4d"    # people
MID = "#808080"     # objects, secondary text
SOFT = "#b3b3b3"    # props, stage face
LINE = "#cccccc"    # guides
FILL = "#e0e0e0"    # stage, slide background
PALE = "#f0f0f0"    # back wall
PAPER = "#ffffff"
FONT = "'Segoe UI', Roboto, Helvetica, Arial, sans-serif"

W, H = 960, 540


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def svg(width, height, title, desc, body, defs=""):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" role="img" aria-labelledby="t d" font-family="{FONT}">
<title id="t">{esc(title)}</title>
<desc id="d">{esc(desc)}</desc>
<defs>
<marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{INK}"/></marker>
<marker id="arrow-mid" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{MID}"/></marker>
<filter id="blur" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="12"/></filter>
<clipPath id="frame"><rect width="{W}" height="{H}"/></clipPath>
{defs}</defs>
{body}
</svg>
"""


def text(x, y, s, size=20, weight="normal", fill=INK, anchor="start", extra=""):
    return (f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}" {extra}>{esc(s)}</text>')


def text_w(s, size):
    """Rough text width for sizing boxes (no font metrics available)."""
    return len(s) * size * 0.55


def chip(x, y, s, size=18, anchor="start"):
    """A white label box, readable on top of any frame content."""
    w = text_w(s, size) + 24
    h = size + 16
    if anchor == "end":
        x -= w
    elif anchor == "middle":
        x -= w / 2
    return (f'<rect x="{x:.0f}" y="{y}" width="{w:.0f}" height="{h}" rx="6" fill="{PAPER}" '
            f'fill-opacity="0.94" stroke="{INK}" stroke-width="1.5"/>'
            + text(x + 12, y + size + 3, s, size))


def tag(s):
    """Dark name tag in the top-left corner of a mock frame."""
    w = text_w(s, 22) + 28
    return (f'<rect x="16" y="16" width="{w:.0f}" height="40" rx="6" fill="{INK}"/>'
            + text(30, 44, s, 22, "bold", PAPER))


# ---------- Shapes ----------

def person(cx, top, h, fill=DARK):
    """Standing figure, facing the camera. `top` is the top of the head, `h` the full height."""
    r = 0.06 * h
    def p(dx, dy):
        return f"{cx + dx * h:.1f},{top + dy * h:.1f}"
    body = (f"M{p(-0.035, 0.11)} L{p(0.035, 0.11)} L{p(0.04, 0.135)} "
            f"Q{p(0.135, 0.14)} {p(0.145, 0.21)} L{p(0.155, 0.50)} L{p(0.105, 0.52)} "
            f"L{p(0.095, 1.0)} L{p(0.02, 1.0)} L{p(0, 0.57)} L{p(-0.02, 1.0)} L{p(-0.095, 1.0)} "
            f"L{p(-0.105, 0.52)} L{p(-0.155, 0.50)} L{p(-0.145, 0.21)} Q{p(-0.135, 0.14)} {p(-0.04, 0.135)} Z")
    return (f'<circle cx="{cx:.1f}" cy="{top + r:.1f}" r="{r:.1f}" fill="{fill}"/>'
            f'<path d="{body}" fill="{fill}"/>')


def seated(cx, cy, s, fill=DARK):
    """Head and shoulders of a seated person (congregation), seen from the front."""
    return (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{0.45 * s:.1f}" fill="{fill}"/>'
            f'<path d="M{cx - s:.1f},{cy + 1.9 * s:.1f} Q{cx - s:.1f},{cy + 0.55 * s:.1f} {cx:.1f},{cy + 0.55 * s:.1f} '
            f'Q{cx + s:.1f},{cy + 0.55 * s:.1f} {cx + s:.1f},{cy + 1.9 * s:.1f} Z" fill="{fill}"/>')


def lectern(cx, top, w, h):
    lip = 0.12 * h
    return (f'<path d="M{cx - 0.42 * w:.1f},{top + lip:.1f} L{cx + 0.42 * w:.1f},{top + lip:.1f} '
            f'L{cx + 0.34 * w:.1f},{top + h:.1f} L{cx - 0.34 * w:.1f},{top + h:.1f} Z" '
            f'fill="{SOFT}" stroke="{DARK}" stroke-width="2"/>'
            f'<rect x="{cx - w / 2:.1f}" y="{top:.1f}" width="{w:.1f}" height="{lip:.1f}" rx="3" '
            f'fill="{SOFT}" stroke="{DARK}" stroke-width="2"/>')


def mic_stand(x, top, bottom, s=1.0):
    return (f'<line x1="{x}" y1="{top}" x2="{x}" y2="{bottom}" stroke="{INK}" stroke-width="{3 * s:.1f}"/>'
            f'<line x1="{x}" y1="{top}" x2="{x - 30 * s:.1f}" y2="{top - 14 * s:.1f}" stroke="{INK}" stroke-width="{3 * s:.1f}"/>'
            f'<circle cx="{x - 32 * s:.1f}" cy="{top - 15 * s:.1f}" r="{6 * s:.1f}" fill="{INK}"/>')


def drums(cx, base, s=1.0):
    def c(dx, dy, r, f=PAPER):
        return (f'<ellipse cx="{cx + dx * s:.1f}" cy="{base + dy * s:.1f}" rx="{r * s:.1f}" ry="{r * s:.1f}" '
                f'fill="{f}" stroke="{DARK}" stroke-width="{2.5 * s:.1f}"/>')
    cym = lambda dx, dy: (f'<line x1="{cx + (dx - 40) * s:.1f}" y1="{base + dy * s:.1f}" x2="{cx + (dx + 40) * s:.1f}" '
                          f'y2="{base + (dy - 6) * s:.1f}" stroke="{DARK}" stroke-width="{4 * s:.1f}"/>'
                          f'<line x1="{cx + dx * s:.1f}" y1="{base + (dy - 3) * s:.1f}" x2="{cx + dx * s:.1f}" y2="{base:.1f}" '
                          f'stroke="{MID}" stroke-width="{2 * s:.1f}"/>')
    return (cym(-95, -150) + cym(95, -165)
            + c(0, -55, 55, FILL) + c(-48, -125, 24) + c(48, -128, 24) + c(-90, -60, 26))


def keyboard(cx, top, s=1.0):
    w = 170 * s
    return (f'<line x1="{cx - 0.35 * w:.1f}" y1="{top:.1f}" x2="{cx - 0.25 * w:.1f}" y2="{top + 110 * s:.1f}" stroke="{MID}" stroke-width="{4 * s:.1f}"/>'
            f'<line x1="{cx + 0.35 * w:.1f}" y1="{top:.1f}" x2="{cx + 0.25 * w:.1f}" y2="{top + 110 * s:.1f}" stroke="{MID}" stroke-width="{4 * s:.1f}"/>'
            f'<rect x="{cx - w / 2:.1f}" y="{top - 16 * s:.1f}" width="{w:.1f}" height="{18 * s:.1f}" rx="3" fill="{INK}"/>')


def table(cx, top, w, h):
    """Communion table with a cloth and a few plates/cups."""
    items = ""
    for i, dx in enumerate((-0.32, -0.12, 0.12, 0.32)):
        x = cx + dx * w
        if i % 2 == 0:
            items += f'<ellipse cx="{x:.1f}" cy="{top - 0.04 * h:.1f}" rx="{0.08 * w:.1f}" ry="{0.05 * h:.1f}" fill="{MID}"/>'
        else:
            items += f'<path d="M{x - 0.03 * w:.1f},{top - 0.22 * h:.1f} L{x + 0.03 * w:.1f},{top - 0.22 * h:.1f} L{x + 0.022 * w:.1f},{top:.1f} L{x - 0.022 * w:.1f},{top:.1f} Z" fill="{MID}"/>'
    return (f'<rect x="{cx - w / 2:.1f}" y="{top:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{SOFT}" stroke="{DARK}" stroke-width="2"/>'
            f'<rect x="{cx - 0.22 * w:.1f}" y="{top:.1f}" width="{0.44 * w:.1f}" height="{0.75 * h:.1f}" fill="{PAPER}" stroke="{DARK}" stroke-width="2"/>'
            f'<line x1="{cx - 0.2 * w:.1f}" y1="{top + 0.55 * h:.1f}" x2="{cx + 0.2 * w:.1f}" y2="{top + 0.55 * h:.1f}" stroke="{MID}" stroke-width="2"/>'
            + items)


def guides():
    """Rule-of-thirds lines, so readers can see where the subject sits."""
    d = ""
    for x in (W / 3, 2 * W / 3):
        d += f'<line x1="{x:.0f}" y1="0" x2="{x:.0f}" y2="{H}" stroke="{MID}" stroke-width="1.5" stroke-dasharray="6 8" opacity="0.6"/>'
    for y in (H / 3, 2 * H / 3):
        d += f'<line x1="0" y1="{y:.0f}" x2="{W}" y2="{y:.0f}" stroke="{MID}" stroke-width="1.5" stroke-dasharray="6 8" opacity="0.6"/>'
    return d


def headroom(x, head_top, label="Headroom"):
    """Bracket from the top of the frame to the top of the head."""
    return (f'<line x1="{x}" y1="4" x2="{x}" y2="{head_top}" stroke="{INK}" stroke-width="2.5" '
            f'marker-start="url(#arrow)" marker-end="url(#arrow)"/>'
            f'<line x1="{x - 60}" y1="{head_top}" x2="{x + 12}" y2="{head_top}" stroke="{INK}" stroke-width="1.5" stroke-dasharray="4 4"/>'
            + chip(x + 16, max(head_top / 2 - 17, 6), label, 16))


# ---------- Camera views (shared by presets and scenes) ----------

def front_stage(floor=380, edge=440):
    """Cam 1 background: back wall, stage top, stage front."""
    return (f'<rect width="{W}" height="{H}" fill="{PALE}"/>'
            f'<rect y="{floor}" width="{W}" height="{edge - floor}" fill="{FILL}"/>'
            f'<rect y="{edge}" width="{W}" height="40" fill="{SOFT}"/>'
            f'<rect y="{edge + 40}" width="{W}" height="{H - edge - 40}" fill="{PAPER}"/>')


def side_stage(y_left=470, y_right=330):
    """Cam 2 background: the stage edge runs at an angle because Cam 2 is off to the side."""
    return (f'<rect width="{W}" height="{H}" fill="{PALE}"/>'
            f'<path d="M0,{y_left - 140} L{W},{y_right - 120} L{W},{y_right} L0,{y_left} Z" fill="{FILL}"/>'
            f'<path d="M0,{y_left} L{W},{y_right} L{W},{y_right + 34} L0,{y_left + 44} Z" fill="{SOFT}"/>'
            f'<path d="M0,{y_left + 44} L{W},{y_right + 34} L{W},{H} L0,{H} Z" fill="{PAPER}"/>')


def view_cam1_p1():
    return (front_stage(300, 400)
            + drums(760, 330, 0.6) + person(660, 200, 150) + keyboard(860, 270, 0.6) + person(860, 210, 130)
            + person(330, 190, 160) + mic_stand(350, 230, 345, 0.7)
            + person(480, 205, 150) + lectern(480, 255, 70, 95)
            + table(480, 470, 150, 60))


def view_cam1_p2():
    return front_stage(470, 520) + person(480, 70, 980) + mic_stand(560, 210, 560, 1.4)


def view_cam1_p3():
    return front_stage(560, 600) + person(480, 85, 1500) + lectern(480, 410, 440, 300) + mic_stand(560, 360, 420, 1.1)


def view_cam1_p4():
    return front_stage(420, 480) + person(480, 95, 600)


def view_cam2_p1():
    return (side_stage(430, 300)
            + person(250, 175, 165) + mic_stand(270, 215, 340, 0.7)
            + person(470, 160, 150) + lectern(495, 210, 64, 92)
            + drums(730, 278, 0.5) + person(640, 155, 120) + keyboard(860, 235, 0.5) + person(860, 160, 110))


def view_cam2_p2():
    return (side_stage(560, 470)
            + drums(470, 455, 1.15) + person(250, 90, 400) + mic_stand(300, 175, 490, 1.2)
            + person(760, 110, 350) + keyboard(760, 330, 1.3))


def view_cam2_p3():
    return side_stage(520, 420) + person(280, 60, 430) + lectern(395, 230, 120, 270) + mic_stand(370, 205, 240, 0.9)


def view_cam2_p4():
    return side_stage(420, 360) + person(330, 60, 420) + person(640, 70, 400) + table(480, 300, 640, 200)


def view_cam2_p5():
    rows = ""
    for r, (y, s, n) in enumerate(((130, 13, 15), (195, 17, 12), (275, 22, 10), (375, 28, 8), (490, 36, 6))):
        pew_y = y + 1.4 * s
        rows += f'<rect x="-20" y="{pew_y:.0f}" width="{W + 40}" height="{s * 1.6:.0f}" fill="{SOFT}"/>'
        step = W / n
        for i in range(n):
            if (i + r) % 4 == 3:
                continue
            rows += seated(step * (i + 0.5) + (r % 2) * step / 3, y, s)
    return f'<rect width="{W}" height="{H}" fill="{PALE}"/>' + rows


# ---------- Mock frames ----------

def frame(fname, name, title, desc, view, overlay=""):
    body = (f'<rect width="{W}" height="{H}" fill="{PAPER}"/>'
            f'<g clip-path="url(#frame)">{view}{overlay}</g>'
            + tag(name)
            + f'<rect x="1.5" y="1.5" width="{W - 3}" height="{H - 3}" fill="none" stroke="{INK}" stroke-width="3"/>')
    (OUT / fname).write_text(svg(W, H, title, desc, body))


PRESETS = [
    ("cam1-p1.svg", "Cam 1 P1", "Full stage wide (safe shot)", view_cam1_p1,
     chip(944, 482, "Whole stage in frame — the safe shot", anchor="end")),
    ("cam1-p2.svg", "Cam 1 P2", "Worship leader, medium", view_cam1_p2,
     headroom(640, 70) + chip(944, 482, "Medium: waist up", anchor="end")),
    ("cam1-p3.svg", "Cam 1 P3", "Pulpit, upper body (sermon front)", view_cam1_p3,
     headroom(640, 85) + chip(944, 482, "Upper body: chest up, behind pulpit", anchor="end")),
    ("cam1-p4.svg", "Cam 1 P4", "Announcements spot", view_cam1_p4,
     headroom(640, 95) + chip(944, 482, "Medium wide: knees up", anchor="end")),
    ("cam2-p1.svg", "Cam 2 P1", "Side wide of stage (safe shot)", view_cam2_p1,
     chip(944, 482, "Whole stage from the left side", anchor="end")),
    ("cam2-p2.svg", "Cam 2 P2", "Band / instruments", view_cam2_p2,
     chip(944, 482, "Band and instruments", anchor="end")),
    ("cam2-p3.svg", "Cam 2 P3", "Pulpit, full body, subject framed left", view_cam2_p3,
     headroom(370, 60)
     + f'<rect x="510" y="90" width="420" height="300" rx="8" fill="none" stroke="{INK}" stroke-width="2.5" stroke-dasharray="12 8"/>'
     + text(720, 225, "Keep this side empty:", 22, "bold", INK, "middle")
     + text(720, 257, "the slide goes here in", 20, "normal", INK, "middle")
     + text(720, 287, "Scene 7 — Sermon Split", 20, "bold", INK, "middle")
     + chip(944, 482, "Full body, subject on the left third", anchor="end")),
    ("cam2-p4.svg", "Cam 2 P4", "Communion table", view_cam2_p4,
     chip(944, 482, "Communion table fills the frame", anchor="end")),
    ("cam2-p5.svg", "Cam 2 P5", "Congregation wide (used only blurred)", view_cam2_p5,
     chip(944, 482, "Used only blurred, in Scene 8 — Break", anchor="end")),
]


def slide_full(lines, big=None, small=None):
    """A ProPresenter slide filling the whole frame."""
    d = f'<rect width="{W}" height="{H}" fill="{FILL}"/>'
    d += f'<rect x="40" y="76" width="{W - 80}" height="{H - 116}" rx="10" fill="none" stroke="{MID}" stroke-width="2"/>'
    y = 200 if big else 190
    for s in lines:
        d += text(W / 2, y, s, 36, "bold", INK, "middle")
        y += 52
    if big:
        d += text(W / 2, y + 90, big, 120, "bold", INK, "middle")
    if small:
        for i, s in enumerate(small):
            d += f'<rect x="{W / 2 - 220}" y="{y + 10 + i * 40}" width="{440 - i * 90}" height="18" rx="9" fill="{SOFT}"/>'
    return d


def lyrics_bar():
    """Lower-third lyrics overlay from ProPresenter."""
    top = 2 * H / 3
    return (f'<rect y="{top:.0f}" width="{W}" height="{H - top:.0f}" fill="{INK}" fill-opacity="0.78"/>'
            + text(W / 2, top + 68, "Lyrics line 1", 36, "bold", PAPER, "middle")
            + text(W / 2, top + 122, "Lyrics line 2", 36, "bold", PAPER, "middle"))


def sermon_slide():
    """The slide box on the right side of Scene 7 — Sermon Split."""
    return (f'<rect x="490" y="96" width="440" height="248" rx="6" fill="{FILL}" stroke="{INK}" stroke-width="3"/>'
            + text(710, 170, "Sermon slide", 30, "bold", INK, "middle")
            + f'<rect x="560" y="200" width="300" height="16" rx="8" fill="{SOFT}"/>'
            + f'<rect x="560" y="232" width="240" height="16" rx="8" fill="{SOFT}"/>'
            + f'<rect x="560" y="264" width="270" height="16" rx="8" fill="{SOFT}"/>')


def scene_frames():
    lyric_note = chip(944, 312, "Lyrics: lower third only", anchor="end")
    split = (sermon_slide()
             + chip(710, 360, "ProPresenter Slides", anchor="middle")
             + chip(24, 482, "Cam 2 P3 — subject on the left"))
    brk = (f'<rect x="200" y="150" width="560" height="250" rx="12" fill="{PAPER}" fill-opacity="0.82" stroke="{INK}" stroke-width="2"/>'
           + text(480, 215, "Break slide overlay", 30, "bold", INK, "middle")
           + text(480, 255, "(with countdown)", 22, "normal", INK, "middle")
           + text(480, 360, "04:59", 90, "bold", INK, "middle")
           + chip(24, 482, "Cam 2 P5 — blurred"))
    return [
        ("scene-1-countdown.svg", "Scene 1 — Countdown",
         "ProPresenter Slides, full screen (countdown)",
         slide_full(["Countdown slide"], "04:59"),
         chip(944, 482, "ProPresenter Slides — full screen", anchor="end")),
        ("scene-2-cam1-lyrics.svg", "Scene 2 — Cam 1 + Lyrics",
         "Cam 1 with the ProPresenter lyrics in a lower-third bar",
         view_cam1_p2(), lyrics_bar() + chip(24, 172, "Cam 1") + lyric_note),
        ("scene-3-cam2-lyrics.svg", "Scene 3 — Cam 2 + Lyrics",
         "Cam 2 with the ProPresenter lyrics in a lower-third bar",
         view_cam2_p2(), lyrics_bar() + chip(24, 172, "Cam 2") + lyric_note),
        ("scene-4-cam1-clean.svg", "Scene 4 — Cam 1 Clean",
         "Cam 1 only, nothing on top",
         view_cam1_p3(), chip(944, 482, "Cam 1 only — no overlay", anchor="end")),
        ("scene-5-cam2-clean.svg", "Scene 5 — Cam 2 Clean",
         "Cam 2 only, nothing on top",
         view_cam2_p4(), chip(944, 482, "Cam 2 only — no overlay", anchor="end")),
        ("scene-6-full-slide.svg", "Scene 6 — Full Slide",
         "ProPresenter Slides, full screen",
         slide_full(["Slide title"], small=[1, 2, 3]),
         chip(944, 482, "ProPresenter Slides — full screen", anchor="end")),
        ("scene-7-sermon-split.svg", "Scene 7 — Sermon Split",
         "Cam 2 P3 with the speaker on the left and the sermon slide on the right",
         view_cam2_p3(), split),
        ("scene-8-break.svg", "Scene 8 — Break",
         "Cam 2 P5 blurred, with the ProPresenter break slide and countdown on top",
         f'<g filter="url(#blur)">{view_cam2_p5()}</g>', brk),
        ("scene-9-end-slate.svg", "Scene 9 — End Slate",
         "Closing graphic, full screen",
         slide_full(["Closing graphic", "(design TBD)"]),
         chip(944, 482, "Closing graphic — full screen", anchor="end")),
    ]


def build_frames():
    for fname, name, what, view, overlay in PRESETS:
        frame(fname, name, f"{name}: {what}",
              f"Mock 16:9 camera frame for {name} — {what}. Dashed lines are the rule-of-thirds guides.",
              view(), guides() + overlay)
    for fname, name, what, view, overlay in scene_frames():
        frame(fname, name, f"{name}: {what}", f"Mock 16:9 program frame for {name}: {what}.", view, overlay)


# ---------- Signal flow ----------

def box(x, y, w, h, title, sub=None, operated=False, dashed=False):
    sw = 4 if operated else 1.75
    dash = ' stroke-dasharray="8 6"' if dashed else ""
    d = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{PAPER}" stroke="{INK}" stroke-width="{sw}"{dash}/>'
    if sub:
        d += text(x + w / 2, y + h / 2 - 4, title, 20, "bold", INK, "middle")
        d += text(x + w / 2, y + h / 2 + 20, sub, 15, "normal", DARK, "middle")
    else:
        d += text(x + w / 2, y + h / 2 + 7, title, 20, "bold", INK, "middle")
    return d


def arrow(x1, y1, x2, y2, control=False):
    if control:
        return (f'<path d="M{x1},{y1} L{x2},{y2}" stroke="{MID}" stroke-width="2.5" stroke-dasharray="7 6" '
                f'fill="none" marker-end="url(#arrow-mid)"/>')
    return f'<path d="M{x1},{y1} L{x2},{y2}" stroke="{INK}" stroke-width="3" fill="none" marker-end="url(#arrow)"/>'


def curve(x1, y1, x2, y2):
    mx = (x1 + x2) / 2
    return (f'<path d="M{x1},{y1} C{mx},{y1} {mx},{y2} {x2},{y2}" stroke="{INK}" stroke-width="3" '
            f'fill="none" marker-end="url(#arrow)"/>')


def build_signal_flow():
    w, h = 1000, 560
    d = f'<rect width="{w}" height="{h}" rx="14" fill="{PAPER}"/>'
    # Sources
    d += box(40, 30, 230, 64, "SuperJoy", "PTZOptics joystick", operated=True)
    d += box(40, 140, 230, 64, "Cam 1", "PTZOptics · center")
    d += box(40, 224, 230, 64, "Cam 2", "PTZOptics · left side")
    d += arrow(155, 94, 155, 138, control=True)
    d += (f'<path d="M40,62 H16 V256 H38" stroke="{MID}" stroke-width="2.5" stroke-dasharray="7 6" '
          f'fill="none" marker-end="url(#arrow-mid)"/>')
    d += f'<rect x="24" y="318" width="262" height="196" rx="12" fill="{PALE}" stroke="{MID}" stroke-width="1.75" stroke-dasharray="8 6"/>'
    d += text(155, 346, "ProPresenter computer", 16, "bold", DARK, "middle")
    d += text(155, 366, "run by another team", 15, "normal", DARK, "middle")
    d += box(40, 380, 230, 54, "Lyrics")
    d += box(40, 446, 230, 54, "Slides")
    # Ecamm + Stream Deck
    d += box(390, 30, 220, 64, "Stream Deck", "one button = one scene", operated=True)
    d += box(390, 210, 220, 130, "Ecamm Live", "builds the scenes", operated=True)
    d += arrow(500, 94, 500, 208, control=True)
    for y_src, y_dst in ((172, 236), (256, 262), (407, 288), (473, 314)):
        d += curve(270, y_src, 388, y_dst)
    # Resi + destinations
    d += box(680, 243, 120, 64, "Resi", "streams out", operated=True)
    d += arrow(610, 275, 678, 275)
    d += box(850, 190, 130, 64, "YouTube")
    d += box(850, 296, 130, 64, "Church", "website embed")
    d += curve(800, 265, 848, 222) + curve(800, 285, 848, 328)
    # Legend
    ly = 450
    d += f'<line x1="400" y1="{ly}" x2="460" y2="{ly}" stroke="{INK}" stroke-width="3" marker-end="url(#arrow)"/>'
    d += text(472, ly + 6, "Video", 17)
    d += f'<line x1="400" y1="{ly + 34}" x2="460" y2="{ly + 34}" stroke="{MID}" stroke-width="2.5" stroke-dasharray="7 6" marker-end="url(#arrow-mid)"/>'
    d += text(472, ly + 40, "Control (no video)", 17)
    d += f'<rect x="680" y="{ly - 16}" width="56" height="32" rx="6" fill="{PAPER}" stroke="{INK}" stroke-width="4"/>'
    d += text(748, ly + 6, "You operate this", 17)
    d += f'<rect x="680" y="{ly + 22}" width="56" height="32" rx="6" fill="{PAPER}" stroke="{INK}" stroke-width="1.75"/>'
    d += text(748, ly + 44, "Runs on its own / other team", 17)
    (OUT / "signal-flow.svg").write_text(svg(
        w, h, "Livestream signal flow",
        "Cam 1 and Cam 2 (moved by the SuperJoy) and ProPresenter Lyrics and Slides feed Ecamm Live. "
        "The Stream Deck picks the Ecamm scene. Ecamm sends the program to Resi, which streams to YouTube "
        "and the church website.", d))


# ---------- Room map ----------

def camera_icon(x, y, angle, label, label_at):
    return (f'<g transform="translate({x},{y}) rotate({angle})">'
            f'<rect x="-22" y="-16" width="34" height="32" rx="5" fill="{INK}"/>'
            f'<path d="M12,-9 L28,-15 L28,15 L12,9 Z" fill="{INK}"/></g>'
            + chip(label_at[0], label_at[1], label, 18))


def cone(x, y, p1, p2, dashed=False):
    style = (f'fill="{MID}" fill-opacity="0.06" stroke="{MID}" stroke-width="2" stroke-dasharray="6 6"' if dashed
             else f'fill="{INK}" fill-opacity="0.1" stroke="{INK}" stroke-width="2"')
    return f'<path d="M{x},{y} L{p1[0]},{p1[1]} L{p2[0]},{p2[1]} Z" {style}/>'


def build_room_map():
    w, h = 1000, 780
    d = f'<rect width="{w}" height="{h}" rx="14" fill="{PAPER}"/>'
    # Walls, stage, congregation rows (two blocks with a center aisle)
    d += f'<rect x="120" y="30" width="720" height="680" fill="none" stroke="{INK}" stroke-width="4"/>'
    d += f'<rect x="200" y="30" width="560" height="170" fill="{FILL}" stroke="{INK}" stroke-width="2.5"/>'
    for i in range(7):
        y = 340 + i * 44
        d += f'<rect x="210" y="{y}" width="240" height="22" rx="4" fill="{PALE}" stroke="{MID}" stroke-width="1.5"/>'
        d += f'<rect x="510" y="{y}" width="240" height="22" rx="4" fill="{PALE}" stroke="{MID}" stroke-width="1.5"/>'
    # Fields of view, drawn under the labels
    c1 = (480, 672)
    c2 = (150, 300)
    d += cone(*c2, (215, 690), (830, 520), dashed=True)
    d += cone(*c1, (220, 40), (740, 40))
    d += cone(*c2, (215, 40), (760, 215))
    # Stage contents (positions approximate)
    d += text(480, 62, "STAGE", 22, "bold", INK, "middle")
    d += f'<circle cx="390" cy="140" r="12" fill="{DARK}"/>'
    d += chip(390, 92, "Worship leader", 15, "middle")
    d += f'<circle cx="480" cy="152" r="10" fill="{DARK}"/>'
    d += f'<path d="M455,165 L505,165 L500,190 L460,190 Z" fill="{SOFT}" stroke="{INK}" stroke-width="2.5"/>'
    d += chip(515, 160, "Pulpit", 15)
    d += f'<rect x="590" y="80" width="150" height="100" rx="10" fill="{SOFT}" stroke="{DARK}" stroke-width="2"/>'
    d += f'<circle cx="700" cy="112" r="20" fill="{PAPER}" stroke="{DARK}" stroke-width="2"/>'
    d += f'<rect x="605" y="100" width="54" height="12" fill="{INK}"/>'
    d += chip(665, 140, "Band", 15, "middle")
    d += f'<rect x="420" y="225" width="120" height="36" fill="{SOFT}" stroke="{INK}" stroke-width="2"/>'
    d += chip(480, 270, "Communion table", 15, "middle")
    d += chip(330, 300, "Congregation", 15, "middle")
    d += chip(630, 300, "Congregation", 15, "middle")
    # Cameras
    d += camera_icon(*c1, -90, "Cam 1 — center", (c1[0] + 30, c1[1] - 30))
    d += camera_icon(*c2, -35, "Cam 2 — left side", (c2[0] - 10, c2[1] - 80))
    # Orientation, legend
    d += text(130, 742, "BACK OF ROOM", 15, "bold", MID)
    d += text(70, 370, "LEFT SIDE (facing stage)", 15, "bold", MID, "middle", 'transform="rotate(-90 70 370)"')
    d += text(840, 742, "Schematic — not to scale", 15, "normal", MID, "end")
    lx = 860
    d += f'<rect x="{lx}" y="560" width="36" height="22" fill="{INK}" fill-opacity="0.1" stroke="{INK}" stroke-width="2"/>'
    d += text(lx + 44, 576, "P1 view", 15)
    d += f'<rect x="{lx}" y="596" width="36" height="22" fill="{MID}" fill-opacity="0.06" stroke="{MID}" stroke-width="2" stroke-dasharray="6 6"/>'
    d += text(lx + 44, 612, "Cam 2 P5", 15)
    (OUT / "room-map.svg").write_text(svg(
        w, h, "Room map: camera positions",
        "Top-down schematic. The stage is at the top with the pulpit in the center, the band on the right and "
        "the communion table on the floor in front. Cam 1 is at the back center and sees the whole stage. "
        "Cam 2 is on the left side (facing the stage) and sees the stage at an angle; its P5 view turns toward "
        "the congregation.", d))


# ---------- Stream Deck ----------

SCENES = ["Countdown", "Cam 1 + Lyrics", "Cam 2 + Lyrics", "Cam 1 Clean", "Cam 2 Clean",
          "Full Slide", "Sermon Split", "Break", "End Slate"]


def build_stream_deck():
    cols, rows, key, gap = 5, 3, 150, 22
    pad = 50
    dw = pad * 2 + cols * key + (cols - 1) * gap
    dh = pad * 2 + rows * key + (rows - 1) * gap
    w, h = dw + 40, dh + 110
    d = f'<rect width="{w}" height="{h}" rx="14" fill="{PAPER}"/>'
    d += f'<rect x="20" y="20" width="{dw}" height="{dh}" rx="28" fill="{PALE}" stroke="{INK}" stroke-width="4"/>'
    for i in range(cols * rows):
        r, c = divmod(i, cols)
        x = 20 + pad + c * (key + gap)
        y = 20 + pad + r * (key + gap)
        if i < len(SCENES):
            name = SCENES[i]
            d += f'<rect x="{x}" y="{y}" width="{key}" height="{key}" rx="16" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>'
            d += text(x + key / 2, y + 74, str(i + 1), 54, "bold", INK, "middle")
            parts = name.split(" + ")
            if len(parts) == 2:
                d += text(x + key / 2, y + 108, parts[0] + " +", 19, "bold", INK, "middle")
                d += text(x + key / 2, y + 132, parts[1], 19, "bold", INK, "middle")
            else:
                d += text(x + key / 2, y + 118, name, 19, "bold", INK, "middle")
        else:
            d += (f'<rect x="{x}" y="{y}" width="{key}" height="{key}" rx="16" fill="none" stroke="{MID}" '
                  f'stroke-width="2" stroke-dasharray="8 7"/>')
            d += text(x + key / 2, y + key / 2 + 6, "empty", 18, "normal", MID, "middle")
    d += text(20, dh + 70, "One button = one complete scene. Empty buttons stay empty on purpose.", 20, "normal", INK)
    (OUT / "stream-deck.svg").write_text(svg(
        w, h, "Stream Deck button layout",
        "15-key Stream Deck. Top row: 1 Countdown, 2 Cam 1 + Lyrics, 3 Cam 2 + Lyrics, 4 Cam 1 Clean, "
        "5 Cam 2 Clean. Second row: 6 Full Slide, 7 Sermon Split, 8 Break, 9 End Slate, then empty. "
        "Third row: empty.", d))


# ---------- Glossary (Video Basics page) ----------

def thumb(x, y, s, view, border=3):
    """A mock frame drawn small, at scale `s`, with its top-left corner at (x, y)."""
    return (f'<g transform="translate({x},{y}) scale({s})">'
            f'<rect width="{W}" height="{H}" fill="{PAPER}"/>'
            f'<g clip-path="url(#frame)">{view}</g>'
            f'<rect x="{border / s / 2:.1f}" y="{border / s / 2:.1f}" width="{W - border / s:.1f}" '
            f'height="{H - border / s:.1f}" fill="none" stroke="{INK}" stroke-width="{border / s:.1f}"/></g>')


def arc(cx, cy, r, a1, a2):
    """Double-headed arc arrow around (cx, cy), from angle a1 to a2 in degrees (0 = right, 90 = down)."""
    x1, y1 = cx + r * cos(radians(a1)), cy + r * sin(radians(a1))
    x2, y2 = cx + r * cos(radians(a2)), cy + r * sin(radians(a2))
    large = 1 if abs(a2 - a1) > 180 else 0
    return (f'<path d="M{x1:.1f},{y1:.1f} A{r},{r} 0 {large} 1 {x2:.1f},{y2:.1f}" stroke="{INK}" stroke-width="3.5" '
            f'fill="none" marker-start="url(#arrow)" marker-end="url(#arrow)"/>')


def ptz_camera(cx, cy, s=1.0, side=False):
    """A PTZ camera. Seen from above by default, or from the side with `side=True`."""
    if side:
        return (f'<rect x="{cx - 50 * s:.1f}" y="{cy + 34 * s:.1f}" width="{100 * s:.1f}" height="{22 * s:.1f}" rx="4" fill="{DARK}"/>'
                f'<rect x="{cx - 10 * s:.1f}" y="{cy + 10 * s:.1f}" width="{20 * s:.1f}" height="{26 * s:.1f}" fill="{MID}"/>'
                f'<rect x="{cx - 45 * s:.1f}" y="{cy - 28 * s:.1f}" width="{80 * s:.1f}" height="{44 * s:.1f}" rx="8" fill="{INK}"/>'
                f'<rect x="{cx + 35 * s:.1f}" y="{cy - 20 * s:.1f}" width="{18 * s:.1f}" height="{28 * s:.1f}" rx="3" fill="{INK}"/>')
    return (f'<circle cx="{cx}" cy="{cy}" r="{48 * s:.1f}" fill="{PALE}" stroke="{MID}" stroke-width="2"/>'
            f'<rect x="{cx - 40 * s:.1f}" y="{cy - 22 * s:.1f}" width="{70 * s:.1f}" height="{44 * s:.1f}" rx="8" fill="{INK}"/>'
            f'<rect x="{cx + 30 * s:.1f}" y="{cy - 15 * s:.1f}" width="{18 * s:.1f}" height="{30 * s:.1f}" rx="3" fill="{INK}"/>')


def build_glossary():
    # Lead room: Cam 2 P3 with the facing direction and the open space marked.
    lead = (guides()
            + f'<line x1="318" y1="88" x2="420" y2="88" stroke="{INK}" stroke-width="3" marker-end="url(#arrow)"/>'
            + chip(428, 70, "Faces this way", 16)
            + f'<line x1="350" y1="440" x2="940" y2="440" stroke="{INK}" stroke-width="2.5" '
              f'marker-start="url(#arrow)" marker-end="url(#arrow)"/>'
            + chip(645, 396, "Lead room: open space on the side they face", 18, "middle"))
    frame("glossary-lead-room.svg", "Cam 2 P3", "Lead room",
          "Mock 16:9 frame of Cam 2 P3. The preacher stands on the left third and faces right. "
          "An arrow marks the open space on the right side of the frame: the lead room.",
          view_cam2_p3(), lead)

    # Program vs. preview: the live picture next to the off-air camera.
    w, h, s = 1000, 470, 0.46
    tw, th = W * s, H * s
    d = f'<rect width="{w}" height="{h}" rx="14" fill="{PAPER}"/>'
    for x, head, sub, view, note, live in (
            (40, "PROGRAM", "On air: viewers see this", view_cam1_p3(), "Scene 4 — Cam 1 Clean, Cam 1 P3", True),
            (518, "PREVIEW", "Off air: safe to move", view_cam2_p3(), "Cam 2: recall Cam 2 P3 here", False)):
        d += text(x, 44, head, 28, "bold")
        d += text(x, 72, sub, 20, "normal", DARK)
        d += thumb(x, 90, s, view, 8 if live else 2)
        if live:
            d += f'<rect x="{x + 14}" y="104" width="74" height="34" rx="6" fill="{INK}"/>' + text(x + 51, 128, "LIVE", 20, "bold", PAPER, "middle")
        else:
            d += (f'<rect x="{x + 14}" y="104" width="104" height="34" rx="6" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'
                  + text(x + 66, 128, "OFF AIR", 18, "bold", INK, "middle"))
        d += chip(x + tw / 2, 90 + th + 16, note, 17, "middle")
    d += text(w / 2, h - 24, "Move only the camera that is off air. Then cut, so it becomes the program.", 19, "normal", INK, "middle")
    (OUT / "glossary-program-preview.svg").write_text(svg(
        w, h, "Program and preview",
        "Two frames side by side. Left: PROGRAM, on air, showing Scene 4 — Cam 1 Clean on Cam 1 P3, with a thick "
        "border and a LIVE label. Right: PREVIEW, off air, showing Cam 2 on Cam 2 P3. This is the camera you may move.", d))

    # Cut: one shot replaced by the next.
    w, h, s = 1000, 390, 0.42
    tw, th = W * s, H * s
    d = f'<rect width="{w}" height="{h}" rx="14" fill="{PAPER}"/>'
    d += thumb(40, 40, s, view_cam1_p3())
    d += thumb(w - 40 - tw, 40, s, view_cam2_p3() + sermon_slide())
    d += chip(40 + tw / 2, 40 + th + 16, "Scene 4 — Cam 1 Clean", 17, "middle")
    d += chip(w - 40 - tw / 2, 40 + th + 16, "Scene 7 — Sermon Split", 17, "middle")
    d += arrow(40 + tw + 20, 40 + th / 2, w - 40 - tw - 20, 40 + th / 2)
    d += text(w / 2, 40 + th / 2 - 18, "CUT", 24, "bold", INK, "middle")
    d += text(w / 2, h - 24, "Press one Stream Deck button: the picture changes from one shot to the next.", 19, "normal", INK, "middle")
    (OUT / "glossary-cut.svg").write_text(svg(
        w, h, "Cut",
        "Two frames with an arrow labeled CUT between them. Left: Scene 4 — Cam 1 Clean. Right: Scene 7 — Sermon Split. "
        "Pressing one Stream Deck button switches from one to the other.", d))

    # PTZ: pan, tilt, zoom.
    w, h = 1000, 380
    d = f'<rect width="{w}" height="{h}" rx="14" fill="{PAPER}"/>'
    d += ptz_camera(170, 170) + arc(170, 170, 95, -55, 55)
    d += text(170, 316, "PAN", 26, "bold", INK, "middle") + text(170, 346, "Turn left or right (seen from above)", 17, "normal", DARK, "middle")
    d += ptz_camera(490, 170, 1.0, side=True) + arc(490, 170, 95, -50, 50)
    d += text(490, 316, "TILT", 26, "bold", INK, "middle") + text(490, 346, "Aim up or down (seen from the side)", 17, "normal", DARK, "middle")
    d += f'<rect x="700" y="70" width="240" height="135" fill="{PALE}" stroke="{INK}" stroke-width="3"/>'
    d += f'<rect x="770" y="110" width="100" height="56" fill="none" stroke="{INK}" stroke-width="2.5" stroke-dasharray="8 6"/>'
    for (x1, y1), (x2, y2) in (((706, 76), (764, 106)), ((934, 76), (876, 106)), ((706, 199), (764, 170)), ((934, 199), (876, 170))):
        d += f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{INK}" stroke-width="2.5" marker-end="url(#arrow)"/>'
    d += text(820, 316, "ZOOM", 26, "bold", INK, "middle") + text(820, 346, "Closer (dashed) or wider (solid)", 17, "normal", DARK, "middle")
    (OUT / "glossary-ptz.svg").write_text(svg(
        w, h, "PTZ: pan, tilt, zoom",
        "Three panels. Pan: a camera seen from above, with a curved arrow showing it turning left and right. "
        "Tilt: a camera seen from the side, with a curved arrow showing it aiming up and down. "
        "Zoom: a frame with a smaller dashed frame inside; arrows point inward to show zooming closer.", d))

    # Preset: one number, one saved shot.
    w, h, s = 1000, 350, 0.215
    tw, th = W * s, H * s
    d = f'<rect width="{w}" height="{h}" rx="14" fill="{PAPER}"/>'
    gap = (w - 4 * tw) / 5
    for i, view in enumerate((view_cam1_p1, view_cam1_p2, view_cam1_p3, view_cam1_p4)):
        x = gap + i * (tw + gap)
        cx = x + tw / 2
        d += f'<circle cx="{cx:.1f}" cy="62" r="30" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>'
        d += text(cx, 74, str(i + 1), 32, "bold", INK, "middle")
        d += arrow(cx, 96, cx, 128)
        d += thumb(x, 134, s, view())
        d += text(cx, 134 + th + 30, f"Cam 1 P{i + 1}", 20, "bold", INK, "middle")
    d += text(w / 2, h - 22, "Each preset number recalls one saved shot. P1 is always the safe wide shot.", 19, "normal", INK, "middle")
    (OUT / "glossary-preset.svg").write_text(svg(
        w, h, "Presets",
        "Four numbered buttons, 1 to 4, each with an arrow down to a small frame: Cam 1 P1 full stage wide, "
        "Cam 1 P2 worship leader, Cam 1 P3 pulpit, Cam 1 P4 announcements spot.", d))


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    build_frames()
    build_signal_flow()
    build_room_map()
    build_stream_deck()
    build_glossary()
    print(f"Wrote {len(list(OUT.glob('*.svg')))} SVGs to {OUT}")
