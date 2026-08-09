# Examples — Positive Reference Corpus

Seven real pages from a showcase corpus (now 61 pages and growing), each a clean instance of one persona + one hero engine (brand register) or one dashboard morphology (product register). Read them to see the substrate, soul, and engine — or the layout shell, chart-crafting, and reduced-motion rules — applied together in shipped code, not as templates to copy verbatim.

The other pages aren't bundled as files (repo-size reasons — several carry Three.js/WebGL payloads), but every brand-register one is catalogued as a technique note in `../references/inspiration-catalog.md`, grouped by persona. Check there for a second reference point when these don't cover the brief's industry or mood.

## Brand register (persona + hero engine)

| File | Persona | Hero engine | What to study |
|------|---------|-------------|---------------|
| `aether-cinematic-tech.html` | Cinematic Tech | A · Three.js + GLSL | fixed 3D canvas, additive-blend particles, cyan/magenta on near-black, grain + vignette |
| `nova-brutal-typographic.html` | Brutal Typographic | D · GSAP | oversized Anton headline, `mix-blend-mode: difference` nav, bone/black + hot accent, outline+fill type |
| `offscreen-editorial.html` | Editorial Publication | D · GSAP scroll-reveal | light register, Playfair + Spectral, grayscale photography, ruled hairlines, drop-caps |
| `signal-phosphor-terminal.html` | Phosphor Terminal | B · Canvas 2D | single neon-green, real-time K-line canvas, CRT scanlines + flicker, mono-forward type |
| `studio-quiet-luxury.html` | Quiet Luxury Minimal | E · CSS-only | dual-layer mouse mask (no JS lib), Raleway 100–900 weight range, max whitespace, light theme |

## Product register (dashboard morphology)

Pulled from a batch of 10 demo dashboards built to stress-test `../references/product-ui.md` and `../references/chart-crafting.md`. These four cover most of that batch's range (canonical sidebar shell, floating-panel shell, tables, forms, charts, KPI rows) between them — see `../references/inspiration-catalog.md`'s dashboard section for the other 6 as technique notes.

| File | Shell | What to study |
|------|-------|----------------|
| `buildly-ai/index.html` → `buildly-growth-dashboard.html` | Canonical sidebar + topbar (dark) | The default shell from `product-ui.md` §1 in its cleanest form: line+area draw-in chart, donut arc, five KPI number-roll-up counters, native-thumb slider (`chart-crafting.md` §7's simple tier) |
| `stakent-monitoring-dashboard.html` | Canonical sidebar + topbar (dark) | Glowing sparklines (`feGaussianBlur` filter layered on the stroke — a polish detail not in `chart-crafting.md`'s base recipe), the premium custom knob+fill+tag slider (`chart-crafting.md` §7's second tier) |
| `acru-financial-dashboard.html` | Canonical sidebar + topbar (light) | Stacked bar chart with a real hover tooltip positioned relative to the chart container not the viewport (`chart-crafting.md` §4), half-ring gauge (`chart-crafting.md` §3), credit-card-styled widget |
| `pawcare-adaptive-health.html` | Floating rounded panel | Hotspot-annotation pins on a real photo (`product-ui.md` §6), a combined accent-color-picker + dark-mode toggle that keeps the two independent (`theming.md`'s accent-recolor boundary), hand-built ECG waveform and ring/segment bars (`chart-crafting.md` §5) |

**Note:** these are single-file pages. `aether` references `three.module.js`; `nova`/`offscreen`/`buildly`/`stakent`/`acru`/`pawcare` use GSAP; in the original showcase those libs and `assets/*.jpg` avatars/photos live in sibling `_lib/`/`assets/` folders. Here the files are kept as **read-only reference** for structure and craft, not as standalone-runnable demos. Lift patterns, not whole files — each new brief deserves its own soul.
