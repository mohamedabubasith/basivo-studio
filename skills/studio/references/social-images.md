# Covers, social images, thumbnails, cards, carousels, diagrams

Pick the preset from `studio.py sizes`. One file per image; for a set (carousel,
several platforms) share one `style` block so they match.

## Layout patterns that don't look templated

- **Editorial:** big headline left-aligned in the top two-thirds, a small kicker above
  it (category or series name), the brand mark small in a corner. Plain background.
- **Object + type:** one strong visual on one side (a simple illustration built from
  shapes, a real screenshot in a device-free frame, a chart), headline on the other.
- **Big number / big word:** one number or word at 300-500 px, one line explaining it.
- **Split colour:** two blocks of brand colour, headline across the edge.
- **Quote card:** the quote at 56-72 px with real quotation marks (“ ”), the name and
  role small underneath, lots of margin.

Vary the pattern across a series; don't repeat centred-headline-on-gradient.

## Per job

- **Blog / Medium cover:** calm, readable as a thumbnail, headline optional (the
  platform shows the title). A cover shouldn't shout.
- **Open Graph (1200x630):** title ≤ 60 characters, site name or logo, readable at
  600 px wide in a chat preview.
- **YouTube thumbnail (1280x720):** 3-5 words max, huge, high contrast, one focal point;
  keep the bottom-right corner clear.
- **Carousel (1080x1350 each):** slide 1 is the hook, one point per slide, a consistent
  frame and page number, the last slide says what to do next. Render each slide, then a
  quick contact sheet (an HTML page with the slides side by side) to check them together.
- **Banner (X 1500x500, LinkedIn 1584x396):** mobile crops the sides and the profile
  photo covers the bottom-left, so keep content centre-right.
- **Diagram:** boxes and arrows in SVG inside the HTML, 3-7 nodes, labels in plain
  words, one accent colour for the path that matters. Left-to-right or top-to-bottom,
  never both.

## Using the user's images

Photos, screenshots or product shots the user gives you go in with relative paths or
`object-fit: cover`; add a flat colour panel for text rather than text over a busy
photo. Only use images the user provided or that they confirm they may use.

## After rendering

Look at the check copy at the size people will see it (a feed thumbnail is ~500 px
wide): can you read the headline in one second? Is anything cut off or touching the edge?
