#!/usr/bin/env python3
"""
Generates the SVG panels used by README.md  ->  ./src/*.svg
Theme: minimal + glassmorphism (neutral dark base, frosted glass panels, one soft accent).

Usage (from the repo root):
    pip install pillow numpy
    python3 generate_assets.py

* Your photo:      src/deval.jpeg  (embedded into the hero + ID card)
* Earth texture:   assets/earth.jpg (NASA Blue Marble, public domain)
Edit the CONFIG block to change text / skills, then re-run.
"""
import base64, io, math, os
import numpy as np
from PIL import Image, ImageEnhance

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "src")
ASSETS = os.path.join(HERE, "assets")
os.makedirs(OUT, exist_ok=True)

# ───────────────────────────── CONFIG ─────────────────────────────
NAME = "Deval Patel"
INITIALS = "DP"
LOCATION = "Gandhinagar, IN"
TAGLINE = "Building AI-powered products and full-stack apps, one commit at a time."
CHIPS = ["GEC Gandhinagar", "B.E. Computer Engineering", "AI / ML", "Full-Stack"]

STATS = [("5", "STARS"), ("5+", "PROJECTS"), ("3-6", "PARALLEL CLAUDES")]
SKILLS = [  # self-rated, change freely
    ("Full-Stack Web", 80),
    ("AI / ML", 65),
    ("DSA & Problem Solving", 70),
    ("Git & Open Source", 60),
]
CALLOUT = "Currently building SentinelAI: AI-driven disaster management & rescue."

STACK = [
    ("LANGUAGES", ["C", "C++", "Java", "Python", "JavaScript"]),
    ("AI / ML", ["NumPy", "Pandas", "Matplotlib", "Seaborn", "OpenCV", "scikit-learn"]),
    ("FRONTEND", ["React", "Next.js", "Tailwind", "Framer Motion", "GSAP"]),
    ("BACKEND", ["Node.js", "Express", "FastAPI"]),
    ("DATA & TOOLS", ["MongoDB", "PostgreSQL", "MySQL", "Git", "Linux", "Figma"]),
]
ORBITS = [  # rx, ry, tilt, seconds, reverse, skills
    (310, 84, -18, 34, 0, ["Python", "C++", "Java", "C"]),
    (450, 132, 14, 50, 1, ["React", "Next.js", "Tailwind", "JavaScript", "Node.js", "Express", "FastAPI"]),
    (530, 62, -4, 66, 0, ["MongoDB", "PostgreSQL", "MySQL", "Git", "Linux", "Figma"]),
    (380, 108, -34, 58, 1, ["NumPy", "Pandas", "Matplotlib", "Seaborn", "OpenCV", "scikit-learn"]),
]
CONNECT = [  # file, badge, title, handle
    ("linkedin", "in", "LinkedIn", "gecgce2024deval"),
    ("x", "X", "X / Twitter", "@Official_Deval"),
    ("stackoverflow", "SO", "Stack Overflow", "user 31278451"),
    ("email", "@", "Email", "pateldeval6050@gmail.com"),
    ("kaggle", "K", "Kaggle", "devalpatel20"),
    ("huggingface", "HF", "Hugging Face", "deval-020"),
    ("medium", "M", "Medium", "@pateldeval07"),
    ("contra", "Co", "Contra", "pateldeval07"),
]

ACCENT = "#8ea2ff"      # the only accent colour
INK = "#f3f4f6"         # primary text
SOFT = "#aab2c2"        # secondary text
MUTE = "#6b7385"        # labels
EARTH_START_LON = 78    # which longitude faces you at load (78 = India)
# ──────────────────────────────────────────────────────────────────


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def b64(img, fmt="JPEG", **kw):
    buf = io.BytesIO()
    img.save(buf, fmt, **kw)
    return base64.b64encode(buf.getvalue()).decode()


def load_photo():
    for n in ("deval.jpeg", "photo.jpg", "photo.jpeg", "photo.png"):
        p = os.path.join(OUT, n)
        if os.path.exists(p):
            im = Image.open(p).convert("RGB")
            im.thumbnail((520, 780))
            global PHOTO_AR
            PHOTO_AR = im.height / im.width
            return b64(im, "JPEG", quality=86, optimize=True)
    return None


