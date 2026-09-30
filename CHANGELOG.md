# Changelog

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
