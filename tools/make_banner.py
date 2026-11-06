#!/usr/bin/env python3
"""Profile banners for github.com/jdominick05 as self-contained SVGs.

GitHub shows README images through its image proxy, where an SVG cannot load web fonts, so every
piece of lettering is converted to outlines here (HarfBuzz shaping + fontTools glyphs). The fonts are
OFL-licensed Google Fonts; pass their directory with --fonts.

    python tools/make_banner.py --fonts DIR --out assets            # every concept
    python tools/make_banner.py --fonts DIR --out assets --only tide

Needs: fonttools, uharfbuzz.
"""
import argparse
import io
import math
import pathlib

import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

W, H = 1280, 320
NAME = "Jordan Dominick"
TAGLINE = "local AI on AMD hardware: GPUs, NPUs and radios"

_FONTS = {}


def font(path, wght=None):
    """A static TTFont (variable fonts instanced at wght) and its bytes, cached."""
    key = (str(path), wght)
    if key not in _FONTS:
        tt = TTFont(path)
        if "fvar" in tt and wght is not None:
            tt = instancer.instantiateVariableFont(tt, {"wght": wght})
        buf = io.BytesIO()
        tt.save(buf)
        data = buf.getvalue()
        _FONTS[key] = (TTFont(io.BytesIO(data)), data)
    return _FONTS[key]


def text_path(path, text, size, x, y, wght=None, tracking=0.0, anchor="start"):
    """SVG path data for `text` with its baseline at y; returns (d, width)."""
    tt, data = font(path, wght)
    upem = tt["head"].unitsPerEm
    hbfont = hb.Font(hb.Face(hb.Blob(data)))
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(hbfont, buf, {"kern": True, "liga": True})
    s = size / upem
    track = tracking * size
    width = sum(p.x_advance for p in buf.glyph_positions) * s + track * max(0, len(text) - 1)
    if anchor == "middle":
        x -= width / 2
    elif anchor == "end":
        x -= width
    glyphs = tt.getGlyphSet()
    order = tt.getGlyphOrder()
    pen_x = 0.0
    parts = []
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        name = order[info.codepoint]
        pen = SVGPathPen(glyphs)
        gx = x + pen_x + pos.x_offset * s
        gy = y - pos.y_offset * s
        glyphs[name].draw(TransformPen(pen, (s, 0, 0, -s, gx, gy)))
        d = pen.getCommands()
        if d:
            parts.append(d)
        pen_x += pos.x_advance * s + track
    return " ".join(parts), width


