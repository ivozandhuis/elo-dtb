#!/usr/bin/env python3
"""Draw logo/mockups.svg: the built logo variants on a cap, scarf, hoodie and t-shirt.

Run after build_logo.py. Usage: python3 build_mockups.py
"""
import re
from pathlib import Path
L = str(Path(__file__).resolve().parent) + "/"
def sym(name, sid):
    src = open(L + f"lods-of-pico-{name}.svg").read()
    vb = re.search(r'viewBox="([^"]*)"', src).group(1)
    inner = src.split(">", 1)[1].rsplit("</svg>", 1)[0].strip()
    return f'<symbol id="{sid}" viewBox="{vb}">{inner}</symbol>', [float(v) for v in vb.split()]
defs, dims = [], {}
for name, sid in [("dark-mark-embroidery", "cap"), ("mono-white-horizontal", "scarf"), ("dark", "hood"), ("", "tee")]:
    s, vb = sym(name, sid) if name else (lambda r: (f'<symbol id="tee" viewBox="{r[1]}">{r[0]}</symbol>', [float(v) for v in r[1].split()]))(
        (open(L + "lods-of-pico.svg").read().split(">", 1)[1].rsplit("</svg>", 1)[0].strip(), re.search(r'viewBox="([^"]*)"', open(L + "lods-of-pico.svg").read()).group(1)))
    defs.append(s); dims[sid] = vb
def use(sid, cx, cy, w):
    vb = dims[sid]; h = w * vb[3] / vb[2]
    return f'<use href="#{sid}" x="{cx - w/2:.1f}" y="{cy - h/2:.1f}" width="{w:.1f}" height="{h:.1f}"/>'
NAVY, BLUE, BG = "#1A2550", "#1438F5", "#F4F1EA"
def panel(x, y, inner, label):
    return (f'<rect x="{x}" y="{y}" width="320" height="230" rx="12" fill="{BG}"/>'
            f'<g transform="translate({x},{y})">{inner}</g>'
            f'<text class="ts" x="{x+160}" y="{y+250}" text-anchor="middle">{label}</text>')
cap = (f'<path d="M 92 140 Q 92 52 160 50 Q 228 52 228 140 Q 160 152 92 140 Z" fill="{NAVY}"/>'
       f'<path d="M 160 50 L 160 146 M 160 50 Q 122 68 116 143 M 160 50 Q 198 68 204 143" stroke="#141D40" stroke-width="1.6" fill="none"/>'
       f'<circle cx="160" cy="51" r="5" fill="#141D40"/>'
       f'<circle cx="124" cy="82" r="2.2" fill="#141D40"/><circle cx="196" cy="82" r="2.2" fill="#141D40"/>'
       f'<path d="M 92 140 Q 160 152 228 140 Q 246 150 226 170 Q 160 206 94 170 Q 74 150 92 140 Z" fill="#141D40"/>'
       f'<path d="M 100 158 Q 160 186 220 158" stroke="#26336A" stroke-width="1.2" fill="none" stroke-dasharray="3 2"/>'
       + use("cap", 160, 106, 70))
scarf = (f'<g stroke="{BLUE}" stroke-width="2.5" stroke-linecap="round">'
         + "".join(f'<line x1="18" y1="{y}" x2="6" y2="{y}"/><line x1="302" y1="{y}" x2="314" y2="{y}"/>' for y in range(88, 156, 7))
         + '</g>'
         f'<rect x="18" y="85" width="284" height="70" rx="3" fill="{BLUE}"/>'
         f'<rect x="30" y="85" width="6" height="70" fill="#FFFFFF"/><rect x="42" y="85" width="3" height="70" fill="#FFFFFF"/>'
         f'<rect x="284" y="85" width="6" height="70" fill="#FFFFFF"/><rect x="275" y="85" width="3" height="70" fill="#FFFFFF"/>'
         + use("scarf", 160, 120, 170))
hood = (f'<path d="M 118 30 L 96 40 Q 78 50 74 82 L 64 190 L 66 204 L 88 206 L 90 192 L 100 94 L 100 200 L 102 216 L 218 216 L 220 200 L 220 94 L 230 192 L 232 206 L 254 204 L 256 190 L 246 82 Q 242 50 224 40 L 202 30 Q 160 40 118 30 Z" fill="{NAVY}"/>'
        f'<path d="M 100 200 L 220 200 M 64 190 L 90 192 M 230 192 L 256 190 M 100 94 L 100 200 M 220 94 L 220 200" stroke="#141D40" stroke-width="1.6" fill="none"/>'
        f'<path d="M 118 30 Q 160 18 202 30 Q 207 70 160 88 Q 113 70 118 30 Z" fill="#141D40"/>'
        + use("hood", 160, 138, 88)
        + f'<text x="160" y="192" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-weight="700" font-size="6" letter-spacing="1" fill="#8FA2FF">NDE HACKALOD 2026</text>')
tee = (f'<path d="M 136 22 Q 160 40 184 22 L 225 34 L 265 82 L 242 100 L 221 80 L 220 212 Q 160 216 100 212 L 99 80 L 78 100 L 55 82 L 95 34 Z" fill="#FFFFFF" stroke="#C9C5BA" stroke-width="1.5" stroke-linejoin="round"/>'
       f'<path d="M 136 22 Q 160 46 184 22" fill="none" stroke="#C9C5BA" stroke-width="1.5"/>'
       f'<path d="M 99 80 L 95 34 M 221 80 L 225 34" stroke="#E4E1D8" stroke-width="1" fill="none"/>'
       + use("tee", 160, 98, 64))
body = (panel(10, 10, cap, "Cap · embroidered mark, no highlights")
        + panel(350, 10, scarf, "Scarf · one-colour white on NDE blue")
        + panel(10, 280, hood, "Hoodie back · dark version")
        + panel(350, 280, tee, "T-shirt front · full colour"))
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 680 550" role="img"><title>LODs of PiCo merch mockups</title>'
       f'<desc>The final logo on a cap, scarf, hoodie back and t-shirt front.</desc><defs>{"".join(defs)}</defs>{body}</svg>')
open(L + "mockups.svg", "w").write(svg)
print("wrote mockups.svg")
