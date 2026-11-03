---
name: canvas-ui
description: Use DavidHDev Canvas UI to add creative WebGL, canvas, fluid, glass, particle, shader, and 3D effects over live HTML in React, Solid, Preact, Vue, Svelte, or vanilla projects. Trigger when users mention Canvas UI, canvasui.dev, @canvas-ui registry items, html-in-canvas, or ask to install, select, customize, debug, or validate a Canvas UI component.
---

# Canvas UI

Use the official Canvas UI registry and current component documentation as the source of truth. Do not copy component source into this skill or redistribute the component library.

## Start with the project

1. Inspect the framework, package manager, build tool, existing `components.json`, rendering model, and browser targets.
2. Read `references/upstream-llms.txt` to shortlist a component and framework suffix.
3. When network access is available, check the current registry index and the chosen component's documentation because names, props, dependencies, and browser support may change:

   ```text
   https://canvasui.dev/r/registry.json
   https://canvasui.dev/docs/components/<component>
   ```

4. Pick one effect that supports the content hierarchy. Avoid stacking multiple heavy full-page effects unless the brief explicitly requires it.

## Install from the official registry

Initialize shadcn only if the project does not already use it and installation is within scope:

```text
npx shadcn@latest init
```

Resolve the exact registry item from current docs, then add it:

```text
npx shadcn@latest add @canvas-ui/<component>-<target>
```

Supported target families in the bundled snapshot are React, Solid, Preact, Vue, Svelte, and vanilla. The source should land in the target application, typically under `components/canvasui/`, where the user can edit it.

Never vendor Canvas UI component source into a reusable library, marketplace, bundle, or this skill collection. Its MIT + Commons Clause permits use in applications and products but prohibits selling, sublicensing, or redistributing the components themselves.

## Integrate safely

- Read the installed source and component docs before changing props or engine behavior.
- Keep the underlying HTML interactive, selectable, keyboard reachable, and semantically correct.
- Ensure the effect layer does not intercept pointer events or hide focus indicators unexpectedly.
- Preserve a usable non-WebGL experience and respect `prefers-reduced-motion`.
- Limit device-pixel ratio, simulation resolution, particle counts, and animation work when performance requires it.
- Pause or reduce rendering when offscreen or when the page is hidden if the installed component does not already do so.
- Avoid applying expensive effects to large DOM subtrees without measuring frame time and memory.

## Browser behavior

Treat the experimental HTML-in-canvas path and its fallback as separate test cases:

- Full HTML-in-canvas effects require supported Chrome/Edge behavior, currently involving the `canvas-draw-element` flag or an origin trial.
- Other browsers receive a WebGL overlay fallback for affected components.
- Object/3D effect components may have different support and asset requirements; verify the selected component's current page.

Do not claim full cross-browser visual parity when only the fallback was tested.

## Validate

Run the project's typecheck, relevant tests, and production build. In a real browser, verify:

- intended effect in a supported Chromium configuration;
- fallback in at least one non-supporting configuration;
- keyboard navigation, pointer interaction, text selection, and focus visibility;
- responsive layout and high-DPI behavior;
- reduced motion and acceptable performance on a mid-range device.

Report the registry item, target framework, commands run, browser modes tested, and any unverified origin-trial behavior.

## Reference

`references/upstream-llms.txt` is an official snapshot of Canvas UI's agent-facing index. Prefer current official docs when it conflicts with the snapshot.
