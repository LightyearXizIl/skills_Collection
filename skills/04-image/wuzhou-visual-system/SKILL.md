---
name: wuzhou-visual-system
description: "Design and review a consistent Wu Zhou dynasty visual system and produce copy-ready English Midjourney prompts. Use for 武周视觉系统、武则天各人生阶段、登基妆造、黑金帝服、神都洛阳宫殿、科举武举、农桑水利、丝路边关、女子群像、百官朝拜、画面资产和构图连续性. This skill governs static visual assets; use the universal 30-second image-to-video skill for motion timelines."
---

# 武周视觉系统

Create historically grounded, cinematically unified Wu Zhou images while honoring the user's established art direction.

## Route the task

- Read [references/visual-bible.md](references/visual-bible.md) for characters, makeup, clothing, architecture, palette, light, and material continuity.
- Read [references/scene-guides.md](references/scene-guides.md) when building coronation, examination, agriculture, border, crowd, aerial, or life-stage scenes.
- Read [references/prompt-contract.md](references/prompt-contract.md) whenever writing or revising a Midjourney prompt.
- For image-to-video motion, timing, dialogue, camera movement, sound nodes, or a fixed 30-second sequence, hand the approved still-image assets to `$universal-30s-image-to-video`; do not invent a second motion system here.

## Follow this priority

1. Treat the current user instruction and visible reference image as the source of truth.
2. Preserve the requested shot size, subject position, action, and image structure.
3. Apply Wu Zhou identity through life stage, makeup, clothing, architecture, props, and social hierarchy.
4. Apply the Oriental Ancient Style contribution only to color, light, skin, and material rendering when the user explicitly requests it. Do not let it invent cast size, story action, or scene structure.
5. Prefer readable visual storytelling over decorative excess.

## Work method

1. Identify the exact asset type: character, location, prop, crowd, policy achievement, or transition plate.
2. Lock the life stage and status before describing appearance or costume.
3. Put shot type, subject, and main action at the beginning of the prompt.
4. Use one dominant action and a simple foreground-midground-background hierarchy.
5. Add only historically useful environment details.
6. Finish with the shared light, palette, material, lens, and realism language.
7. Add concise negatives that block modern, fantasy, Ming-Qing, CGI, text, and anatomy failures as appropriate.

## Revision discipline

- When the user says “只改服饰/妆容/构图/背景,” change only that fragment and keep every other clause and its order unchanged.
- When the user asks for the complete version after a targeted change, return the full prompt with that single change merged in.
- Do not silently turn a close-up into a wide shot, add ministers behind a throne close-up, add a random bell, create extra characters, or insert props that were not requested.
- If the visible reference contradicts a previous generic rule, follow the visible reference and current correction.

## Output modes

### Midjourney asset

Return a Chinese title followed by one English copy-ready MJ prompt. Keep all generation instructions inside the English prompt. Never append Chinese operational text such as “调用SKILL.”

### Visual review

State the mismatch first, then give the smallest correction needed. Separate historical issues from optional art-direction choices.

### Visual framework

For a multi-image project, provide a numbered asset list with shot size, subject/action, story function, and continuity anchor. Do not assign video duration unless asked.

