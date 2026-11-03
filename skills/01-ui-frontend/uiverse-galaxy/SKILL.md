---
name: uiverse-galaxy
description: Find, inspect, adapt, and validate MIT-licensed HTML/CSS or Tailwind UI elements from Uiverse Galaxy. Trigger when users mention Uiverse, uiverse-io/galaxy, or ask for a community-made button, card, loader, checkbox, form, input, notification, radio, toggle, tooltip, or CSS/Tailwind micro-component from the Galaxy collection.
---

# Uiverse Galaxy

Use Uiverse or the official Galaxy repository to locate a real component. Preserve its creator attribution and adapt the exact source rather than recreating it from a screenshot or secondary description.

## Find the component

1. Read `references/upstream-readme.md` for the repository model and attribution guidance.
2. Prefer browsing [Uiverse.io](https://uiverse.io/) when visual comparison matters.
3. When using GitHub, search the relevant category directory and record the exact repository path. Filenames encode the original creator and component identifier.
4. Inspect the source before choosing it. Do not assume a visually similar filename has the required states or behavior.

Common repository categories include buttons, cards, checkboxes, forms, inputs, loaders, notifications, patterns, radio buttons, toggle switches, and tooltips. Verify current paths rather than treating this list as exhaustive.

## Adapt to the project

- Preserve semantic HTML and native controls.
- Keep or improve keyboard focus, labels, checked/disabled states, and target size.
- Scope classes, animations, keyframes, and CSS variables to avoid collisions.
- Replace global selectors and page-wide resets with component-local styles.
- Preserve the existing framework and styling approach; convert to Tailwind or component CSS only when requested.
- Keep the original visual identity while adapting tokens, sizing, and content to the host design system.
- Add `prefers-reduced-motion` handling for non-essential animation.
- Remove tracking, remote assets, unsafe inline handlers, or unnecessary dependencies if present.
- Credit the original creator and Uiverse in code comments or project documentation when practical, even though attribution is not mandatory under MIT.

## Validate

Run the project's formatter, typecheck, tests, and build as applicable. Verify in a real browser:

- hover, focus, active, disabled, checked, loading, and error states that apply;
- keyboard use and visible focus;
- responsive behavior and text wrapping;
- contrast and reduced motion;
- no class/keyframe collisions or console errors.

Report the exact Uiverse/Galaxy source path, creator encoded in the filename, changes made, and validation performed.

## Contributing upstream

Do not open direct pull requests to the Galaxy archive. Submit new elements through Uiverse, following the upstream workflow in `references/upstream-readme.md`.
