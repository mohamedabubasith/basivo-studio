# Changelog

## [0.1.1] - 2026-09-30

### Fixed
- Images were rendered at 1x and looked soft on retina screens. Everything now
  renders at 2x by default (`--scale 1` for exact pixels).
- Logos looked amateur: the logo guide now requires geometric construction on a
  grid (true arcs, one stroke weight, mirrored symmetry, no floating accents),
  HTML wordmarks with ligatures off, a board with a 64/32/16 px row, and a scored
  critique of every concept at 512 px before the user sees it.
- Colours and fonts now come from the project's theme (Tailwind, CSS variables,
  existing logo) when there's no brand kit, instead of an invented palette.

### Added
- `studio.py zoom <png> x,y,w,h`: a full-resolution crop to check fine detail.
- The finished image is opened for the user.

## [0.1.0] - 2026-09-30

### Added
- `studio.py`: renders HTML/SVG to exact-size PNGs with the local Chrome, Edge,
  Chromium or Brave (headless, transparent backgrounds, `--scale`, and a
  `--check` copy capped at 800 px for cheap visual checks).
- 15 size presets (Open Graph, X, LinkedIn, Instagram, YouTube, Medium, slides,
  GitHub social preview and more).
- `icons`: favicon.ico (PNG entries), favicon.svg, apple-touch-icon, PWA and
  maskable icons, site.webmanifest and the `<head>` tags from one SVG.
- `studio` skill with design rules against the "AI look", and references for
  logos and social images.
- Commands: `/studio-brand`, `/studio-logo`, `/studio-image`, `/studio-icons`.
