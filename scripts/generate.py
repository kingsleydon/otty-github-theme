"""Generate Otty themes from GitHub's official VS Code theme (github-vscode-theme).

Usage: python3 -I scripts/generate.py <extension-dir> <themes-dir>

<extension-dir> is an unpacked github-vscode-theme VSIX (the folder holding
package.json and themes/). scripts/update.sh downloads one and runs this.
"""
import json
import os
import re
import sys

SRC, OUT = sys.argv[1], sys.argv[2]
VERSION = json.load(open(os.path.join(SRC, "package.json")))["version"]

ANSI = ["Black", "Red", "Green", "Yellow", "Blue", "Magenta", "Cyan", "White"]

# VS Code's built-in fallbacks for keys a variant leaves unset.
DEFAULT_SELECTION = {"dark": "#264F78", "light": "#ADD6FF"}


def expand(v):
    """#FFF -> #FFFFFF, #FFF8 -> #FFFFFF88."""
    v = v.upper()
    if re.fullmatch(r"#[0-9A-F]{3,4}", v):
        v = "#" + "".join(ch * 2 for ch in v[1:])
    return v


def slug(label):
    return re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-")


def render(label, path, ui):
    c = {k: expand(v) for k, v in json.load(open(os.path.join(SRC, path)))["colors"].items() if isinstance(v, str)}
    mode = "light" if ui in ("vs", "hc-light") else "dark"

    def g(key):
        return f'"{c[key]}"'

    if "editor.selectionBackground" in c:
        sel, sel_src = c["editor.selectionBackground"], "editor.selectionBackground"
    else:
        sel, sel_src = DEFAULT_SELECTION[mode], "VS Code default (theme leaves it unset)"
    if "editor.selectionForeground" in c:
        sel_fg, sel_fg_src = c["editor.selectionForeground"], "editor.selectionForeground"
    else:
        sel_fg, sel_fg_src = c["terminal.foreground"], "terminal.foreground"
    cursor_key = "terminalCursor.foreground" if "terminalCursor.foreground" in c else "editorCursor.foreground"

    normal = ", ".join(f'"{c["terminal.ansi" + n]}"' for n in ANSI[:4])
    normal2 = ", ".join(f'"{c["terminal.ansi" + n]}"' for n in ANSI[4:])
    bright = ", ".join(f'"{c["terminal.ansiBright" + n]}"' for n in ANSI[:4])
    bright2 = ", ".join(f'"{c["terminal.ansiBright" + n]}"' for n in ANSI[4:])

    return f'''[meta]
name        = "{label}"
author      = "Based on GitHub's VS Code theme (Primer)"
mode        = "{mode}"
description = "{label}, ported from the official GitHub VS Code theme (v{VERSION})."

# Every colour is taken verbatim from GitHub's official VS Code theme,
# "{label}" (github-vscode-theme {VERSION}, {path.lstrip("./")}).
# The VS Code key each value comes from is noted alongside it.

[terminal]
foreground           = {g("terminal.foreground")}   # terminal.foreground
background           = {g("editor.background")}   # editor.background
cursor               = {g(cursor_key)}   # {cursor_key}
cursor-text          = {g("editor.background")}
selection-foreground = "{sel_fg}"   # {sel_fg_src}
selection-background = "{sel}"   # {sel_src}
# palette: terminal.ansiBlack … ansiWhite, then ansiBrightBlack … ansiBrightWhite
palette = [
    {normal},
    {normal2},
    {bright},
    {bright2},
]

[cursor.bar]
color = {g(cursor_key)}

[cursor.underline]
color = {g(cursor_key)}

[token]
foreground = {g("foreground")}   # foreground
secondary  = {g("descriptionForeground")}   # descriptionForeground
tertiary   = {g("terminal.ansiBrightBlack")}   # terminal.ansiBrightBlack
accent     = {g("textLink.foreground")}   # textLink.foreground
success    = {g("terminal.ansiGreen")}   # terminal.ansiGreen
warning    = {g("terminal.ansiYellow")}   # terminal.ansiYellow
danger     = {g("errorForeground")}   # errorForeground
hover-bg   = {g("list.hoverBackground")} # list.hoverBackground
active-bg  = {g("list.activeSelectionBackground")} # list.activeSelectionBackground
radius     = 6

[panel]
background = {g("editor.background")}   # editor.background
surface    = {g("editorWidget.background")}   # editorWidget.background
border     = {g("panel.border")}   # panel.border

[window]
background = {g("editor.background")}
material   = "none"

[titlebar]
background  = {g("titleBar.activeBackground")}  # titleBar.activeBackground
foreground  = {g("titleBar.activeForeground")}  # titleBar.activeForeground
font-weight = 500

[titlebar.unfocused]
background = {g("titleBar.inactiveBackground")}   # titleBar.inactiveBackground
foreground = {g("titleBar.inactiveForeground")}   # titleBar.inactiveForeground

# Session list = VS Code's Explorer list + Activity Bar indicator.
[sidebar]
background   = {g("sideBar.background")}           # sideBar.background
border-right = "1px solid {c["sideBar.border"]}" # sideBar.border
material     = "none"

[tab]
radius      = 6
foreground  = {g("activityBar.inactiveForeground")}            # activityBar.inactiveForeground
font-weight = 400

[tab.hover]
background = {g("list.hoverBackground")}           # list.hoverBackground
foreground = {g("list.hoverForeground")}             # list.hoverForeground

[tab.active]
background      = {g("list.activeSelectionBackground")}      # list.activeSelectionBackground
foreground      = {g("list.activeSelectionForeground")}        # list.activeSelectionForeground
font-weight     = 600
indicator       = "bar"
indicator-color = {g("activityBar.activeBorder")}        # activityBar.activeBorder

[tab.active.unfocused]
background      = {g("list.inactiveSelectionBackground")}      # list.inactiveSelectionBackground
foreground      = {g("list.inactiveSelectionForeground")}        # list.inactiveSelectionForeground
indicator-color = {g("tab.unfocusedActiveBorderTop")}        # tab.unfocusedActiveBorderTop

# Top/bottom tab strip = VS Code's editor tabs.
[tab-bar]
background    = {g("editorGroupHeader.tabsBackground")}           # editorGroupHeader.tabsBackground
border-bottom = "1px solid {c["editorGroupHeader.tabsBorder"]}" # editorGroupHeader.tabsBorder

[tab-bar.tab]
background = {g("tab.inactiveBackground")}             # tab.inactiveBackground
foreground = {g("tab.inactiveForeground")}             # tab.inactiveForeground
border     = "1px solid {c["tab.border"]}"   # tab.border

[tab-bar.tab.hover]
background = {g("tab.hoverBackground")}             # tab.hoverBackground

[tab-bar.tab.active]
background      = {g("tab.activeBackground")}        # tab.activeBackground
foreground      = {g("tab.activeForeground")}        # tab.activeForeground
indicator-color = {g("tab.activeBorderTop")}        # tab.activeBorderTop

[container]
background = {g("editor.background")}             # editor.background
radius     = 0

[divider]
color = {g("editorGroup.border")}                  # editorGroup.border
width = 1
'''


for t in json.load(open(os.path.join(SRC, "package.json")))["contributes"]["themes"]:
    label = t["label"].replace(" (Beta)", "")
    dest = os.path.join(OUT, slug(label) + ".ottytheme")
    open(dest, "w").write(render(label, t["path"], t["uiTheme"]))
    print(dest)