def rnd(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


# ----------------------------------------------------------------------------------------------
# Concept 1: spectrum. A 2.4 GHz band as an analyzer would draw it: three Wi-Fi humps (channels
# 1 / 6 / 11) and three narrow BLE advertising spikes (37 / 38 / 39), gently breathing.
# ----------------------------------------------------------------------------------------------
def spectrum(F, static=False):
    sg, mono = F["sg"], F["mono"]
    n, x0, x1, base = 96, 56, W - 56, 292
    step = (x1 - x0) / n
    f0, f1 = 2400.0, 2483.5
    wifi = [2412, 2437, 2462]
    ble = [2402, 2426, 2480]

    def level(f):
        v = 0.06 + 0.03 * math.sin(f * 1.7) ** 2
        for c in wifi:
            v += 0.62 * math.exp(-(((f - c) / 7.5) ** 4))
        for c in ble:
            v += 0.85 * math.exp(-(((f - c) / 0.9) ** 2))
        return min(v, 1.0)

    bars = []
    for i in range(n):
        f = f0 + (f1 - f0) * (i + 0.5) / n
        h = 8 + level(f) * 96
        x = x0 + i * step
        dur = 2.6 + (i * 37 % 17) / 10
        delay = -((i * 53) % 29) / 10
        style = "" if static else f' style="animation-duration:{rnd(dur)}s;animation-delay:{rnd(delay)}s"'
        bars.append(
            f'<rect class="b" x="{rnd(x + 1.5)}" y="{rnd(base - h)}" width="{rnd(step - 3)}" height="{rnd(h)}" rx="1.5"{style}/>'
        )
    name_d, _ = text_path(sg, NAME, 80, 64, 124, wght=700, tracking=-0.01)
    tag_d, _ = text_path(mono, TAGLINE, 22, 66, 166, wght=400)
    lab_d, _ = text_path(mono, "2.400 GHz", 13, x0, base + 20, wght=500)
    lab2_d, _ = text_path(mono, "2.4835 GHz", 13, x1, base + 20, wght=500, anchor="end")
    loc_d, _ = text_path(mono, "MARYLAND, USA", 13, W - 64, 56, wght=500, tracking=0.18, anchor="end")
    grid = "".join(
        f'<line x1="{x0}" x2="{x1}" y1="{base - k * 24}" y2="{base - k * 24}"/>' for k in range(1, 5)
    )
    anim = "" if static else """
    .b{transform-box:fill-box;transform-origin:50% 100%;animation:breathe 3s ease-in-out infinite alternate}
    @keyframes breathe{from{transform:scaleY(.82)}to{transform:scaleY(1.04)}}
    @media (prefers-reduced-motion:reduce){.b{animation:none}}"""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{NAME}: {TAGLINE}">
  <title>{NAME}: {TAGLINE}</title>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#0a0f1e"/><stop offset="1" stop-color="#121a33"/>
    </linearGradient>
    <linearGradient id="bar" x1="0" y1="0" x2="{W}" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#2dd4bf"/><stop offset=".5" stop-color="#60a5fa"/><stop offset="1" stop-color="#a78bfa"/>
    </linearGradient>
    <linearGradient id="fade" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#fff" stop-opacity=".95"/><stop offset="1" stop-color="#fff" stop-opacity=".35"/>
    </linearGradient>
    <mask id="m"><rect x="0" y="180" width="{W}" height="{base - 180}" fill="url(#fade)"/></mask>
    <clipPath id="card"><rect width="{W}" height="{H}" rx="20"/></clipPath>
  </defs>
  <style>{anim}
  </style>
  <g clip-path="url(#card)">
    <rect width="{W}" height="{H}" fill="url(#bg)"/>
    <g stroke="#1d2847" stroke-width="1">{grid}</g>
    <g fill="url(#bar)" mask="url(#m)">{''.join(bars)}</g>
    <line x1="{x0}" x2="{x1}" y1="{base + .5}" y2="{base + .5}" stroke="#33426b" stroke-width="1"/>
    <path d="{lab_d}" fill="#4f5f88"/><path d="{lab2_d}" fill="#4f5f88"/>
    <path d="{loc_d}" fill="#4f5f88"/>
    <path d="{name_d}" fill="#f4f6ff"/>
    <path d="{tag_d}" fill="#93a7d1"/>
  </g>
</svg>
"""


# ----------------------------------------------------------------------------------------------
# Concept 2: tide. The Chesapeake at dusk: a low sun on the horizon, the water as layered swells.
# ----------------------------------------------------------------------------------------------
def tide(F, static=False):
    serif, mono = F["serif"], F["mono"]
    horizon = 222
    sun_x, sun_r = 1010, 74

    def wave(y, amp, length, phase):
        pts = []
        for i in range(0, 2 * W + 41, 8):
            pts.append(f"{i},{rnd(y + amp * math.sin(2 * math.pi * i / length + phase))}")
        return "M" + " L".join(pts) + f" L{2 * W + 40},{H} L0,{H} Z"

    layers = []
    specs = [
        (horizon + 6, 2.5, 160, 0.0, "#1b4a7a", 0.9, 48),
        (horizon + 22, 4, 210, 1.3, "#1a4370", 0.95, 40),
        (horizon + 42, 5, 260, 2.1, "#173b63", 1, 34),
        (horizon + 64, 6, 320, 0.7, "#133356", 1, 28),
        (horizon + 88, 7, 400, 2.9, "#0f2a48", 1, 22),
    ]
    for k, (y, amp, length, phase, color, op, dur) in enumerate(specs):
        cls = "" if static else f' class="w" style="animation-duration:{dur}s"'
        layers.append(f'<path{cls} d="{wave(y, amp, length, phase)}" fill="{color}" fill-opacity="{op}"/>')
    glints = []
    for k in range(9):
        y = horizon + 10 + k * 9
        half = 60 - k * 5.5
        glints.append(
            f'<rect x="{rnd(sun_x - half)}" y="{y}" width="{rnd(2 * half)}" height="2.2" rx="1.1" fill="#ffcf70" fill-opacity="{rnd(0.55 - k * 0.05)}"/>'
        )
    name_d, _ = text_path(serif, NAME, 92, 64, 132)
    tag_d, _ = text_path(mono, TAGLINE, 21, 67, 174, wght=400)
    loc_d, _ = text_path(mono, "CHESAPEAKE BAY · MARYLAND", 13, 67, 56, wght=500, tracking=0.2)
    anim = "" if static else """
    .w{animation:drift 40s linear infinite}
    @keyframes drift{from{transform:translateX(0)}to{transform:translateX(-640px)}}
    @media (prefers-reduced-motion:reduce){.w{animation:none}}"""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{NAME}: {TAGLINE}">
  <title>{NAME}: {TAGLINE}</title>
  <defs>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#0b1730"/><stop offset=".6" stop-color="#22305e"/><stop offset="1" stop-color="#6a4470"/>
    </linearGradient>
    <radialGradient id="glow" cx="{sun_x}" cy="{horizon}" r="420" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#ff8f70" stop-opacity=".42"/><stop offset=".55" stop-color="#d9708f" stop-opacity=".12"/><stop offset="1" stop-color="#d9708f" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="sun" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#ffe29a"/><stop offset="1" stop-color="#f59e4c"/>
    </linearGradient>
    <clipPath id="above"><rect width="{W}" height="{horizon}"/></clipPath>
    <clipPath id="card"><rect width="{W}" height="{H}" rx="20"/></clipPath>
  </defs>
  <style>{anim}
  </style>
  <g clip-path="url(#card)">
    <rect width="{W}" height="{H}" fill="url(#sky)"/>
    <rect width="{W}" height="{H}" fill="url(#glow)"/>
    <circle cx="{sun_x}" cy="{horizon}" r="{sun_r}" fill="url(#sun)" clip-path="url(#above)"/>
    <rect y="{horizon}" width="{W}" height="{H - horizon}" fill="#0e2442"/>
    {''.join(layers)}
    {''.join(glints)}
    <path d="{loc_d}" fill="#8fa6cc"/>
    <path d="{name_d}" fill="#fbf3e4"/>
    <path d="{tag_d}" fill="#c3d2ea"/>
  </g>
</svg>
"""


# ----------------------------------------------------------------------------------------------
# Concept 3: terminal. A shell window that types who I am and what I work on.
# ----------------------------------------------------------------------------------------------
def terminal(F, static=False):
    mono = F["mono"]
    amber, ink, dim = "#ffb547", "#e8e6e3", "#8b8f98"
    lines = [
        ("$ ", "whoami", 26, 400, 112),
        ("", NAME, 54, 700, 176),
        ("$ ", "cat focus.txt", 26, 400, 232),
        ("", TAGLINE, 24, 400, 272),
    ]
    out = []
    t = 0.4
    for i, (prompt, text, size, wght, y) in enumerate(lines):
        x = 56
        if prompt:
            pd, pw = text_path(mono, prompt, size, x, y, wght=600)
            out.append(f'<path d="{pd}" fill="{amber}"/>')
            x += pw
        d, w = text_path(mono, text, size, x, y, wght=wght)
        color = ink if i != 3 else "#c7cbd3"
        if static:
            out.append(f'<path d="{d}" fill="{color}"/>')
        else:
            chars = len(text)
            per = 0.055 if size < 40 else 0.07
            dur = chars * per
            vals = ";".join(rnd(w * k / chars) for k in range(chars + 1))
            out.append(
                f'<clipPath id="c{i}"><rect x="{rnd(x)}" y="{y - size}" width="0" height="{size * 1.4}">'
                f'<animate attributeName="width" values="{vals}" dur="{rnd(dur)}s" begin="{rnd(t)}s" fill="freeze" calcMode="discrete"/>'
                f"</rect></clipPath>"
                f'<path d="{d}" fill="{color}" clip-path="url(#c{i})"/>'
            )
            t += dur + (0.5 if prompt else 0.25)
    cur_y = 272
    _, tw = text_path(mono, TAGLINE, 24, 56, cur_y, wght=400)
    cursor_anim = "" if static else (
        f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1.06s" begin="{rnd(t)}s" repeatCount="indefinite"/>'
    )
    cursor_vis = "1" if static else "0"
    cursor = (
        f'<rect x="{rnd(56 + tw + 10)}" y="{cur_y - 22}" width="13" height="27" fill="{amber}" opacity="{cursor_vis}">'
        + ("" if static else f'<set attributeName="opacity" to="1" begin="{rnd(t - 0.01)}s"/>')
        + cursor_anim
        + "</rect>"
    )
    title_d, _ = text_path(mono, "jordan@maryland: ~", 14, W / 2, 33, wght=500, anchor="middle")
    dots = "".join(
        f'<circle cx="{32 + k * 22}" cy="28" r="6.5" fill="{c}"/>' for k, c in enumerate(["#4a4f59", "#4a4f59", "#4a4f59"])
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{NAME}: {TAGLINE}">
  <title>{NAME}: {TAGLINE}</title>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#14161b"/><stop offset="1" stop-color="#0d0e12"/>
    </linearGradient>
    <radialGradient id="warm" cx="0.15" cy="0.35" r="0.9">
      <stop offset="0" stop-color="#ffb547" stop-opacity=".07"/><stop offset="1" stop-color="#ffb547" stop-opacity="0"/>
    </radialGradient>
    <clipPath id="card"><rect width="{W}" height="{H}" rx="16"/></clipPath>
  </defs>
  <g clip-path="url(#card)">
    <rect width="{W}" height="{H}" fill="url(#bg)"/>
    <rect width="{W}" height="{H}" fill="url(#warm)"/>
    <rect width="{W}" height="56" fill="#1b1e24"/>
    <line x1="0" x2="{W}" y1="56.5" y2="56.5" stroke="#2a2e36"/>
    {dots}
    <path d="{title_d}" fill="{dim}"/>
    {''.join(out)}
    {cursor}
  </g>
  <rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="16" fill="none" stroke="#2a2e36"/>
</svg>
"""


CONCEPTS = {"spectrum": spectrum, "tide": tide, "terminal": terminal}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fonts", required=True, type=pathlib.Path)
    ap.add_argument("--out", required=True, type=pathlib.Path)
    ap.add_argument("--only", choices=sorted(CONCEPTS))
    ap.add_argument("--static", action="store_true", help="no animation (for previews)")
    a = ap.parse_args()
    F = {
        "sg": a.fonts / "SpaceGrotesk[wght].ttf",
        "mono": a.fonts / "JetBrainsMono[wght].ttf",
        "serif": a.fonts / "DMSerifDisplay-Regular.ttf",
    }
    a.out.mkdir(parents=True, exist_ok=True)
    for name, fn in CONCEPTS.items():
        if a.only and name != a.only:
            continue
        svg = fn(F, static=a.static)
        p = a.out / f"banner-{name}{'-static' if a.static else ''}.svg"
        p.write_text(svg)
        print(f"{p}  {len(svg) / 1024:.0f} KB")


if __name__ == "__main__":
    main()
