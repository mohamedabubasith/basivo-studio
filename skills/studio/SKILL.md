---
name: studio
description: Make logos, icons, favicons, blog covers, social images (Open Graph, X, LinkedIn, Instagram, YouTube thumbnails), quote cards, banners, carousels and simple diagrams as real files, by writing HTML/SVG and rendering it to exact-size PNGs with a local headless browser. Use when the user asks for a logo, icon, favicon, cover, thumbnail, banner, social card or any designed image with text. Not for photographs or realistic scenes.
---

# basivo-studio

You design with code: SVG for logos and icons, HTML/CSS for everything else, then
`studio.py` renders pixel-exact PNGs. Text is always spelled right, logos stay vector,
and the result is editable.

`S='sh "${CLAUDE_PLUGIN_ROOT}/scripts/run" studio.py'`

## Workflow

1. **Brand first.** `$S brand`. If there's a kit, use its colours, fonts and logo on
   every image. If not and the work is brand-related, offer `/studio-brand` (one
   question round), otherwise pick a small palette and say which.
2. **Workspace.** Put sources and outputs in `studio/<slug>/` in the current project
   (or where the user asks). Keep the `.html`/`.svg` source next to the PNG so it can
   be edited later.
3. **Write one self-contained file.** Inline CSS. Web fonts only from Google Fonts
   (`<link>`), images by relative path or data URI. Size the root element to exactly
   the preset (`$S sizes`), `margin:0`.
4. **Render with a check copy:** `$S render in.html out.png --preset og --check`.
   Use `--scale 2` for crisp final exports.
5. **Look before you hand over.** Read the `check` PNG (max 800 px wide, cheap). Fix
   clipping, overflow, low contrast, cramped margins, widows, and anything that looks
   templated. At most 2 fix rounds, then show the user.
6. **Hand over:** the PNG path(s), what you made in one line, and offer one change.

## Design rules (the "not AI-looking" part)

- **One idea per image.** One headline (≤ 8 words), an optional line under it, and one
  visual. Cut everything else.
- **Real typography.** A clear hierarchy of 2-3 sizes, one or two families, tight
  headline line height (1.05-1.15), comfortable body (1.4-1.6). The headline is readable
  at thumbnail size: ≥ 64 px on a 1200-wide canvas.
- **Restrained colour.** Brand colours, or 1 accent on a neutral. Contrast ≥ 4.5:1 for
  text. Avoid the tells: purple-to-blue gradients, glowing orbs, glassmorphism blobs,
  random sparkles, neon on black, rainbow meshes, emoji as decoration.
- **Space and grid.** Margins ≥ 6% of the width; align to a grid; leave real empty space.
  Asymmetric layouts beat everything-centred.
- **Texture over gloss.** Flat colour, a subtle grain or paper tone, a crisp shape, a
  real screenshot or chart. Soft shadows only if they mean something.
- **Safe zones.** Keep text out of the outer 5% (platform crops); YouTube thumbnails:
  nothing important bottom-right (timestamp); banners: centre-weight for mobile crops.
- **No fake UI or fake logos** of real companies, and no real people's likeness.

## Details per job

- Logos, marks, wordmarks, icon systems: read `references/logos.md`.
- Covers, social images, thumbnails, quote cards, carousels, diagrams:
  read `references/social-images.md`.

## Tokens

Write the file once, then make targeted edits; don't re-read your own source. Look at
`check` copies, never the full-size export, and only after a change. Use
`$S icons` for icon sets instead of rendering sizes one by one.

## Can't do

Photographs, realistic people, products or scenes. Say so, and offer a designed
alternative (type-led, shapes, a chart, the user's own photo placed in a layout).
