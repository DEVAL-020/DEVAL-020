#!/usr/bin/env python3
"""
Generates the SVG panels used by README.md  ->  ./src/*.svg
Theme: minimal + glassmorphism (neutral dark base, frosted panels, one soft accent).

Usage (from the repo root):
    python3 generate_assets.py

Optional: put your photo at  src/photo.jpg  (or .png) and run again.
Edit the CONFIG block to change text / numbers, then re-run.
"""
import base64, io, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "src")
os.makedirs(OUT, exist_ok=True)

# ───────────────────────────── CONFIG ─────────────────────────────
NAME = "Deval Patel"
INITIALS = "DP"
TAGLINE = "Building AI-powered products and full-stack apps, one commit at a time."
CHIPS = ["GEC Gandhinagar", "B.E. Computer Engineering", "AI / ML", "Full-Stack"]
LOCATION = "Gandhinagar, IN"

STATS = [("5", "STARS"), ("10+", "PROJECTS"), ("3", "YEARS OF LEARNING")]
SKILLS = [  # self-rated, change freely
    ("Full-Stack Web", 80),
    ("AI / ML", 65),
    ("DSA & Problem Solving", 70),
    ("Git & Open Source", 60),
]
CALLOUT = "Currently building SentinelAI: AI-driven disaster management & rescue."

STACK = [
    ("LANGUAGES", ["C", "C++", "Java", "Python", "JavaScript"]),
    ("FRONTEND", ["React", "Next.js", "Tailwind", "Framer Motion", "GSAP"]),
    ("BACKEND", ["Node.js", "Express", "FastAPI"]),
    ("DATA & TOOLS", ["MongoDB", "PostgreSQL", "MySQL", "Git", "Linux", "Figma"]),
]
ORBITS = [  # rx, ry, tilt, seconds, reverse, skills
    (300, 82, -18, 30, 0, ["Python", "C++", "Java", "C"]),
    (440, 130, 14, 44, 1, ["React", "Next.js", "Tailwind", "JavaScript", "Node.js", "Express", "FastAPI"]),
    (520, 60, -4, 58, 0, ["MongoDB", "PostgreSQL", "MySQL", "Git", "Linux", "Figma"]),
]
WORK = [
    ("SentinelAI", "AI-driven disaster management & rescue command centre", "AI + Full-Stack"),
    ("Music Player", "Web player with fluid Framer Motion & GSAP animations", "Frontend + UX"),
    ("Notebook To-Do", "Handwritten-notebook UI with Express + PostgreSQL login", "Full-Stack"),
    ("Arcade Calculator", "Google Arcade points calculator tool", "Utility"),
    ("DVX / DevalLabs", "Open-source AI/ML project built with school friends", "Open Source"),
]
CONNECT = [  # file, badge, title, handle
    ("linkedin", "in", "LinkedIn", "gecgce2024deval"),
    ("x", "X", "X / Twitter", "@Official_Deval"),
    ("stackoverflow", "SO", "Stack Overflow", "user 31278451"),
    ("email", "@", "Email", "pateldeval6050@gmail.com"),
]

ACCENT = "#8ea2ff"      # the only accent colour
INK = "#f3f4f6"         # primary text
SOFT = "#aab2c2"        # secondary text
MUTE = "#6b7385"        # labels
# ──────────────────────────────────────────────────────────────────


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def load_photo():
    for n in ("deval.jpeg", "deval.jpg", "deval.png", "photo.jpg", "photo.jpeg", "photo.png"):
        p = os.path.join(OUT, n)
        if os.path.exists(p):
            try:
                from PIL import Image
                im = Image.open(p).convert("RGB")
                s = min(im.size)
                l, t = (im.width - s) // 2, (im.height - s) // 6
                im = im.crop((l, t, l + s, t + s)).resize((480, 480))
                buf = io.BytesIO()
                im.save(buf, "JPEG", quality=85)
                return base64.b64encode(buf.getvalue()).decode()
            except Exception as e:
                print("Could not embed photo:", e)
    return None


PHOTO = load_photo()

STYLE = """
.s{font-family:Inter,'SF Pro Display','Segoe UI',Helvetica,Arial,sans-serif}
.m{font-family:'JetBrains Mono','SF Mono',Consolas,'Courier New',monospace}
@keyframes fl{0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}
@keyframes br{0%,100%{opacity:.55}50%{opacity:1}}
.br{animation:br 3.2s ease-in-out infinite}
"""