PHOTO_AR = 1.5
PHOTO = load_photo()

STYLE = """
.s{font-family:Inter,'SF Pro Display','Segoe UI',Helvetica,Arial,sans-serif}
.m{font-family:'JetBrains Mono','SF Mono',Consolas,'Courier New',monospace}
@keyframes br{0%,100%{opacity:.5}50%{opacity:1}}
.br{animation:br 3.2s ease-in-out infinite}
"""


def svg(w, h, body, defs="", orbs=(), css=""):
    orb_svg = "".join(
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{c}" opacity="{o}" filter="url(#blur)"/>' for cx, cy, r, c, o in orbs)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<style>{STYLE}{css}</style>
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b0d12"/><stop offset="1" stop-color="#131723"/></linearGradient>
<linearGradient id="glass" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".11"/><stop offset="1" stop-color="#fff" stop-opacity=".03"/></linearGradient>
<linearGradient id="gstroke" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".40"/><stop offset=".5" stop-color="#fff" stop-opacity=".07"/><stop offset="1" stop-color="#fff" stop-opacity=".20"/></linearGradient>
<linearGradient id="bar" x1="0" x2="1"><stop offset="0" stop-color="{ACCENT}" stop-opacity=".55"/><stop offset="1" stop-color="#ffffff" stop-opacity=".9"/></linearGradient>
<linearGradient id="fade" x1="0" y1="0" x2="0" y2="1"><stop offset=".55" stop-color="#0b0d12" stop-opacity="0"/><stop offset="1" stop-color="#0b0d12" stop-opacity=".75"/></linearGradient>
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


def label(x, y, text, anchor="start"):
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" class="m" font-size="12" fill="{MUTE}" letter-spacing="3">'
            f'{esc(text.upper())}</text>')


def photo_box(x, y, w, h, rx, cid, zoom=1.32):
    """Your photo (top-aligned crop) clipped to a rounded rect, with a glass edge."""
    defs = f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}"/></clipPath>'
    if PHOTO:
        iw = w * zoom
        ih = iw * PHOTO_AR
        inner = (f'<image href="data:image/jpeg;base64,{PHOTO}" x="{x - (iw - w) / 2:.1f}" y="{y - ih * 0.055:.1f}" width="{iw:.1f}" height="{ih:.1f}" '
                 f'preserveAspectRatio="none" clip-path="url(#{cid})"/>'
                 f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="url(#fade)"/>')
    else:
        inner = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="#fff" fill-opacity=".05"/>'
                 f'<text x="{x+w/2}" y="{y+h/2+min(w,h)*0.14:.0f}" text-anchor="middle" class="s" font-weight="300" '
                 f'font-size="{min(w,h)*0.40:.0f}" fill="#fff" fill-opacity=".75">{INITIALS}</text>')
    edge = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="none" stroke="#fff" stroke-opacity=".28"/>'
    return defs, inner + edge


# ───────────────────────────── HERO ─────────────────────────────
def hero():
    W, H = 1200, 480
    pdefs, ph = photo_box(888, 66, 240, 348, 24, "ph")
    chips, x = "", 64
    for c in CHIPS:
        s, w = pill(x, 346, c, 13)
        chips += s
        x += w + 12
    body = f"""
{glass(24, 24, 1152, 432, 26)}
<text x="64" y="104" class="m" font-size="13" fill="{SOFT}" letter-spacing="3">SOFTWARE ENGINEER IN THE MAKING · {esc(LOCATION.upper())}</text>
<text x="60" y="226" class="s" font-size="96" font-weight="700" fill="{INK}" letter-spacing="-3">{esc(NAME)}<tspan fill="{ACCENT}">.</tspan></text>
<text x="64" y="282" class="s" font-size="20" fill="{SOFT}">{esc(TAGLINE)}</text>
{chips}
<rect x="876" y="54" width="264" height="372" rx="32" fill="#fff" fill-opacity=".05" stroke="#fff" stroke-opacity=".16"/>
{ph}
<rect x="852" y="362" width="204" height="44" rx="22" fill="#10131c" fill-opacity=".78" stroke="#fff" stroke-opacity=".26"/>
<circle cx="878" cy="384" r="4.5" fill="#5eead4" class="br"/>
<text x="894" y="389" class="s" font-size="14" font-weight="500" fill="#e5e7eb">Open to collaborate</text>
"""
    return svg(W, H, body, pdefs, orbs=[(1010, 90, 240, "#5b6cff", .55), (110, 460, 200, "#2dd4bf", .20)])


