#!/usr/bin/env python3
"""basivo-studio: turn HTML/SVG into pixel-exact PNGs, icon sets and favicons with a headless
Chrome/Edge/Chromium/Brave that's already on the machine. Standard library only, any OS.

  studio.py doctor                          which browser will render
  studio.py sizes                           the size presets
  studio.py render <in.html|in.svg> <out.png> [--preset NAME | --size WxH] [--scale N] [--check]
                                            --check also writes <out>.check.png (max 800 px wide) to look at
  studio.py icons <logo.svg> [out_dir] [--bg #hex] [--name "App"]
                                            favicon.ico/.svg, apple-touch-icon, PWA icons, site.webmanifest
  studio.py brand [path]                    show the brand kit in use (./studio/brand.json, else ~/.basivo-studio/brand.json)
"""
import json
import os
import pathlib
import shutil
import struct
import subprocess
import sys
import tempfile

PRESETS = {
    "og": (1200, 630, "Open Graph / link preview (Facebook, LinkedIn, Slack, WhatsApp)"),
    "x-post": (1600, 900, "X/Twitter post image"),
    "x-banner": (1500, 500, "X/Twitter header"),
    "linkedin-post": (1200, 627, "LinkedIn feed image"),
    "linkedin-banner": (1584, 396, "LinkedIn profile banner"),
    "instagram-post": (1080, 1080, "Instagram square post, quote card"),
    "instagram-portrait": (1080, 1350, "Instagram portrait post, carousel slide"),
    "story": (1080, 1920, "Instagram/WhatsApp story, reel cover"),
    "youtube-thumb": (1280, 720, "YouTube thumbnail"),
    "youtube-banner": (2560, 1440, "YouTube channel art (safe area 1546x423 centred)"),
    "medium-cover": (1400, 788, "Medium / Substack / blog cover"),
    "blog-cover": (1600, 900, "Generic 16:9 blog or article hero"),
    "slide": (1920, 1080, "16:9 slide"),
    "logo": (1024, 1024, "Square logo export"),
    "github-social": (1280, 640, "GitHub repository social preview"),
}

BROWSERS = {
    "darwin": ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
               "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
               "/Applications/Chromium.app/Contents/MacOS/Chromium",
               "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"],
    "win32": [r"%ProgramFiles%\Google\Chrome\Application\chrome.exe",
              r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe",
              r"%LocalAppData%\Google\Chrome\Application\chrome.exe",
              r"%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe",
              r"%ProgramFiles%\Microsoft\Edge\Application\msedge.exe"],
    "linux": ["google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "microsoft-edge", "brave-browser"],
}
ICON_PNGS = {"favicon-16.png": 16, "favicon-32.png": 32, "favicon-48.png": 48,
             "apple-touch-icon.png": 180, "icon-192.png": 192, "icon-512.png": 512, "icon-maskable-512.png": 512}


def find_browser():
    env = os.environ.get("BASIVO_STUDIO_BROWSER")
    if env:
        return env if os.path.exists(env) or shutil.which(env) else None
    plat = "win32" if sys.platform.startswith("win") else "darwin" if sys.platform == "darwin" else "linux"
    for c in BROWSERS[plat]:
        c = os.path.expandvars(c)
        if os.path.isfile(c):
            return c
        if os.sep not in c and shutil.which(c):
            return shutil.which(c)
    return None


def png_size(path):
    with open(path, "rb") as f:
        head = f.read(24)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"{path} is not a PNG")
    return struct.unpack(">II", head[16:24])


def _svg_page(svg_path, bg=None, pad=0.0):
    """An HTML page that shows the SVG filling the viewport (optionally on a background, with padding)."""
    svg = pathlib.Path(svg_path).read_text(encoding="utf-8")
    inset = f"{pad * 100:.1f}%"
    return (f"<!doctype html><meta charset=utf-8><style>html,body{{margin:0;width:100%;height:100%;"
            f"background:{bg or 'transparent'}}}#m{{position:absolute;inset:{inset};display:flex}}"
            f"#m>svg{{width:100%;height:100%}}</style><div id=m>{svg}</div>")


def render(src, out, w, h, scale=1.0, html=None):
    """Screenshot `src` (or the given html text) at w x h CSS px; the PNG is (w*scale) x (h*scale)."""
    browser = find_browser()
    if not browser:
        sys.exit("No Chrome, Edge, Chromium or Brave found. Install Google Chrome (https://www.google.com/chrome/) "
                 "or set BASIVO_STUDIO_BROWSER to a Chromium-based browser.")
    out = os.path.abspath(out)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    tmp = None
    if html is None and str(src).lower().endswith(".svg"):
        html = _svg_page(src)
    if html is not None:
        # next to the source so relative assets (fonts, images) still resolve
        d = os.path.dirname(os.path.abspath(src)) if src else tempfile.gettempdir()
        fd, tmp = tempfile.mkstemp(suffix=".html", prefix=".studio-", dir=d)
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(html)
        src = tmp
    if os.path.exists(out):
        os.remove(out)
    args = [browser, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
            "--no-default-browser-check", "--default-background-color=00000000", "--allow-file-access-from-files",
            f"--window-size={int(w)},{int(h)}", f"--force-device-scale-factor={scale}",
            "--virtual-time-budget=4000",  # let web fonts and images load
            f"--screenshot={out}", pathlib.Path(os.path.abspath(src)).as_uri()]
    try:
        subprocess.run(args, capture_output=True, timeout=60)
    except subprocess.TimeoutExpired:
        sys.exit("The browser didn't finish in 60 s. Close stuck browser windows and try again.")
    finally:
        if tmp:
            os.remove(tmp)
    if not os.path.exists(out):
        sys.exit("The browser produced no image. Run `studio.py doctor`.")
    return png_size(out)


