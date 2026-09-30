# Logos

A logo is judged on detail, so it gets more care than any other image. Use this whole
process; don't skip the critique.

## 1. Brief (one message at most)

The name, what it does and for whom, and 2-3 feel words. **Colours and fonts come from
the project first:** a brand kit (`studio.py brand`), else the app's theme (Tailwind
`@theme`, CSS variables, `tailwind.config`, an existing favicon or logo). Never invent a
palette that fights the product's UI. If there's nothing, ask or propose one and say so.

## 2. Ideas before drawing

Write 6-8 one-line ideas that tie to something true about the business: what it sells,
where, its customers, a detail of how it works (like its product tags). Keep the 4 most
distinct: usually **one wordmark, one lettermark, one symbol from the business, one
emblem or badge**. Skip clichés for the category unless you give them a fresh twist.

## 3. Construction rules (why logos look amateur, and how not to)

- **Build from geometry, not freehand curves.** Use circles, rectangles, rounded
  rectangles, arcs (`A` commands with equal radii), straight lines, `stroke-linecap` and
  `stroke-linejoin` round. Don't hand-plot Bézier blobs (`C`/`Q` with guessed control
  points): they come out lumpy. If a curve is needed, make it a true arc or a circle
  segment.
- **A grid:** `viewBox="0 0 96 96"`, key points on multiples of 4 or 8, and a 6-8 unit
  margin all round. Wordmarks: a wide box such as `0 0 400 120`.
- **One stroke weight** across a monoline mark (e.g. 8 units at 96); filled marks use
  consistent gaps (≥ 6 units) so they survive at 32 px.
- **Symmetry by construction:** draw half and mirror it with
  `<use href="#half" transform="translate(96 0) scale(-1 1)"/>` rather than guessing
  mirrored coordinates.
- **Nothing floats and nothing is cropped.** Every accent (dot, diamond, string, leaf)
  touches or aligns with something: centred on a stem, tangent to a curve, on the
  baseline. No shape cut off flat by the frame.
- **Wordmarks are HTML text, not SVG path guesses.** Set the name in a real Google
  Font with tuned letter-spacing, and add at most one custom detail. Position the detail
  against the glyph with CSS, e.g. a dotless `ı` in an inline-block with the new dot
  absolutely centred above it, never with guessed coordinates.
- 1-2 colours per mark, plus the neutral. No gradients, shadows or filters.

## 4. The concept board, made to be judged

- `studio/logo/board.html` at 1600x1000, rendered at the default 2x. Each concept gets
  a large cell (the mark ≥ 240 px) on the light and dark brand backgrounds, and **a
  small-size row** showing it at 64, 32 and 16 px. Under each: its number, name and the
  idea in one plain sentence (no dashes, no jargon).
- Also render each concept alone: `render concept-N.svg concept-N.png --size 512x512`.

## 5. Critique before showing (mandatory)

Look at each `concept-N.png` (512 px, not the tiny board check copy) and use
`studio.py zoom` on the small-size row. Score each concept from 1 to 5 on:

1. **Reads at 32 px**, still recognisable
2. **Craft:** even strokes, true curves, balanced weight, optical centre, nothing floating
3. **Meaning:** a real tie to the business, not a generic shape
4. **Distinct** from the other three and from category clichés
5. **Fits** the product's colours and feel

Any concept scoring under 4 on anything gets redrawn (up to 2 rounds). Only then
show the board. If you can't get a concept to 4, drop it and show 3.

## 6. Show it properly

Give the paths to `board.png` and the 4 `concept-N.png` files, and open the board for
the user (`open` on macOS, `start ""` on Windows, `xdg-open` on Linux). Say one line per
concept and which one you'd pick and why.

## 7. Final set (`studio/logo/final/`) after the user picks

- Refine the chosen one: spacing, optical balance, then re-run the critique.
- `mark.svg`, `mark-mono-black.svg`, `mark-mono-white.svg`
- `lockup.html` (mark + wordmark, horizontal, and stacked if useful), rendered to
  `lockup.png` and `lockup-dark.png` on transparent
- `mark-1024.png`: `render mark.svg mark-1024.png --size 1024x1024 --scale 1`
- Icons: `/studio-icons studio/logo/final/mark.svg`
- Offer to add the mark and colours to `studio/brand.json`.