def svg(w, h, body, defs="", orbs=()):
    orb_svg = "".join(
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{c}" opacity="{o}" filter="url(#blur)"/>' for cx, cy, r, c, o in orbs)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<style>{STYLE}</style>
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0c0e13"/><stop offset="1" stop-color="#141824"/></linearGradient>
<linearGradient id="glass" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".10"/><stop offset="1" stop-color="#fff" stop-opacity=".03"/></linearGradient>
<linearGradient id="gstroke" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".38"/><stop offset=".5" stop-color="#fff" stop-opacity=".08"/><stop offset="1" stop-color="#fff" stop-opacity=".18"/></linearGradient>
<linearGradient id="bar" x1="0" x2="1"><stop offset="0" stop-color="{ACCENT}" stop-opacity=".55"/><stop offset="1" stop-color="#ffffff" stop-opacity=".9"/></linearGradient>
<filter id="blur" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="55"/></filter>
<clipPath id="panel"><rect width="{w}" height="{h}" rx="26"/></clipPath>
{defs}
</defs>
<g clip-path="url(#panel)">
<rect width="{w}" height="{h}" fill="url(#bg)"/>
{orb_svg}
{body}
</g>
<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="26" fill="none" stroke="#fff" stroke-opacity=".10"/>
</svg>"""


def glass(x, y, w, h, rx=18):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="url(#glass)" stroke="url(#gstroke)"/>'


def pill(x, y, text, size=13, h=32, dot=True, mono=False):
    w = 30 + len(text) * (size * 0.58) + (14 if dot else 0)
    cls = "m" if mono else "s"
    d = f'<circle cx="{x+16}" cy="{y+h/2}" r="3" fill="{ACCENT}"/>' if dot else ""
    tx = x + (30 if dot else 16)
    return (glass(x, y, w, h, h / 2) + d +
            f'<text x="{tx}" y="{y+h/2+size*0.35:.1f}" class="{cls}" font-size="{size}" font-weight="500" fill="#e5e7eb">{esc(text)}</text>'), w


def label(x, y, text):
    return f'<text x="{x}" y="{y}" class="m" font-size="12" fill="{MUTE}" letter-spacing="3">{esc(text.upper())}</text>'


def avatar(x, y, w, h, rx, cid):
    defs = f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}"/></clipPath>'
    if PHOTO:
        inner = (f'<image href="data:image/jpeg;base64,{PHOTO}" x="{x}" y="{y}" width="{w}" height="{h}" '
                 f'preserveAspectRatio="xMidYMid slice" clip-path="url(#{cid})"/>')
    else:
        inner = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="#fff" fill-opacity=".05"/>'
                 f'<text x="{x+w/2}" y="{y+h/2+min(w,h)*0.14:.0f}" text-anchor="middle" class="s" font-weight="300" '
                 f'font-size="{min(w,h)*0.40:.0f}" fill="#fff" fill-opacity=".75">{INITIALS}</text>')
    return defs, inner + f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="none" stroke="#fff" stroke-opacity=".25"/>'


# ───────────────────────────── HERO ─────────────────────────────
def hero():
    W, H = 1200, 440
    adefs, av = avatar(860, 100, 240, 240, 120, "avh")
    chips, x = "", 64
    for c in CHIPS:
        s, w = pill(x, 330, c, 13)
        chips += s
        x += w + 12
    body = f"""
{glass(24, 24, 1152, 392, 24)}
<text x="64" y="92" class="m" font-size="13" fill="{SOFT}" letter-spacing="3">SOFTWARE ENGINEER IN THE MAKING · {esc(LOCATION.upper())}</text>
<text x="60" y="206" class="s" font-size="96" font-weight="700" fill="{INK}" letter-spacing="-3">{esc(NAME)}<tspan fill="{ACCENT}">.</tspan></text>
<text x="64" y="262" class="s" font-size="20" fill="{SOFT}">{esc(TAGLINE)}</text>
{chips}
<circle cx="980" cy="220" r="134" fill="#fff" fill-opacity=".04" stroke="#fff" stroke-opacity=".16"/>
<circle cx="980" cy="220" r="152" fill="none" stroke="#fff" stroke-opacity=".07"/>
{av}
"""
    return svg(W, H, body, adefs, orbs=[(1000, 90, 230, "#5b6cff", .55), (120, 420, 200, "#2dd4bf", .20)])


# ───────────────────────────── EARTH ─────────────────────────────
def earth():
    W, H, cx, cy, R = 1200, 760, 600, 430, 150
    land = ('<g id="land" fill="#b8c4e0" fill-opacity=".85">'
            '<path d="M60 62 L118 38 L172 58 L164 100 L132 132 L98 122 L70 92Z"/>'
            '<path d="M132 152 L168 146 L178 192 L152 252 L130 222 L124 182Z"/>'
            '<path d="M300 112 L350 104 L372 150 L352 216 L320 222 L298 170Z"/>'
            '<path d="M300 60 L350 54 L362 86 L322 96Z"/>'
            '<path d="M372 60 L472 48 L524 86 L502 132 L432 142 L392 112Z"/>'
            '<path d="M476 192 L524 186 L534 222 L492 228Z"/>'
            '<circle cx="268" cy="70" r="12"/><circle cx="560" cy="150" r="9"/><circle cx="30" cy="190" r="8"/></g>')
    clouds = ('<g id="clouds" fill="#fff" opacity=".16">'
              '<ellipse cx="90" cy="110" rx="46" ry="9"/><ellipse cx="230" cy="190" rx="60" ry="10"/><ellipse cx="340" cy="70" rx="40" ry="8"/>'
              '<ellipse cx="450" cy="170" rx="55" ry="9"/><ellipse cx="540" cy="90" rx="38" ry="8"/></g>')
    defs = f"""
<radialGradient id="ocean" cx=".35" cy=".3" r=".95"><stop offset="0" stop-color="#5a6fa8"/><stop offset=".6" stop-color="#27325a"/><stop offset="1" stop-color="#131a33"/></radialGradient>
<radialGradient id="shade" cx=".3" cy=".25" r=".95"><stop offset=".45" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#05060d" stop-opacity=".8"/></radialGradient>
<clipPath id="ec"><circle cx="{cx}" cy="{cy}" r="{R}"/></clipPath>
{land}{clouds}"""
    ox, oy = cx - R, cy - R
    back, front, nodes = "", "", ""
    for (rx, ry, tilt, dur, rev, skills) in ORBITS:
        back += (f'<g transform="rotate({tilt} {cx} {cy})"><ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" '
                 f'stroke="#fff" stroke-opacity=".12" stroke-dasharray="2 8"/></g>')
        front += (f'<g transform="rotate({tilt} {cx} {cy})"><path d="M{cx-rx} {cy} A{rx} {ry} 0 0 0 {cx+rx} {cy}" fill="none" '
                  f'stroke="#fff" stroke-opacity=".28"/></g>')
        sw = 1 if rev else 0
        path = f"M{cx-rx} {cy} a{rx} {ry} 0 1 {sw} {2*rx} 0 a{rx} {ry} 0 1 {sw} {-2*rx} 0"
        n = len(skills)
        nodes += f'<g transform="rotate({tilt} {cx} {cy})">'
        for k, lab in enumerate(skills):
            w = 36 + len(lab) * 8.2
            nodes += (f'<g><animateMotion dur="{dur}s" begin="-{dur*k/n:.1f}s" repeatCount="indefinite" path="{path}"/>'
                      f'<g transform="rotate({-tilt})"><rect x="{-w/2:.1f}" y="-16" width="{w:.1f}" height="32" rx="16" fill="#141a2b" fill-opacity=".82" stroke="#fff" stroke-opacity=".28"/>'
                      f'<circle cx="{-w/2+16:.1f}" cy="0" r="3" fill="{ACCENT}"/>'
                      f'<text x="{-w/2+28:.1f}" y="4.5" class="s" font-size="13" font-weight="500" fill="#e5e7eb">{esc(lab)}</text></g></g>')
        nodes += "</g>"
    body = f"""
{label(60, 56, "01 — Tech orbit")}
<text x="58" y="128" class="s" font-size="60" font-weight="700" fill="{INK}" letter-spacing="-2">My tech world<tspan fill="{ACCENT}">.</tspan></text>
<text x="60" y="164" class="s" font-size="18" fill="{SOFT}">A planet that never stops spinning, just like my curiosity.</text>
{back}
<g clip-path="url(#ec)">
  <rect x="{ox}" y="{oy}" width="{2*R}" height="{2*R}" fill="url(#ocean)"/>
  <g transform="translate({ox} {oy})"><animateTransform attributeName="transform" type="translate" from="{ox} {oy}" to="{ox-600} {oy}" dur="40s" repeatCount="indefinite"/>
     <use href="#land"/><use href="#land" x="600"/></g>
  <g transform="translate({ox} {oy})"><animateTransform attributeName="transform" type="translate" from="{ox} {oy}" to="{ox-600} {oy}" dur="26s" repeatCount="indefinite"/>
     <use href="#clouds"/><use href="#clouds" x="600"/></g>
  <circle cx="{cx}" cy="{cy}" r="{R}" fill="url(#shade)"/>
</g>
<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="#fff" stroke-opacity=".30"/>
<circle cx="{cx}" cy="{cy}" r="{R+14}" fill="none" stroke="#fff" stroke-opacity=".08"/>
{front}
{nodes}
{label(cx-150, H-34, "skills in orbit").replace('<text ', '<text text-anchor="start" ')}
"""
    return svg(W, H, body, defs, orbs=[(cx, cy, 210, "#5b6cff", .45), (1050, 120, 150, "#2dd4bf", .14), (100, 700, 160, "#5b6cff", .18)])


# ───────────────────────────── ABOUT CARD ─────────────────────────────
def card():
    W, H = 1200, 560
    adefs, av = avatar(112, 92, 256, 232, 16, "avc")
    tiles = ""
    for i, (v, l) in enumerate(STATS):
        x = 450 + i * 240
        tiles += (glass(x, 150, 220, 104, 16) +
                  f'<text x="{x+24}" y="208" class="s" font-size="46" font-weight="600" fill="{INK}" letter-spacing="-1">{esc(v)}</text>'
                  f'<text x="{x+24}" y="236" class="m" font-size="11" fill="{MUTE}" letter-spacing="2">{esc(l)}</text>')
    sk = ""
    for i, (lab, pct) in enumerate(SKILLS):
        y = 318 + i * 46
        sk += (f'<text x="450" y="{y}" class="s" font-size="15" fill="#d1d5db">{esc(lab)}</text>'
               f'<text x="1150" y="{y}" text-anchor="end" class="m" font-size="12" fill="{SOFT}">{pct}%</text>'
               f'<rect x="450" y="{y+12}" width="700" height="4" rx="2" fill="#fff" fill-opacity=".10"/>'
               f'<rect x="450" y="{y+12}" width="{7*pct}" height="4" rx="2" fill="url(#bar)">'
               f'<animate attributeName="width" from="0" to="{7*pct}" dur="1.2s" begin="0s" fill="freeze"/></rect>')
    body = f"""
{glass(80, 60, 300, 440, 26)}
{av}
<text x="112" y="372" class="s" font-size="26" font-weight="600" fill="{INK}" letter-spacing="-.5">{esc(NAME)}</text>
<text x="112" y="396" class="s" font-size="14" fill="{SOFT}">B.E. Computer Engineering</text>
<text x="112" y="416" class="s" font-size="14" fill="{SOFT}">GEC Gandhinagar · Sem 5</text>
<rect x="112" y="442" width="236" height="1" fill="#fff" fill-opacity=".12"/>
<text x="112" y="468" class="m" font-size="11" fill="{MUTE}" letter-spacing="2">@DEVAL-020</text>
<circle cx="338" cy="464" r="4" fill="{ACCENT}" class="br"/>
{label(450, 76, "02 — About")}
<text x="448" y="128" class="s" font-size="44" font-weight="700" fill="{INK}" letter-spacing="-1.5">More than a marksheet<tspan fill="{ACCENT}">.</tspan></text>
{tiles}
{label(450, 292, "skill signal · self-rated")}
{sk}
{glass(450, 500, 700, 36, 18)}
<circle cx="472" cy="518" r="3.5" fill="{ACCENT}" class="br"/>
<text x="488" y="523" class="s" font-size="14" fill="#d1d5db">{esc(CALLOUT)}</text>
"""
    return svg(W, H, body, adefs, orbs=[(1080, 80, 220, "#5b6cff", .40), (160, 520, 190, "#2dd4bf", .16)])


# ───────────────────────────── STACK ─────────────────────────────
def stack():
    chips, y = "", 196
    for label_, items in STACK:
        chips += label(60, y, label_)
        y += 16
        x = 60
        for it in items:
            s, w = pill(x, y, it, 14, h=36)
            if x + w > 1140:
                x, y = 60, y + 46
                s, w = pill(x, y, it, 14, h=36)
            chips += s
            x += w + 12
        y += 70
    W, H = 1200, y - 6
    body = f"""
{label(60, 56, "03 — Toolbox")}
<text x="58" y="112" class="s" font-size="48" font-weight="700" fill="{INK}" letter-spacing="-1.5">Tools change<tspan fill="{ACCENT}">.</tspan></text>
<text x="58" y="162" class="s" font-size="48" font-weight="700" fill="{MUTE}" letter-spacing="-1.5">Curiosity doesn't.</text>
{chips}
"""
    return svg(W, H, body, orbs=[(1100, 60, 200, "#5b6cff", .35), (100, H, 180, "#2dd4bf", .14)])


# ───────────────────────────── WORK ─────────────────────────────
def work():
    n = len(WORK)
    top, rh = 176, 70
    rows = ""
    for i, (p, d, f) in enumerate(WORK):
        y = top + i * rh
        if i:
            rows += f'<rect x="72" y="{y}" width="1056" height="1" fill="#fff" fill-opacity=".08"/>'
        cy = y + rh / 2
        pw = 28 + len(f) * 7.6
        rows += (f'<text x="72" y="{cy+6:.0f}" class="m" font-size="12" fill="{MUTE}">0{i+1}</text>'
                 f'<text x="120" y="{cy+7:.0f}" class="s" font-size="20" font-weight="600" fill="{INK}">{esc(p)}</text>'
                 f'<text x="380" y="{cy+6:.0f}" class="s" font-size="16" fill="{SOFT}">{esc(d)}</text>'
                 f'<rect x="{1128-pw:.0f}" y="{cy-14:.0f}" width="{pw:.0f}" height="28" rx="14" fill="#fff" fill-opacity=".05" stroke="#fff" stroke-opacity=".18"/>'
                 f'<text x="{1128-pw/2:.0f}" y="{cy+4:.0f}" text-anchor="middle" class="m" font-size="11" fill="{SOFT}">{esc(f)}</text>')
    H = top + n * rh + 40
    body = f"""
{label(60, 56, "04 — Projects")}
<text x="58" y="120" class="s" font-size="48" font-weight="700" fill="{INK}" letter-spacing="-1.5">Real work<tspan fill="{ACCENT}">.</tspan> <tspan fill="{MUTE}">Real impact.</tspan></text>
{glass(40, 156, 1120, n * rh + 20, 22)}
<g transform="translate(0,10)">{rows}</g>
"""
    return svg(1200, H, body, orbs=[(1080, 40, 200, "#5b6cff", .35), (80, H, 170, "#2dd4bf", .14)])


# ───────────────────────────── CONNECT ─────────────────────────────
def connect_header():
    body = f"""
{label(60, 56, "05 — Contact")}
<text x="58" y="136" class="s" font-size="68" font-weight="700" fill="{INK}" letter-spacing="-2.5">Let's connect<tspan fill="{ACCENT}">.</tspan></text>
<text x="60" y="180" class="s" font-size="18" fill="{SOFT}">Ideas, collaboration, open source. Say hi.</text>
"""
    return svg(1200, 220, body, orbs=[(1050, 60, 200, "#5b6cff", .35), (80, 220, 150, "#2dd4bf", .14)])


def connect_card(badge, title, handle):
    body = f"""
{glass(1, 1, 338, 98, 22)}
<rect x="26" y="24" width="52" height="52" rx="14" fill="#fff" fill-opacity=".06" stroke="#fff" stroke-opacity=".2"/>
<text x="52" y="58" text-anchor="middle" class="s" font-size="20" font-weight="600" fill="{INK}">{esc(badge)}</text>
<text x="96" y="46" class="s" font-size="18" font-weight="600" fill="{INK}">{esc(title)}</text>
<text x="96" y="68" class="m" font-size="12" fill="{SOFT}">{esc(handle)}</text>
<text x="312" y="56" text-anchor="middle" class="s" font-size="22" fill="{MUTE}">↗</text>
"""
    return svg(340, 100, body, orbs=[(300, 20, 90, "#5b6cff", .30)])


def footer():
    body = f"""
<text x="600" y="48" text-anchor="middle" class="s" font-size="26" font-weight="700" fill="{INK}" letter-spacing="-.5">Ship beats perfect<tspan fill="{ACCENT}">.</tspan></text>
<text x="600" y="76" text-anchor="middle" class="m" font-size="11" fill="{MUTE}" letter-spacing="3">THANKS FOR VISITING</text>
"""
    return svg(1200, 100, body, orbs=[(600, 120, 220, "#5b6cff", .22)])


files = {
    "hero.svg": hero(), "earth.svg": earth(), "card.svg": card(), "stack.svg": stack(),
    "connect_header.svg": connect_header(), "footer.svg": footer(),
}
for name, badge, title, handle in CONNECT:
    files[f"connect_{name}.svg"] = connect_card(badge, title, handle)

for fn, content in files.items():
    with open(os.path.join(OUT, fn), "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", os.path.join("src", fn))
