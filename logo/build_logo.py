#!/usr/bin/env python3
"""Build the LODs of PiCo logo from lods-of-pico-settings.json.

Three persons stand at the node positions of the RDF logo (seen from above),
linked by NDE-style slices, and are drawn through a simple perspective camera.
The same model is implemented in JavaScript in tweaker.html; keep both in sync.

Usage: python3 build_logo.py [settings.json]
Writes: lods-of-pico.svg, lods-of-pico-mark.svg, lods-of-pico-animated.svg
and refreshes the defaults embedded in tweaker.html.
"""
import json
import math
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

# RDF logo node layout in top view: left, top-right, bottom-right (x, y, radius)
TOP = [(103, 201, 47), (247, 115, 47), (249, 284, 47)]
EDGES = [(0, 1), (1, 2), (2, 0)]
CENTER = 200
FONT = "Arial, Helvetica, sans-serif"


def f1(v):
    return f"{round(v, 1):g}"


def depth_k(s):
    # perspective slider 0..100 -> depth spread K (lower K = stronger perspective)
    return 1620 - 15 * s["perspective"]


def head(x, y, r, k):
    rh = k * r
    return x, y - r - 0.1 * r - rh, rh


def gloss(x, y, r, color):
    a0, a1, g = math.radians(195), math.radians(265), math.radians(240)
    rr = 0.8 * r
    return (f'<path d="M {f1(x + rr * math.cos(a0))} {f1(y + rr * math.sin(a0))} '
            f'A {f1(rr)} {f1(rr)} 0 0 1 {f1(x + rr * math.cos(a1))} {f1(y + rr * math.sin(a1))}" '
            f'fill="none" stroke="{color}" stroke-width="{f1(0.09 * r)}" stroke-linecap="round"/>'
            f'<circle cx="{f1(x + 0.55 * r * math.cos(g))}" cy="{f1(y + 0.55 * r * math.sin(g))}" '
            f'r="{f1(0.08 * r)}" fill="{color}"/>')


