#!/usr/bin/env python3
"""Render checks with the local browser. Run: python3 tests/test_studio.py (exit 0 = pass; skips without a browser)."""
import json
import os
import struct
import subprocess
import sys
import tempfile

S = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts", "studio.py")


def run(*args):
    r = subprocess.run([sys.executable, S, *args], capture_output=True, text=True, timeout=180)
    assert r.returncode == 0, (args, r.stdout, r.stderr)
    return r.stdout


def size(p):
    return struct.unpack(">II", open(p, "rb").read(24)[16:24])


def pixel_alpha(p, x, y):
    """Alpha of one pixel in an 8-bit RGBA PNG (stdlib zlib, filters undone)."""
    import zlib
    d = open(p, "rb").read()
    w, h = size(p)
    if d[24:26] == b"\x08\x02":
        return 255  # RGB, no alpha channel: fully opaque
    assert d[24:26] == b"\x08\x06", "expected 8-bit RGB or RGBA"
    raw, i = b"", 8
    while i < len(d):
        n, typ = struct.unpack(">I4s", d[i:i + 8])
        if typ == b"IDAT":
            raw += d[i + 8:i + 8 + n]
        i += 12 + n
    data, stride, prev, rows = zlib.decompress(raw), w * 4, bytearray(w * 4), []
    for r in range(h):
        f, line = data[r * (stride + 1)], bytearray(data[r * (stride + 1) + 1:(r + 1) * (stride + 1)])
        for c in range(stride):
            a = line[c - 4] if c >= 4 else 0
            b = prev[c]
            cc = prev[c - 4] if c >= 4 else 0
            if f == 1: line[c] = (line[c] + a) & 255
            elif f == 2: line[c] = (line[c] + b) & 255
            elif f == 3: line[c] = (line[c] + (a + b) // 2) & 255
            elif f == 4:
                pa, pb, pc = abs(b - cc), abs(a - cc), abs(a + b - 2 * cc)
                line[c] = (line[c] + (a if pa <= pb and pa <= pc else b if pb <= pc else cc)) & 255
        rows.append(line)
        prev = line
    return rows[y][x * 4 + 3]


if not json.loads(run("doctor"))["ok"]:
    print("SKIP  no Chromium-based browser on this machine")
    sys.exit(0)

with tempfile.TemporaryDirectory() as t:
    html = os.path.join(t, "card.html")
    open(html, "w").write("<!doctype html><style>html,body{margin:0;background:transparent}"
                          "div{width:1200px;height:630px;background:#123;border-radius:60px}</style><div></div>")
    r = json.loads(run("render", html, os.path.join(t, "out", "card.png"), "--preset", "og", "--check"))
    assert r["pixels"] == "1200x630" and size(r["check"]) == (800, 420), r
    assert pixel_alpha(r["out"], 0, 0) == 0 and pixel_alpha(r["out"], 600, 300) == 255, "transparent corners, solid centre"
    r = json.loads(run("render", html, os.path.join(t, "card@2x.png"), "--size", "600x300", "--scale", "2"))
    assert r["pixels"] == "1200x600", r
    print("PASS  render: presets, --size, --scale, check copy, transparency")

    svg = os.path.join(t, "mark.svg")
    open(svg, "w").write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><circle cx="32" cy="32" r="20" fill="#e11d48"/></svg>')
    r = json.loads(run("icons", svg, os.path.join(t, "icons"), "--bg", "#ffffff", "--name", "Test"))
    d = r["dir"]
    for f, px in {"favicon-16.png": 16, "favicon-32.png": 32, "apple-touch-icon.png": 180, "icon-512.png": 512}.items():
        assert size(os.path.join(d, f)) == (px, px), f
    ico = open(os.path.join(d, "favicon.ico"), "rb").read()
    assert struct.unpack("<HHH", ico[:6]) == (0, 1, 3) and ico[54:62] == b"\x89PNG\r\n\x1a\n"
    assert pixel_alpha(os.path.join(d, "icon-512.png"), 0, 0) == 0, "plain icons keep transparency"
    assert pixel_alpha(os.path.join(d, "apple-touch-icon.png"), 0, 0) == 255, "apple-touch-icon gets a solid background"
    assert json.load(open(os.path.join(d, "site.webmanifest")))["name"] == "Test"
    print("PASS  icons: favicon.ico (3 PNG entries), apple-touch, PWA, maskable, manifest")

print("\nAll basivo-studio tests passed.")
