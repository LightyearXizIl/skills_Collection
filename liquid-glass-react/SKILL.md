---
name: liquid-glass-react
description: Install, implement, customize, troubleshoot, and validate the liquid-glass-react package for Apple-like refraction, frosted glass, chromatic aberration, elasticity, and interactive liquid glass effects in React. Trigger when users mention rdev/liquid-glass-react, the liquid-glass-react npm package, Apple Liquid Glass in React, or its LiquidGlass component and props.
---

# Liquid Glass React

Use the installed package types and current upstream README as the source of truth. The bundled references are a snapshot and may be stale.

## Check the project

1. Confirm the project uses React 18 or later and identify its package manager, rendering model, CSS system, and browser targets.
2. Inspect `package.json` and the lockfile before installing or upgrading.
3. If the package is already installed, read its installed type declarations and version. Do not silently change versions.
4. For an SSR framework, verify whether the installed version can be imported during server rendering. If it accesses browser APIs at import/render time, isolate it using the framework's documented client-only mechanism.

## Install

Use the project's package manager. For npm:

```text
npm install liquid-glass-react
```

Do not pin to the bundled snapshot version unless the user requests reproducibility or the existing lockfile requires it.

## Implement

- Import the default `LiquidGlass` component from `liquid-glass-react`.
- Preserve meaningful children and native interaction semantics.
- Use the installed type declarations to confirm props before editing.
- Use `mouseContainer` with a stable React ref when the effect should respond to a larger pointer region.
- Tune displacement, blur, saturation, aberration, elasticity, radius, and padding against the real background rather than in isolation.
- Treat `mode="shader"` as a quality/stability tradeoff; verify it in the project's browsers instead of assuming it is best.
- Avoid wrapping large application trees or many repeated items without profiling.
- Provide a restrained static/frosted fallback for reduced motion, low-power devices, and partial browser support.

## Accessibility and interaction

- Keep buttons and links as native interactive elements; do not replace semantics with clickable glass containers.
- Preserve focus visibility, keyboard activation, hit targets, labels, and contrast.
- Ensure decorative layers do not capture pointer events or enter the accessibility tree unnecessarily.
- Respect `prefers-reduced-motion` and avoid continuous pointer-driven motion when the user disables it.

## Browser support

The bundled upstream snapshot warns that Safari and Firefox only partially support the effect and do not show displacement. Verify the current package and browsers. Do not claim pixel parity across Chrome, Safari, and Firefox unless each was tested.

## Validate

Run typecheck, relevant tests, and a production build. Test:

- Chrome/Edge full effect;
- Safari and Firefox fallback/partial rendering when in scope;
- hover, click, keyboard focus, and `mouseContainer` behavior;
- light and dark backgrounds;
- mobile layout, reduced motion, performance, and cleanup on unmount.

Report the installed version, props used, browsers tested, commands run, and remaining compatibility gaps.

## References

- `references/upstream-readme.md`: official usage and prop snapshot
- `references/upstream-package.json`: upstream package metadata snapshot

Prefer installed types and current upstream documentation when they disagree with these files.