def slices(a, b, s):
    (x1, y1, r1), (x2, y2, r2) = a, b
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    nx, ny = -uy, ux
    th = s["slice_thickness"]
    s0, s1 = r1 + 1.6 * th * r1 / 47, L - r2 - 1.6 * th * r2 / 47
    if s1 <= s0:
        return ""
    step = s["slice_spacing"] * (r1 + r2) / 94
    n = max(2, int((s1 - s0) // step) + 1)
    out = []
    for i in range(n):
        t = i / (n - 1)
        d = s0 + (s1 - s0) * t
        w_end = 0.42 * (r1 * (1 - t) + r2 * t)
        w_mid = 0.24 * (r1 + r2) / 2
        h = w_end - (w_end - w_mid) * math.sin(math.pi * t)
        cx, cy = x1 + ux * d, y1 + uy * d
        sw = th * (r1 * (1 - t) + r2 * t) / 47
        out.append(f'<line x1="{f1(cx + nx * h)}" y1="{f1(cy + ny * h)}" x2="{f1(cx - nx * h)}" '
                   f'y2="{f1(cy - ny * h)}" stroke="{s["colors"]["body"]}" stroke-width="{f1(sw)}" '
                   f'stroke-linecap="round"/>')
    return "".join(out)


def scene(s, rotate=None):
    """Return (svg fragment, (x0, y0, x1, y1)) for the three persons and their links."""
    rot = math.radians(s["rotate"] if rotate is None else rotate)
    sp, K, G = s["spacing"], depth_k(s), s["camera_height"]
    top = []
    for x, y, r in TOP:
        dx, dy = (x - CENTER) * sp, (y - CENTER) * sp
        top.append((CENTER + dx * math.cos(rot) - dy * math.sin(rot),
                    CENTER + dx * math.sin(rot) + dy * math.cos(rot), r))
    zf = max(p[1] for p in top)
    P = []
    for x, y, r in top:
        k = 1 / (1 + (zf - y) / K)
        P.append((CENTER + (x - CENTER) * k, zf - G + G * k, r * k))

    # painter's order: far to near; a link is drawn just after its farther end
    items = [(top[i][1], "p", i, None) for i in range(3)]
    items += [(min(top[i][1], top[j][1]) + 0.01, "e", i, j) for i, j in EDGES]
    items.sort(key=lambda it: it[0])

    c = s["colors"]
    out = []
    for _, kind, i, j in items:
        if kind == "e":
            out.append(slices(P[i], P[j], s))
            continue
        x, y, r = P[i]
        hx, hy, hr = head(x, y, r, s["head_size"])
        out.append(f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{f1(r)}" fill="{c["body"]}"/>')
        outline = f' stroke="{c["outline"]}" stroke-width="{f1(5 * r / 47)}"' if s["head_outline"] else ""
        out.append(f'<circle cx="{f1(hx)}" cy="{f1(hy)}" r="{f1(hr)}" fill="{c["head"]}"{outline}/>')
        if s["highlights"]:
            out.append(gloss(x, y, r, c["highlight"]) + gloss(hx, hy, hr, c["highlight"]))

    x0 = min(min(x - r, head(x, y, r, s["head_size"])[0] - head(x, y, r, s["head_size"])[2]) for x, y, r in P)
    x1 = max(max(x + r, head(x, y, r, s["head_size"])[0] + head(x, y, r, s["head_size"])[2]) for x, y, r in P)
    y0 = min(head(x, y, r, s["head_size"])[1] - head(x, y, r, s["head_size"])[2] for x, y, r in P)
    y1 = max(y + r for x, y, r in P)
    return "".join(out), (x0, y0, x1, y1)


def frame_box(bounds, text, pad=14):
    x0, y0, x1, y1 = bounds
    cx = (x0 + x1) / 2
    w = max(x1 - x0, 300) + 2 * pad
    ty = y1 + 52
    h = (ty + 14 if text else y1 + pad) - (y0 - pad)
    return cx - w / 2, y0 - pad, w, h, cx, ty


def wrap(body, box, s, text):
    vx, vy, w, h, cx, ty = box
    label = (f'<text x="{f1(cx)}" y="{f1(ty)}" text-anchor="middle" font-family="{FONT}" '
             f'font-weight="800" font-size="44" fill="{s["colors"]["text"]}">{s["label"]}</text>') if text else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{f1(vx)} {f1(vy)} {f1(w)} {f1(h)}" '
            f'width="{round(w * 5)}" height="{round(h * 5)}">\n{body}\n{label}\n</svg>\n')


def still(s, text):
    body, bounds = scene(s)
    return wrap(body, frame_box(bounds, text), s, text)


def animated(s):
    """Camera circles the group once; frames are swapped with discrete SMIL animation."""
    n, dur = s["animation"]["frames"], s["animation"]["duration_s"]
    frames, boxes = [], []
    for i in range(n):
        body, bounds = scene(s, s["rotate"] + 360 * i / n)
        frames.append(body)
        boxes.append(bounds)
    union = (min(b[0] for b in boxes), min(b[1] for b in boxes), max(b[2] for b in boxes), max(b[3] for b in boxes))
    groups = []
    for i, body in enumerate(frames):
        if i == 0:
            vals, times = "visible;hidden", f"0;{1 / n:.5f}"
        elif i == n - 1:
            vals, times = "hidden;visible", f"0;{i / n:.5f}"
        else:
            vals, times = "hidden;visible;hidden", f"0;{i / n:.5f};{(i + 1) / n:.5f}"
        groups.append(f'<g visibility="{"visible" if i == 0 else "hidden"}">'
                      f'<animate attributeName="visibility" values="{vals}" keyTimes="{times}" '
                      f'dur="{dur}s" repeatCount="indefinite" calcMode="discrete"/>{body}</g>')
    return wrap("\n".join(groups), frame_box(union, s["text"]), s, s["text"])


def horizontal(s):
    """Mark on the left, label on the right, for scarves and banners."""
    body, (x0, y0, x1, y1) = scene(s)
    pad, size = 14, 56
    tx, ty = x1 + 26, (y0 + y1) / 2 + size * 0.36
    tw = 0.54 * size * len(s["label"])  # measured width of bold Arial
    vx, vy, w, h = x0 - pad, y0 - pad, tx + tw + pad - (x0 - pad), y1 - y0 + 2 * pad
    label = (f'<text x="{f1(tx)}" y="{f1(ty)}" font-family="{FONT}" font-weight="800" '
             f'font-size="{size}" fill="{s["colors"]["text"]}">{s["label"]}</text>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{f1(vx)} {f1(vy)} {f1(w)} {f1(h)}" '
            f'width="{round(w * 5)}" height="{round(h * 5)}">\n{body}\n{label}\n</svg>\n')


def variant(s, spec):
    v = {**s, **{k: val for k, val in spec.items() if k not in ("colors", "layout")}}
    v["colors"] = {**s["colors"], **spec.get("colors", {})}
    return v, spec.get("layout", "stacked")


def refresh_tweaker(s):
    page = HERE / "tweaker.html"
    if not page.exists():
        return
    html = page.read_text()
    block = "/*SETTINGS*/" + json.dumps(s) + "/*END*/"
    page.write_text(re.sub(r"/\*SETTINGS\*/.*?/\*END\*/", lambda _: block, html, flags=re.S))


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "lods-of-pico-settings.json"
    s = json.loads(path.read_text())
    (HERE / "lods-of-pico.svg").write_text(still(s, s["text"]))
    (HERE / "lods-of-pico-mark.svg").write_text(still(s, False))
    (HERE / "lods-of-pico-animated.svg").write_text(animated(s))
    written = ["lods-of-pico.svg", "lods-of-pico-mark.svg", "lods-of-pico-animated.svg"]
    for name, spec in s.get("variants", {}).items():
        v, layout = variant(s, spec)
        out = horizontal(v) if layout == "horizontal" else still(v, v["text"])
        (HERE / f"lods-of-pico-{name}.svg").write_text(out)
        written.append(f"lods-of-pico-{name}.svg")
    refresh_tweaker(s)
    print("wrote", ", ".join(written))


if __name__ == "__main__":
    main()
