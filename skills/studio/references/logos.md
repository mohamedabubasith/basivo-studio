# Logos

## Explore, then refine

1. Ask (or take from the brand kit) three things: the name, what it does, and 2-3 words
   for how it should feel. Don't ask more.
2. Make **4 distinct directions**, not 4 variations: e.g. a lettermark, an abstract mark
   built from one idea in the product, a wordmark with one custom detail, an emblem.
   One SVG each: `studio/logo/concept-1.svg` …
3. Put them on one comparison board (`board.html`, 1600x900, a 2x2 grid, each concept
   on light and dark, name underneath) and render it with `--check`. Show the board and
   say in one line what idea each one carries.
4. The user picks one. Refine it: spacing, optical balance, stroke weights, then make
   the final set.

## Construction

- `viewBox="0 0 64 64"` (marks) or a wide box for wordmarks; integer coordinates; a
  few simple paths. No filters, no gradients unless the brand needs one, no embedded
  bitmaps.
- **Test small.** A mark must still read at 16 px: render it at 32x32 and look.
  Thin details and small counters die first.
- **Works in one colour.** Every mark must hold up in solid black and solid white.
- Wordmarks use a real font through a Google Fonts `<link>` when rendered to PNG. For a
  portable SVG, keep the mark as paths and say that the wordmark text uses the font
  name (it needs that font installed to look the same outside the browser).
- Optical fixes: round shapes overshoot the baseline slightly; a visually centred mark
  sits a touch above the mathematical centre.

## Final set (`studio/logo/final/`)

- `mark.svg`, `mark-mono-black.svg`, `mark-mono-white.svg`
- `lockup.svg` (mark + name, horizontal) and a stacked version if it helps
- PNG exports: `$S render mark.svg mark-1024.png --size 1024x1024`, and the lockup on
  transparent at `--scale 2`
- Icons and favicons: `/studio-icons studio/logo/final/mark.svg`
- A one-page `usage.html` (clear space, minimum size, colours with hex, do/don't),
  rendered to `usage.png`, only if the user wants a brand sheet.
