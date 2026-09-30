---
description: Turn a square SVG logo into every favicon and app icon (favicon.ico/.svg, apple-touch-icon, PWA 192/512, maskable) plus site.webmanifest and the <head> tags.
argument-hint: <logo.svg> [out_dir] [--bg #hex] [--name "App"]
---

`S='sh "${CLAUDE_PLUGIN_ROOT}/scripts/run" studio.py'`

1. The source must be a square SVG. No path given: use `logo.mark` from `$S brand`, else ask.
   A wide lockup: make a square mark first (ask, or offer `/studio-logo`).
2. `$S icons <logo.svg> <out_dir, default public/ if it exists, else studio/icons> --bg <brand paper or primary> --name "<brand name>"`
3. Read `favicon-32.png` (tiny) and `icon-maskable-512.png` via a check if unsure. If the mark
   is unreadable at 32 px, say so and offer a simplified small-size version.
4. Give the `head_html` and where to paste it (for Next.js, files in `public/` or `app/icon.svg`).
