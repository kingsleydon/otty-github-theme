"""Render an SVG preview of each theme in themes/ into assets/previews/.

Usage: python3 -I scripts/preview.py
"""
import glob
import os
import re
from html import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "previews")

W, H = 860, 420
TITLE_H, SIDEBAR_W = 40, 210
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
UI = "-apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif"


def parse(path):
    """Minimal reader for the flat TOML these themes use."""
    data, section = {}, ""
    text = open(path).read()
    palette = re.search(r"palette = \[(.*?)\]", text, flags=re.S).group(1)
    text = text.replace(palette, "")
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("["):
            section = line.strip("[]")
            continue
        m = re.match(r'([\w.-]+)\s*=\s*("[^"]*"|[^\s#]+)', line)
        if m:
            data[f"{section}.{m.group(1)}"] = m.group(2).strip('"')
    data["terminal.palette"] = re.findall(r"#[0-9A-Fa-f]+", palette)
    return data


def border_color(value):
    return value.split()[-1]


def render(t):
    p = t["terminal.palette"]
    bg, fg = t["terminal.background"], t["terminal.foreground"]
    side_bg = t["sidebar.background"]
    title_bg = t["titlebar.background"]
    line = border_color(t["sidebar.border-right"])
    muted = t["tab.foreground"]
    active_bg, active_fg = t["tab.active.background"], t["tab.active.foreground"]
    indicator = t["tab.active.indicator-color"]
    cursor, sel = t["terminal.cursor"], t["terminal.selection-background"]

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        f'<title>{escape(t["meta.name"])} for Otty</title>',
        f'<defs><clipPath id="w"><rect width="{W}" height="{H}" rx="12"/></clipPath></defs>',
        f'<g clip-path="url(#w)">',
        f'<rect width="{W}" height="{H}" fill="{bg}"/>',
        # sidebar runs the full height, like Otty's session column
        f'<rect width="{SIDEBAR_W}" height="{H}" fill="{side_bg}"/>',
        f'<rect x="{SIDEBAR_W}" width="{W - SIDEBAR_W}" height="{TITLE_H}" fill="{title_bg}"/>',
        f'<rect x="{SIDEBAR_W}" y="{TITLE_H - 1}" width="{W - SIDEBAR_W}" height="1" fill="{line}"/>',
        f'<rect x="{SIDEBAR_W - 1}" width="1" height="{H}" fill="{line}"/>',
    ]
    for i, c in enumerate(("#FF5F57", "#FEBC2E", "#28C840")):
        out.append(f'<circle cx="{20 + i * 20}" cy="20" r="6" fill="{c}"/>')
    out.append(f'<text x="{SIDEBAR_W + (W - SIDEBAR_W) / 2}" y="25" text-anchor="middle" font-family="{UI}" font-size="13" font-weight="500" fill="{t["titlebar.foreground"]}">~/otty-github-theme</text>')

    sessions = [("otty-github-theme", True), ("primer/primitives", False), ("~/.config/otty", False)]
    for i, (name, active) in enumerate(sessions):
        y = 56 + i * 34
        if active:
            out.append(f'<rect x="10" y="{y}" width="{SIDEBAR_W - 20}" height="28" rx="6" fill="{active_bg}"/>')
            out.append(f'<rect x="10" y="{y + 6}" width="3" height="16" rx="1.5" fill="{indicator}"/>')
        out.append(f'<text x="24" y="{y + 18.5}" font-family="{UI}" font-size="13" font-weight="{600 if active else 400}" fill="{active_fg if active else muted}">{escape(name)}</text>')

    # terminal content: (text, colour) runs per line
    x0, y0, lh = SIDEBAR_W + 24, TITLE_H + 34, 22
    lines = [
        [("❯ ", p[2]), ("git ", fg), ("status", fg)],
        [("On branch ", fg), ("main", p[6])],
        [("Changes to be committed:", fg)],
        [("        new file:   ", p[2]), ("themes/github-dark-default.ottytheme", p[2])],
        [("        modified:   ", p[1]), ("README.md", p[1])],
        [],
        [("❯ ", p[2]), ("otty theme import ", fg), ("github-dark.ottytheme", p[4])],
        [("Imported ", fg), ('"' + t["meta.name"] + '"', p[3]), (" (otty, " + t["meta.mode"] + ")", p[8])],
        [],
    ]
    for i, runs in enumerate(lines):
        if not runs:
            continue
        spans = "".join(f'<tspan fill="{c}">{escape(s)}</tspan>' for s, c in runs)
        out.append(f'<text x="{x0}" y="{y0 + i * lh}" font-family="{MONO}" font-size="14" xml:space="preserve">{spans}</text>')

    # prompt with a selection and the cursor
    py = y0 + len(lines) * lh
    out.append(f'<rect x="{x0 + 17}" y="{py - 15}" width="68" height="20" fill="{sel}"/>')
    out.append(f'<text x="{x0}" y="{py}" font-family="{MONO}" font-size="14" xml:space="preserve"><tspan fill="{p[2]}">❯ </tspan><tspan fill="{t["terminal.selection-foreground"]}">selected</tspan></text>')
    out.append(f'<rect x="{x0 + 92}" y="{py - 14}" width="9" height="18" fill="{cursor}"/>')

    # the 16 ANSI colours
    sw, gap = 30, 6
    sy = H - 2 * sw - gap - 22
    for i, c in enumerate(p):
        row, col = divmod(i, 8)
        out.append(f'<rect x="{x0 + col * (sw + gap)}" y="{sy + row * (sw + gap)}" width="{sw}" height="{sw}" rx="5" fill="{c}" stroke="{line}" stroke-width="1"/>')

    out += ["</g>", f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="11.5" fill="none" stroke="{line}"/>', "</svg>"]
    return "\n".join(out) + "\n"


os.makedirs(OUT, exist_ok=True)
for path in sorted(glob.glob(os.path.join(ROOT, "themes", "*.ottytheme"))):
    dest = os.path.join(OUT, os.path.basename(path).replace(".ottytheme", ".svg"))
    open(dest, "w").write(render(parse(path)))
    print(dest)