def check_copy(out, w, h, scale):
    """A small copy to look at: max 800 px wide, so checking an image costs few tokens."""
    if w * scale <= 800:
        return out
    path = out[:-4] + ".check.png"
    render(None, path, w, h, 800 / w, html=_img_page(out))
    return path


def _img_page(png):
    return (f"<!doctype html><style>html,body{{margin:0;background:transparent}}img{{width:100vw;height:100vh;display:block}}"
            f"</style><img src='{pathlib.Path(png).as_uri()}'>")


def write_ico(pngs, out):
    """ICO file with PNG-compressed entries (supported by every browser and Windows Vista+)."""
    datas = [open(p, "rb").read() for p in pngs]
    head = struct.pack("<HHH", 0, 1, len(datas))
    offset = 6 + 16 * len(datas)
    entries = b""
    for d in datas:
        w, h = struct.unpack(">II", d[16:24])
        entries += struct.pack("<BBBBHHII", w % 256, h % 256, 0, 0, 1, 32, len(d), offset)
        offset += len(d)
    with open(out, "wb") as f:
        f.write(head + entries + b"".join(datas))


def icons(svg, out_dir, bg=None, name="App"):
    os.makedirs(out_dir, exist_ok=True)
    made = {}
    for fname, px in ICON_PNGS.items():
        # iOS paints transparent corners black, and maskable icons get cropped to a circle: give both a
        # solid background and (maskable) a 10% safe-zone padding
        solid = fname in ("apple-touch-icon.png", "icon-maskable-512.png")
        page = _svg_page(svg, bg=(bg or "#ffffff") if solid else None, pad=0.1 if "maskable" in fname else 0.0)
        made[fname] = render(svg, os.path.join(out_dir, fname), px, px, html=page)
    write_ico([os.path.join(out_dir, f) for f in ("favicon-16.png", "favicon-32.png", "favicon-48.png")],
              os.path.join(out_dir, "favicon.ico"))
    shutil.copyfile(svg, os.path.join(out_dir, "favicon.svg"))
    manifest = {"name": name, "short_name": name, "icons": [
        {"src": "/icon-192.png", "sizes": "192x192", "type": "image/png"},
        {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png"},
        {"src": "/icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}],
        "theme_color": bg or "#ffffff", "background_color": bg or "#ffffff", "display": "standalone"}
    with open(os.path.join(out_dir, "site.webmanifest"), "w") as f:
        json.dump(manifest, f, indent=2)
    head = ('<link rel="icon" href="/favicon.ico" sizes="48x48">\n'
            '<link rel="icon" href="/favicon.svg" type="image/svg+xml">\n'
            '<link rel="apple-touch-icon" href="/apple-touch-icon.png">\n'
            '<link rel="manifest" href="/site.webmanifest">')
    return {"ok": True, "dir": os.path.abspath(out_dir), "files": sorted(os.listdir(out_dir)), "head_html": head,
            "check": os.path.join(os.path.abspath(out_dir), "icon-512.png")}


def brand(path=None):
    for p in [path, os.path.join("studio", "brand.json"), os.path.expanduser("~/.basivo-studio/brand.json")]:
        if p and os.path.isfile(p):
            return {"path": os.path.abspath(p), "brand": json.load(open(p, encoding="utf-8"))}
    return {"path": None, "brand": None, "hint": "No brand kit yet. /studio-brand creates studio/brand.json."}


def _opt(args, name, default=None):
    if name in args:
        i = args.index(name)
        val = args[i + 1] if i + 1 < len(args) else None
        del args[i:i + 2]
        return val
    return default


def main(argv):
    cmd, args = (argv[0] if argv else ""), list(argv[1:])
    if cmd == "doctor":
        b = find_browser()
        print(json.dumps({"ok": bool(b), "browser": b, "python": sys.version.split()[0]}))
    elif cmd == "sizes":
        for k, (w, h, what) in PRESETS.items():
            print(f"{k:20} {w}x{h:<6} {what}")
    elif cmd == "render" and len(args) >= 2:
        preset, size = _opt(args, "--preset"), _opt(args, "--size")
        scale = float(_opt(args, "--scale", "1"))
        check = "--check" in args
        args = [a for a in args if a != "--check"]
        if preset:
            if preset not in PRESETS:
                sys.exit(f"unknown preset {preset}; see `studio.py sizes`")
            w, h = PRESETS[preset][:2]
        elif size:
            w, h = (int(x) for x in size.lower().split("x"))
        else:
            w, h = PRESETS["logo"][:2] if args[0].lower().endswith(".svg") else PRESETS["og"][:2]
        pw, ph = render(args[0], args[1], w, h, scale)
        out = {"ok": True, "out": os.path.abspath(args[1]), "pixels": f"{pw}x{ph}"}
        if check:
            out["check"] = check_copy(os.path.abspath(args[1]), w, h, scale)
        print(json.dumps(out))
    elif cmd == "icons" and args:
        bg, name = _opt(args, "--bg"), _opt(args, "--name", "App")
        print(json.dumps(icons(args[0], args[1] if len(args) > 1 else "icons", bg, name), indent=2))
    elif cmd == "brand":
        print(json.dumps(brand(args[0] if args else None), indent=2))
    else:
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