# ───────────────────────────── EARTH ─────────────────────────────
FRAMES = 60          # pre-rendered views of the globe (cross-faded for a smooth spin)
SPIN_SECONDS = 120   # one full rotation
TILT_DEG = 20        # axial tilt


def cloud_alpha(w=1200, h=600, seed=7):
    """Tileable fractal clouds (FFT noise) -> alpha 0..1."""
    rng = np.random.default_rng(seed)
    F = np.fft.fft2(rng.standard_normal((h, w)))
    f = np.sqrt(np.fft.fftfreq(w)[None, :] ** 2 + np.fft.fftfreq(h)[:, None] ** 2)
    f[0, 0] = 1
    amp = f ** -1.9 * np.exp(-(f / 0.30) ** 2)
    amp[0, 0] = 0
    n = np.real(np.fft.ifft2(F * amp))
    n = (n - n.mean()) / n.std()
    return np.clip((n - 0.35) / 1.3, 0, 1) ** 1.15 * 0.92


def bilinear(img, u, v):
    """Sample img (H,W[,C]) at float pixel coords, wrapping in u, clamping in v."""
    H, W = img.shape[:2]
    u = np.mod(u, W)
    v = np.clip(v, 0, H - 1.001)
    i0, j0 = np.floor(u).astype(int), np.floor(v).astype(int)
    i1 = (i0 + 1) % W
    fu, fv = u - i0, v - j0
    if img.ndim == 3:
        fu, fv = fu[..., None], fv[..., None]
    top = img[j0, i0] * (1 - fu) + img[j0, i1] * fu
    bot = img[j0 + 1, i0] * (1 - fu) + img[j0 + 1, i1] * fu
    return top * (1 - fv) + bot * fv


def render_globe(tex, clouds, lon0, px):
    """One orthographic view of Earth centred on longitude lon0 (degrees)."""
    r = px / 2
    j, i = np.mgrid[0:px, 0:px]
    x, y = (i + 0.5 - r) / r, (j + 0.5 - r) / r
    rr = x ** 2 + y ** 2
    inside = rr < 1.0
    z = np.sqrt(np.clip(1 - rr, 0, 1))
    t = math.radians(TILT_DEG)
    # undo the screen-plane tilt so the polar axis leans like the real Earth
    xr = x * math.cos(t) - y * math.sin(t)
    yr = x * math.sin(t) + y * math.cos(t)
    lat = np.arcsin(np.clip(-yr, -1, 1))
    lon = math.radians(lon0) + np.arctan2(xr, z)
    H, W = tex.shape[:2]
    u, v = (lon / (2 * math.pi) + 0.5) * W, (0.5 - lat / math.pi) * H
    col = bilinear(tex, u, v)
    ch, cw = clouds.shape
    ca = bilinear(clouds, (lon / (2 * math.pi) + 0.5) * cw, (0.5 - lat / math.pi) * ch)[..., None]
    water = np.clip((col[..., 2] - col[..., 0] - 8) / 60, 0, 1)[..., None] * (1 - ca)
    col = col * (1 - 0.82 * ca) + 255 * 0.82 * ca
    # lighting: sun from the upper left, soft terminator, ocean glint
    L = np.array([-0.55, -0.42, 0.72]); L /= np.linalg.norm(L)
    ndl = np.clip(x * L[0] + y * L[1] + z * L[2], 0, 1)
    light = (0.10 + 0.90 * ndl ** 0.75)[..., None]
    Hh = L + np.array([0, 0, 1.0]); Hh /= np.linalg.norm(Hh)
    spec = (np.clip(x * Hh[0] + y * Hh[1] + z * Hh[2], 0, 1) ** 60)[..., None] * water * 140
    col = col * light + spec
    # atmosphere on the limb
    rim = np.clip((1 - z) ** 2.6, 0, 1)[..., None]
    atmo = np.array([110.0, 175.0, 255.0])
    col = col * (1 - 0.55 * rim) + atmo * 0.55 * rim * (0.35 + 0.65 * light)
    col = np.where(inside[..., None], col, 8.0)
    return Image.fromarray(np.clip(col, 0, 255).astype(np.uint8), "RGB")


