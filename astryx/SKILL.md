---
name: astryx
description: Use Meta's Astryx design system to build accessible React interfaces with @astryxdesign/core, themes, templates, and the Astryx CLI. Trigger when users ask to install or use Astryx, build React 19+ UI with Astryx components, inspect component APIs, create or extend Astryx themes, use templates, swizzle components, run Astryx upgrades, or contribute components and documentation to facebook/astryx.
---

# Astryx

Use Astryx's installed CLI and structured documentation as the source of truth. Do not guess component names, props, variants, tokens, or template APIs from memory.

## Establish the context

1. Inspect the repository, package manager, React version, and existing Astryx dependencies.
2. Distinguish between:
   - a consumer application using published `@astryxdesign/*` packages;
   - the upstream `facebook/astryx` monorepo.
3. For upstream repository work, read `references/upstream-project-guide.md` before editing.
4. Preserve the project's existing package manager and conventions.

## Set up a consumer application

Require React 19 or later. When installation is in scope, add:

```text
dependencies: @astryxdesign/core @astryxdesign/theme-neutral @stylexjs/stylex
devDependency: @astryxdesign/cli
```

Use the project's package manager. For reliable CLI access, add this script if the project does not already provide one:

```json
{
  "scripts": {
    "astryx": "node node_modules/@astryxdesign/cli/clients/cli/bin/astryx.mjs"
  }
}
```

Do not pin versions unless the user or existing lockfile requires it.

## Bootstrap the CLI before coding

Run the equivalent package script commands from the project root:

```text
astryx help
astryx docs
astryx docs principles --dense
astryx docs tokens --dense
astryx docs theme --dense
astryx component --list
astryx template --list
```

Adapt invocation to the package manager, for example `npm run astryx -- <args>` or the corresponding pnpm/yarn script form.

If the CLI is unavailable and installation is outside the request, state that component details are unverified and use the official Astryx documentation rather than inventing an API.

## Build with Astryx

1. Query every component before first use:

   ```text
   astryx component <Name> --dense
   ```

2. Prefer existing Astryx components and templates over rebuilding primitives.
3. Query a full template or its annotated skeleton when the request matches an available page pattern:

   ```text
   astryx template <name>
   astryx template <name> --skeleton
   ```

4. Use documented tokens, theming, accessibility behavior, and composition patterns.
5. Preserve native semantics, keyboard behavior, visible focus, labels, and reduced-motion behavior.
6. Use `className` with the consumer's existing CSS approach when customization is sufficient. Use `swizzle` only when the user needs ownership of component source:

   ```text
   astryx swizzle <Name>
   ```

7. After upgrading `@astryxdesign/core`, run the documented migration command:

   ```text
   astryx upgrade --apply
   ```

## Author upstream components and themes

- To create a component in `facebook/astryx`, read `references/create-component.md`, then follow the current wiki lifecycle and inspect sibling components.
- To create or extend a theme package, read `references/create-theme.md`.
- To write `{Name}.doc.mjs`, read `references/writing-component-docs.md`.
- To add `docsDense`, also read `references/dense-compression-protocol.md`; preserve counts, signal words, required markers, full component names, and cross-component references.
- Treat the branch-local CLI output and wiki as newer than the bundled snapshot when they disagree.

## Validate

Run validation proportional to the change:

- consumer app: typecheck, relevant tests, production build, and focused UI/accessibility checks;
- upstream monorepo: the component or package tests first, then the repository-prescribed build, test, and lint commands;
- theme work: verify light and dark modes and component override scope;
- documentation work: confirm CLI discovery and rendered output for full, compact, translated, or dense modes as applicable.

Report commands actually run and any remaining validation gap.

## Bundled official references

The files in `references/` are snapshots from `facebook/astryx`:

- `upstream-project-guide.md`: upstream repository and StyleX/CLI conventions
- `create-component.md`: component lifecycle quick reference
- `create-theme.md`: `defineTheme` package workflow
- `writing-component-docs.md`: structured component documentation
- `dense-compression-protocol.md`: loss-aware dense translation rules

Prefer current CLI output and official online documentation for drift-prone details.
