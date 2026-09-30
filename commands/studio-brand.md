---
description: Create or update the brand kit (colours, fonts, logo, style) that every basivo-studio image uses.
argument-hint: [brand name]
---

`S='sh "${CLAUDE_PLUGIN_ROOT}/scripts/run" studio.py'`. Run `$S brand` to see the current kit.

Ask in **one** message (skip what `$ARGUMENTS`, the repo's README or an existing logo already answers):
the name, one line on what it does, 2-3 words for the feel, any colours or fonts they already use,
and whether a logo file exists.

Write `studio/brand.json` in this project (or `~/.basivo-studio/brand.json` if they want it for
every project):

```json
{"name": "", "tagline": "",
 "colors": {"primary": "#", "accent": "#", "ink": "#", "paper": "#", "muted": "#"},
 "fonts": {"heading": "Google Fonts family", "body": "Google Fonts family"},
 "logo": {"mark": "studio/logo/final/mark.svg", "lockup": null},
 "style": "calm, editorial, lots of space", "avoid": ["gradients", "stock-photo look"]}
```

Choose accessible colours (ink on paper ≥ 7:1, primary on paper ≥ 4.5:1). Render a one-screen
swatch board (`studio/brand/board.html`, 1600x900: colours with hex, the two fonts at real sizes,
the logo if any) with `$S render … --check`, look at it, and show it. No logo yet? Offer `/studio-logo`.