def earth():
    W, H, cx, cy, R = 1200, 790, 600, 450, 160
    px = 340
    tex = Image.open(os.path.join(ASSETS, "earth.jpg")).convert("RGB")
    tex = np.asarray(ImageEnhance.Color(tex).enhance(1.10)).astype(np.float32)
    clouds = cloud_alpha().astype(np.float32)
    frames = []
    for k in range(FRAMES):
        im = render_globe(tex, clouds, EARTH_START_LON - 360.0 * k / FRAMES, px)
        frames.append(b64(im, "JPEG", quality=72, optimize=True))

    img = lambda k: (f'<image id="f{k}" href="data:image/jpeg;base64,{frames[k]}" x="{cx-R}" y="{cy-R}" '
                     f'width="{2*R}" height="{2*R}"/>')
    defs = ("<clipPath id=\"ec\"><circle cx=\"%d\" cy=\"%d\" r=\"%d\"/></clipPath>" % (cx, cy, R)
            + "".join(img(k) for k in range(FRAMES))
            + '<radialGradient id="atmo" cx=".5" cy=".5" r=".5"><stop offset=".78" stop-color="#5aa9ff" stop-opacity=".40"/>'
              '<stop offset="1" stop-color="#5aa9ff" stop-opacity="0"/></radialGradient>')
    css = ".fa{opacity:1}"
    uses = f'<use href="#f0"/>'
    for k in range(1, FRAMES + 1):
        a, b = (k - 1) / FRAMES * 100, min(k / FRAMES * 100, 99.99)
        css += (f"@keyframes a{k}{{0%,{a:.3f}%{{opacity:0}}{b:.3f}%{{opacity:1}}100%{{opacity:{1 if k == FRAMES else 0}}}}}"
                f".a{k}{{animation:a{k} {SPIN_SECONDS}s linear infinite}}")
        uses += f'<use href="#f{k % FRAMES}" class="fa a{k}"/>'

    back, front, nodes = "", "", ""
    for (rx, ry, tilt, dur, rev, skills) in ORBITS:
        back += (f'<g transform="rotate({tilt} {cx} {cy})"><ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" '
                 f'stroke="#fff" stroke-opacity=".12" stroke-dasharray="2 8"/></g>')
        front += (f'<g transform="rotate({tilt} {cx} {cy})"><path d="M{cx-rx} {cy} A{rx} {ry} 0 0 0 {cx+rx} {cy}" fill="none" '
                  f'stroke="#fff" stroke-opacity=".26"/></g>')
        sw = 1 if rev else 0
        path = f"M{cx-rx} {cy} a{rx} {ry} 0 1 {sw} {2*rx} 0 a{rx} {ry} 0 1 {sw} {-2*rx} 0"
        n = len(skills)
        nodes += f'<g transform="rotate({tilt} {cx} {cy})">'
        for k, lab in enumerate(skills):
            w = 36 + len(lab) * 8.0
            nodes += (f'<g><animateMotion dur="{dur}s" begin="-{dur*k/n:.1f}s" repeatCount="indefinite" path="{path}"/>'
                      f'<g transform="rotate({-tilt})"><rect x="{-w/2:.1f}" y="-16" width="{w:.1f}" height="32" rx="16" fill="#10131c" fill-opacity=".80" stroke="#fff" stroke-opacity=".30"/>'
                      f'<circle cx="{-w/2+16:.1f}" cy="0" r="3" fill="{ACCENT}"/>'
                      f'<text x="{-w/2+28:.1f}" y="4.5" class="s" font-size="13" font-weight="500" fill="#e5e7eb">{esc(lab)}</text></g></g>')
        nodes += "</g>"
    count = sum(len(o[5]) for o in ORBITS)
    body = f"""
{label(60, 56, "01 — Tech orbit")}
<text x="58" y="128" class="s" font-size="60" font-weight="700" fill="{INK}" letter-spacing="-2">My tech world<tspan fill="{ACCENT}">.</tspan></text>
<text x="60" y="164" class="s" font-size="18" fill="{SOFT}">A planet that never stops spinning, just like my curiosity.</text>
{glass(930, 40, 230, 44, 22)}
<circle cx="954" cy="62" r="3.5" fill="{ACCENT}" class="br"/>
<text x="970" y="67" class="s" font-size="14" font-weight="500" fill="#e5e7eb">{count} technologies in orbit</text>
<circle cx="{cx}" cy="{cy}" r="{R+36}" fill="url(#atmo)"/>
{back}
<g clip-path="url(#ec)">{uses}</g>
<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="#bfe2ff" stroke-opacity=".22"/>
{front}
{nodes}
{label(cx, H-34, "skills in orbit", "middle")}
"""
    return svg(W, H, body, defs, orbs=[(cx, cy, 230, "#5b6cff", .30), (1060, 130, 150, "#2dd4bf", .12), (90, 720, 170, "#5b6cff", .16)], css=css)


