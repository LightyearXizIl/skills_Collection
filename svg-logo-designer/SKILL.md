---
name: svg-logo-designer
description: Create original, editable, production-minded SVG logo concepts and logo systems, including marks, wordmarks, lockups, monochrome and reversed variants, accessibility metadata, usage guidance, and validation. Trigger when users ask for a logo, vector brand mark, SVG icon, wordmark, lettermark, monogram, emblem, or scalable logo variations.
---

# SVG Logo Designer

Create original vector work directly as SVG. Do not default to bitmap image generation when the requested deliverable is editable vector code.

## Establish the brief

Determine the minimum information that changes the design:

- brand name and optional initials;
- product/category and audience;
- one to three personality traits;
- required applications and smallest expected size;
- preferred or forbidden colors, symbols, and competitors;
- requested mark type: symbol, wordmark, lettermark, monogram, combination, or emblem.

If a missing choice would materially change the result, ask one focused question. Otherwise state reasonable assumptions and proceed.

## Develop concepts

1. Define the brand idea and the lazy category default to avoid.
2. Produce three distinct directions unless the user requests another count. Each direction must use a different construction logic, not a recolor.
3. Explain each direction in one concise sentence: metaphor, geometry, and intended impression.
4. Check that the concept remains recognizable at favicon size and in one color.
5. Do not imitate, trace, or create a confusingly similar version of a known trademark. State that originality review is not legal trademark clearance.

Prefer presenting a small concept set before generating dozens of variants. After the user selects a direction, refine it and create the requested system.

## Build production-minded SVG

- Use a valid `viewBox` and vector primitives or paths.
- Keep IDs unique and deterministic; prefix IDs when several logos may share a page.
- Avoid scripts, event-handler attributes, `foreignObject`, external URLs, embedded raster images, and unnecessary filters.
- Add `<title>` and `<desc>`, and connect them with `aria-labelledby` when the SVG conveys content.
- Use `aria-hidden="true"` only for a decorative duplicate whose accessible name exists elsewhere.
- Keep shapes simple, path precision reasonable, and visual bounds balanced.
- Test monochrome output; do not rely on gradients to preserve the core silhouette.
- Do not claim a `<text>` wordmark is portable across systems. Name the font and license requirement, or convert approved lettering to real paths with an appropriate vector/font tool.
- Never fabricate Pantone, CMYK, or font-license data. Provide only values actually derived or verified.

## Create variants after selection

Generate only the variants the user needs, typically:

- primary horizontal lockup;
- stacked lockup;
- mark-only/favicon;
- monochrome dark;
- reversed light;
- optional small-size simplified mark.

Keep geometry and spacing consistent across variants. Record the palette, clear-space unit, minimum sizes, background rules, and incorrect-use examples.

## Validate

Run the bundled validator on every SVG:

```text
python scripts/validate_svg.py path/to/logo.svg [more.svg]
python scripts/validate_svg.py --json path/to/logo.svg
```

Then render or open the files and inspect them at small, medium, and large sizes on light and dark backgrounds. Check for clipping, missing fonts, duplicate IDs, malformed paths, low contrast, and inconsistent optical alignment.

## Deliver

Provide editable `.svg` files, a short concept rationale, palette values, font/source notes, variant mapping, and validation results. Clearly separate verified technical facts from design recommendations and legal checks the user must perform.