# ───────────────────────────── ABOUT CARD ─────────────────────────────
def card():
    W, H = 1200, 580
    pdefs, ph = photo_box(100, 80, 260, 296, 20, "pc")
    tiles = ""
    for i, (v, l) in enumerate(STATS):
        x = 450 + i * 240
        tiles += (glass(x, 150, 220, 104, 16) +
                  f'<text x="{x+24}" y="208" class="s" font-size="46" font-weight="600" fill="{INK}" letter-spacing="-1">{esc(v)}</text>'
                  f'<text x="{x+24}" y="236" class="m" font-size="11" fill="{MUTE}" letter-spacing="2">{esc(l)}</text>')
    sk = ""
    for i, (lab, pct) in enumerate(SKILLS):
        y = 322 + i * 46
        sk += (f'<text x="450" y="{y}" class="s" font-size="15" fill="#d1d5db">{esc(lab)}</text>'
               f'<text x="1150" y="{y}" text-anchor="end" class="m" font-size="12" fill="{SOFT}">{pct}%</text>'
               f'<rect x="450" y="{y+12}" width="700" height="4" rx="2" fill="#fff" fill-opacity=".10"/>'
               f'<rect x="450" y="{y+12}" width="{7*pct}" height="4" rx="2" fill="url(#bar)">'
               f'<animate attributeName="width" from="0" to="{7*pct}" dur="1.2s" begin="0s" fill="freeze"/></rect>')
    body = f"""
{glass(80, 60, 300, 460, 28)}
{ph}
<text x="104" y="414" class="s" font-size="26" font-weight="600" fill="{INK}" letter-spacing="-.5">{esc(NAME)}</text>
<text x="104" y="438" class="s" font-size="14" fill="{SOFT}">B.E. Computer Engineering</text>
<text x="104" y="458" class="s" font-size="14" fill="{SOFT}">GEC Gandhinagar · Sem 5</text>
<rect x="104" y="476" width="236" height="1" fill="#fff" fill-opacity=".12"/>
<text x="104" y="500" class="m" font-size="11" fill="{MUTE}" letter-spacing="2">@DEVAL-020</text>
<circle cx="340" cy="496" r="4" fill="#5eead4" class="br"/>
{label(450, 76, "02 — About")}
<text x="448" y="128" class="s" font-size="44" font-weight="700" fill="{INK}" letter-spacing="-1.5">More than a marksheet<tspan fill="{ACCENT}">.</tspan></text>
{tiles}
{label(450, 296, "skill signal · self-rated")}
{sk}
{glass(450, 510, 700, 40, 20)}
<circle cx="474" cy="530" r="3.5" fill="{ACCENT}" class="br"/>
<text x="490" y="535" class="s" font-size="14" fill="#d1d5db">{esc(CALLOUT)}</text>
"""
    return svg(W, H, body, pdefs, orbs=[(1080, 80, 220, "#5b6cff", .40), (160, 540, 190, "#2dd4bf", .16)])


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


# ───────────────────────────── CONNECT ─────────────────────────────
def connect_header():
    body = f"""
{label(60, 56, "04 — Contact")}
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
    print("wrote", os.path.join("src", fn), f"({len(content)//1024} KB)")
