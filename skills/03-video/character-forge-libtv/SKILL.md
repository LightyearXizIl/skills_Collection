---
name: character-forge-libtv
description: Convert a rough character direction into 3-4 differentiated candidates, then create a clean picture-node-only LibTV canvas with Image2 full-body master variants and downstream image nodes that are visibly connected to the chosen/default master node. Default image quality is standard quality + 2K to save credits. Expression sheets must use 3:4 portrait framing with larger face occupancy.
metadata:
  version: 1.4-expression-portrait
---

# Character Forge LibTV Skill

## Purpose

Use this skill when the user wants to create a reusable AI character from a rough text direction and wants LibTV to hold the actual image-generation workflow.

The goal is a clean, usable LibTV canvas, not a documentation board.

Default workflow:

1. Convert the user's rough direction into 3-4 differentiated character candidates in chat only.
2. Wait for the user to choose one candidate.
3. Create a clean LibTV canvas containing image generation nodes only.
4. Create 2-4 Image2 9:16 full-body master variants and run only these first.
5. Prebuild downstream Image2 nodes, do not run them yet:
   - face portrait close-up
   - 3x3 expression sheet
   - turnaround / character board
6. IMPORTANT: downstream nodes must have real visible canvas connections from the current default/selected full-body master node. Do not rely only on prompt text references.
7. Return the LibTV canvas/project link and a short node/connection summary. Do not paste generated images back into chat unless the user explicitly asks.

## v1.3 Credit-Saving Default

All Image2 image nodes must default to:

- **Quality:** standard quality / 标准画质
- **Resolution / clarity:** 2K

Do **not** use high quality / 高画质 by default because the user said high quality costs too many credits.

Only use high quality if the user explicitly says one of these:

- 高画质
- 最终精修
- 最终成品图
- final high quality
- final polished version

This default applies to all core image nodes:

- `10_IMAGE2_9x16_FULL_BODY_MASTER_01`
- `11_IMAGE2_9x16_FULL_BODY_MASTER_02`
- optional `12/13_IMAGE2_9x16_FULL_BODY_MASTER_03/04`
- `20_IMAGE2_FACE_PORTRAIT_CLOSEUP`
- `21_IMAGE2_3x3_EXPRESSION_SHEET`
- `22_IMAGE2_TURNAROUND_CHARACTER_BOARD`

## v1.4 Framing Update

Additional hard requirements:

- `20_IMAGE2_FACE_PORTRAIT_CLOSEUP` must use a portrait ratio and a much larger face crop than before. Prefer **3:4** portrait by default; **4:5** is acceptable only if 3:4 is unavailable in the installed CLI. The face should dominate the frame, typically head-and-shoulders or chest-up, with minimal empty space.
- `21_IMAGE2_3x3_EXPRESSION_SHEET` must use **3:4 portrait ratio** rather than square. The output should still contain a 3x3 grid, but each cell must be a close-up portrait with the face occupying a large portion of each panel, similar to a clean ID-photo/expression-reference layout. Avoid tiny heads or excessive torso space.
- For the expression sheet, keep a clean light background and consistent framing across all 9 panels so expression differences are easy to compare.

If the local LibTV CLI exposes quality flags, set them explicitly to standard quality and 2K. If flags are named differently, inspect local help and choose the option matching the UI's “标准画质 + 2K”. If the CLI does not expose image quality flags, state that the installed CLI did not expose a configurable quality parameter instead of pretending it was set.

## Critical User Preferences

These are hard requirements unless the user explicitly overrides them:

- Candidate mode first.
  - Output 3-4 role candidates in chat.
  - Do not create the LibTV canvas until the user chooses a candidate.
- Canvas must be picture-node-only.
  - Do not create large text nodes.
  - Do not create character card text nodes.
  - Do not create prompt-copy text nodes.
  - Do not create delivery/next-step text nodes.
  - Do not create documentation-heavy groups.
- Canvas layout must be clean.
  - Do not stack nodes on top of each other.
  - Do not use overlapping group frames.
  - Use explicit positions if the CLI supports node coordinates.
  - Use large spacing even if it looks sparse.
- Canvas dependency lines are mandatory.
  - Face portrait, 3x3 expression sheet, and turnaround board must be visibly connected to the current master node.
  - A prompt string like `{{Node "10_IMAGE2_9x16_FULL_BODY_MASTER_01"}}` is not enough by itself.
  - Create real LibTV edges/dependencies/media-reference connections using the installed CLI's supported command.
- Image defaults:
  - Model: image2.
  - Quality: standard quality / 标准画质.
  - Resolution: 2K.
  - Never choose high quality unless the user explicitly asks for final high quality output.
  - `20_IMAGE2_FACE_PORTRAIT_CLOSEUP`: default ratio **3:4**, face-dominant close-up.
  - `21_IMAGE2_3x3_EXPRESSION_SHEET`: default ratio **3:4**, 3x3 layout, close-up portraits with larger face occupancy.
  - `22_IMAGE2_TURNAROUND_CHARACTER_BOARD`: wide landscape ratio as supported.
- Full-body master images:
  - Default 2 variants.
  - Use 4 variants only when the user asks for more options.
  - Model: image2.
  - Aspect ratio: 9:16.
  - Quality: standard quality / 标准画质.
  - Resolution: 2K.
  - Run these first.
- Downstream nodes:
  - Create them in the canvas, but do not run them by default.
  - Default-create real edges from `10_IMAGE2_9x16_FULL_BODY_MASTER_01` to all downstream nodes so the canvas visually shows the workflow.
  - If the user later chooses 02/03/04, replace the downstream edges and prompt references so all downstream nodes point only to the chosen master.
- Final chat response after creating/running the canvas:
  - Return only the LibTV canvas/project link, run status, downstream connection status, and which node needs user confirmation.
  - Do not embed or repost generated images in chat.
  - Do not dump long prompts unless the user asks.

## Safety and Credential Rules

- Never read, print, modify, or ask for access keys, API keys, tokens, cookies, browser cookies, or secrets.
- Do not ask the user for a LibTV access key. Use browser login if LibTV CLI requires login.
- If login is required, ask the user to complete the browser login flow.
- Never rerun expensive generation nodes without a clear reason.
- If a node fails, diagnose the specific failed node instead of rebuilding the whole canvas.

## Before Using LibTV CLI

The exact CLI schema may vary. Before creating a real project, inspect local CLI commands:

```bash
libtv --help
libtv project --help
libtv node --help
libtv canvas --help || true
libtv edge --help || true
libtv connect --help || true
libtv node connect --help || true
libtv workspace --help || true
```

Use only supported commands/flags shown by the installed LibTV CLI. Do not invent unsupported flags.

Parameter discovery rule:

- Search local help for model, ratio, quality, resolution, clarity, size, image quality, 画质, 清晰度, 2K, standard, 标准画质.
- If available, set Image2 nodes to standard quality + 2K.
- Do not accidentally set high quality. Do not use any flag that maps to 高画质 unless the user explicitly asks.

Connection rule:

- First look for a real command that creates canvas edges or media-reference dependencies, for example commands containing `edge`, `connect`, `link`, `dependency`, `reference`, `source`, or similar.
- If the CLI supports connecting nodes, use that real command after node creation.
- If the CLI supports node prompt references but not visible edges, explicitly tell the user that the installed CLI cannot create visible lines with the available commands. Do not pretend the nodes are connected.
- Never treat prompt-only `{{Node ...}}` as sufficient when the user expects visible canvas lines.

If the CLI supports `x`, `y`, `position`, `width`, `height`, or layout parameters, use them. If it does not support coordinates, create nodes one by one in a simple order and then use any available auto-layout/arrange command if present.

## Stage 1: Candidate Role Generation, Chat Only

When the user gives a rough role direction, first output 3-4 differentiated candidates in chat only.

Do not create a LibTV canvas yet.

Each candidate should include:

- Candidate label: A/B/C/D
- Role name
- Use case fit
- Age impression: adult / young adult unless the user asks otherwise
- Regional / visual impression if requested
- Three recognition points
- Face shape
- Eye shape
- Nose shape
- Mouth shape
- Hair / makeup
- Skin texture
- Temperament / emotional base
- Identity / story background
- Hard negative constraints
- Why this candidate is different from the others

Keep candidates clearly different. Avoid four versions of the same AI template face.

After listing candidates, ask the user to choose one.

## Stage 2: Selected Character DNA, Internal Prompt Source

After the user chooses a candidate, create the final character DNA internally and use it to fill the image prompts.

Do not create a text node for this DNA in LibTV.

The final character DNA should contain:

- Role name
- Use case
- Age impression
- Regional / visual impression
- Three recognition points
- Face shape
- Eye shape
- Nose shape
- Mouth shape
- Bone structure
- Hair / makeup
- Skin texture
- Personality / emotional base
- Identity / story background
- Clothing / styling direction
- Hard negative constraints

Use only 3 strong recognition points. Do not stuff prompts with too many random facial defects.

## Reference Image Strategy

If the user provides reference images, assign a clear role to each image in the prompt. Never blindly average all faces.

Possible roles:

- `REF_FACE_MAIN`: main face structure, face shape, eye shape, age impression, regional look.
- `REF_FACE_AUX`: auxiliary skin texture, slight bone clarity, portrait cleanliness.
- `REF_EXPRESSION`: expression and emotional state.
- `REF_HAIR_MAKEUP`: hair, makeup, grooming.
- `REF_OUTFIT`: clothing structure and styling.
- `REF_LIGHTING_STYLE`: color, lighting, camera style.

Prompt rule:

```text
Main face reference controls face structure. Auxiliary references only contribute their assigned traits. Do not average multiple faces. Do not create an indistinct mixed face unless the user explicitly asks for that.
```

If the user wants a more East Asian result, use:

```text
The final character should be clearly perceived as East Asian. Use the East Asian reference as the main face structure. Use the non-East-Asian reference only for auxiliary skin texture, slight bone clarity, and portrait cleanliness. Do not generate blonde hair, blue eyes, or an obviously Western face.
```

## Downstream Node Prompt Requirements

### 20_IMAGE2_FACE_PORTRAIT_CLOSEUP
Prompt must explicitly say:

- keep the same character identity as the selected master node
- create a **close-up portrait**
- use **3:4 portrait ratio** when possible
- face should occupy a large portion of the frame
- framing should be head-and-shoulders or chest-up with minimal background

### 21_IMAGE2_3x3_EXPRESSION_SHEET
Prompt must explicitly say:

- create a **3x3 expression sheet**
- use **3:4 portrait ratio**
- each of the 9 panels should be a **close-up portrait** with the face occupying most of the panel
- use consistent framing, neutral clean background, and even lighting
- avoid tiny heads, excessive torso area, or wide empty margins

Suggested 9 expressions:

1. neutral
2. soft smile
3. stern / serious
4. sad / disappointed
5. happy smile
6. crying / about to cry
7. surprised
8. angry / frowning
9. concerned / confused

### 22_IMAGE2_TURNAROUND_CHARACTER_BOARD
Prompt should keep the existing structure: left full-body turnaround views, right multi-angle half-body portraits.

## Canvas: Picture Nodes Only

Create only image generation nodes on the LibTV canvas.

Do not create these unless the user asks:

- no `00_INPUT` text node
- no `CHARACTER_DNA` text node
- no `NEGATIVE_RULES` text node
- no `DELIVERY` text node
- no large prompt text node
- no heavy group cards that overlap the picture nodes

If the CLI requires groups/frames, use group labels only and make them large enough to avoid overlap. Prefer no groups if possible.

## Clean Layout Requirements

Use a simple left-to-right layout with large gaps.

Recommended coordinate map if the CLI supports positions:

```text
Column A: Full-body master generation
10_IMAGE2_9x16_FULL_BODY_MASTER_01   x=0      y=0
11_IMAGE2_9x16_FULL_BODY_MASTER_02   x=0      y=1100
12_IMAGE2_9x16_FULL_BODY_MASTER_03   x=0      y=2200   optional
13_IMAGE2_9x16_FULL_BODY_MASTER_04   x=0      y=3300   optional

Column B: Confirmed-character downstream nodes
20_IMAGE2_FACE_PORTRAIT_CLOSEUP      x=1700   y=0
21_IMAGE2_3x3_EXPRESSION_SHEET       x=1700   y=1100
22_IMAGE2_TURNAROUND_CHARACTER_BOARD x=1700   y=2200
```

Minimum layout spacing:

- horizontal gap between columns: 1200-1700 px
- vertical gap between nodes: 900-1200 px
- no two node rectangles should overlap
- do not place a text card on top of an image node
- do not place downstream nodes behind master nodes

After creation, if LibTV CLI has a layout/arrange command, run it or verify that nodes are not overlapping.

## Required Image Nodes

All required image nodes must use:

- Model: `image2` / `Lib Image` if that is the installed LibTV display name for Image2
- Quality: standard quality / 标准画质
- Resolution: 2K

Do not set high quality.

### `10_IMAGE2_9x16_FULL_BODY_MASTER_01`

Purpose: full-body master candidate 01.

- Model: `image2`
- Aspect ratio: `9:16`
- Quality: standard quality / 标准画质
- Resolution: 2K
- Run immediately.

Prompt template:

```text
Create a full-body character master image for the selected role.

Character DNA:
{SELECTED_CHARACTER_DNA}

Image requirements:
Full-body standing portrait, head-to-toe visible, 9:16 vertical composition, clear face, clear outfit, natural full-body proportion, cinematic but clean character presentation. The whole figure must be visible, not cropped. Simple readable background or scene background matching the use case. Realistic photography / cinematic character still. Keep the character adult or young adult. Preserve the selected facial recognition points and temperament.

Negative constraints:
{NEGATIVE_RULES}
Avoid AI template face, over-smoothed plastic skin, exaggerated beauty filter, random face change, cropped feet, cropped head, distorted hands, wrong costume era, childish appearance, underage impression.
```

### `11_IMAGE2_9x16_FULL_BODY_MASTER_02`

Same role DNA, but use a meaningfully different pose/composition/styling intensity while keeping the same character identity.

- Model: `image2`
- Aspect ratio: `9:16`
- Quality: standard quality / 标准画质
- Resolution: 2K
- Run immediately.

Prompt should include:

```text
Alternative full-body master variant 02 of the same selected character. Keep the same identity, face DNA, age impression, hair, temperament, and costume direction. Change only pose, micro-expression, framing, and background rhythm enough to provide a useful selection option.
```

### Optional `12/13_IMAGE2_9x16_FULL_BODY_MASTER_03/04`

Only create/run these when the user wants 4 variants or more selection.

Use the same Image2 standard quality + 2K default.

### `20_IMAGE2_FACE_PORTRAIT_CLOSEUP`

Purpose: close-up face portrait for checking facial details.

- Model: `image2`
- Aspect ratio: use `3:4`, `4:5`, or platform-supported portrait ratio. If only fixed ratios are available, choose a portrait ratio.
- Quality: standard quality / 标准画质
- Resolution: 2K
- Do not run until the user confirms the master image.
- Must have a real visible edge from the chosen/default full-body master.
- Prompt should also include the node reference to the same chosen/default master.

Prompt template:

```text
Use {{Node "CHOSEN_FULL_BODY_MASTER_NODE"}} as the only character identity reference.
Keep the same person, same facial structure, same age impression, same hair, same temperament, and same overall identity.

Create a close-up face portrait, chest-up or head-and-shoulders framing, neutral clean background or subtle matching scene atmosphere. Emphasize real skin texture, natural pores, subtle skin tone variation, nose wing shadow, natural eye detail, believable makeup, and non-plastic realism. The face must remain consistent with the chosen full-body master image.

Negative constraints:
Do not change the face. Do not beautify into an AI template face. Do not make the person look younger. Do not add modern influencer styling unless requested. Do not create blonde hair, blue eyes, Westernized face, heavy filter, over-smooth skin, or doll-like features.
```

### `21_IMAGE2_3x3_EXPRESSION_SHEET`

Purpose: 9-expression reference sheet for expression consistency.

- Model: `image2`
- Aspect ratio: square or 4:3 if supported.
- Quality: standard quality / 标准画质
- Resolution: 2K
- Do not run until the user confirms the master image.
- Must have a real visible edge from the chosen/default full-body master.
- Prompt should also include the node reference to the same chosen/default master.

Default fixed 9 expressions:

1. calm neutral
2. slight smile
3. serious
4. sad
5. surprised
6. angry
7. confused
8. wronged / restrained grievance
9. thoughtful / inward-looking

Prompt template:

```text
Use {{Node "CHOSEN_FULL_BODY_MASTER_NODE"}} as the only character identity reference.
Create a 3x3 expression reference sheet of the same character. Keep the same face structure, same hair, same age impression, same identity, same skin texture, and same costume/styling direction across all 9 panels.

3x3 grid expressions, left to right, top to bottom:
1 calm neutral, 2 slight smile, 3 serious,
4 sad, 5 surprised, 6 angry,
7 confused, 8 restrained grievance, 9 thoughtful inward-looking.

Clean consistent lighting, same camera distance for all panels, no text labels if the platform struggles with text, white or simple neutral background. The face must not drift across panels.

Negative constraints:
No identity drift, no different person, no exaggerated cartoon expressions, no AI beauty template, no plastic skin, no underage look, no changed hairstyle.
```

### `22_IMAGE2_TURNAROUND_CHARACTER_BOARD`

Purpose: fixed character board.

- Model: `image2`
- Aspect ratio: landscape such as `16:9`, or the closest supported wide ratio.
- Quality: standard quality / 标准画质
- Resolution: 2K
- Do not run until the user confirms the master image.
- Must have a real visible edge from the chosen/default full-body master.
- Prompt should also include the node reference to the same chosen/default master.

Fixed layout:

- Left side: full-body turnaround, front / side / back.
- Right side: multi-angle half-body portraits, front / 45-degree / side / 3/4 auxiliary angle.

Prompt template:

```text
Use {{Node "CHOSEN_FULL_BODY_MASTER_NODE"}} as the only character identity reference.
Create a clean character turnaround board for the same character.

Layout:
Left side: full-body turnaround views: front view, side view, back view. Head-to-toe visible.
Right side: multi-angle half-body portraits: front face, 45-degree face, side face, 3/4 auxiliary angle.
Keep the same person, same face DNA, same hair, same costume, same age impression, same body proportion, same temperament across all views.

Clean studio/white background or simple neutral background. Character design reference sheet style, readable structure, no clutter.

Negative constraints:
No identity drift, no different face in each view, no changed costume, no cropped full-body views, no deformed profile, no over-beautified AI template face.
```

## Real Edge / Dependency Rules

Downstream nodes must be connected with real canvas edges, not only prompt references.

### After creating the nodes, perform this default connection set

Create visible/real dependencies:

```text
10_IMAGE2_9x16_FULL_BODY_MASTER_01  -> 20_IMAGE2_FACE_PORTRAIT_CLOSEUP
10_IMAGE2_9x16_FULL_BODY_MASTER_01  -> 21_IMAGE2_3x3_EXPRESSION_SHEET
10_IMAGE2_9x16_FULL_BODY_MASTER_01  -> 22_IMAGE2_TURNAROUND_CHARACTER_BOARD
```

Then update the downstream prompts so their `CHOSEN_FULL_BODY_MASTER_NODE` placeholder becomes:

```text
{{Node "10_IMAGE2_9x16_FULL_BODY_MASTER_01"}}
```

Do not run downstream nodes yet.

### If the user chooses master 02 later

Before running downstream nodes, replace all downstream edges and prompt references:

Remove or replace:

```text
10_IMAGE2_9x16_FULL_BODY_MASTER_01  -> 20_IMAGE2_FACE_PORTRAIT_CLOSEUP
10_IMAGE2_9x16_FULL_BODY_MASTER_01  -> 21_IMAGE2_3x3_EXPRESSION_SHEET
10_IMAGE2_9x16_FULL_BODY_MASTER_01  -> 22_IMAGE2_TURNAROUND_CHARACTER_BOARD
```

Create:

```text
11_IMAGE2_9x16_FULL_BODY_MASTER_02  -> 20_IMAGE2_FACE_PORTRAIT_CLOSEUP
11_IMAGE2_9x16_FULL_BODY_MASTER_02  -> 21_IMAGE2_3x3_EXPRESSION_SHEET
11_IMAGE2_9x16_FULL_BODY_MASTER_02  -> 22_IMAGE2_TURNAROUND_CHARACTER_BOARD
```

Update downstream prompt references to:

```text
{{Node "11_IMAGE2_9x16_FULL_BODY_MASTER_02"}}
```

Do the equivalent for master 03 or 04 if used.

### Verification checklist before returning the link

Before replying to the user, verify and report:

- Nodes 10/11 exist.
- Nodes 20/21/22 exist.
- All Image2 nodes are configured as standard quality + 2K when the CLI supports those parameters.
- Full-body nodes 10/11 have run or are running.
- Nodes 20/21/22 are not run yet.
- There are visible/real edges from the default master 01 to nodes 20/21/22.
- The prompts of nodes 20/21/22 reference the same master node as the visible edges.
- The canvas has no large text nodes and no overlapping nodes.

If the installed CLI cannot verify edges or quality settings, do the closest available project/node inspection and say what could and could not be verified.

## What to Run

Default run behavior:

1. Create the canvas with only image nodes.
2. Create real visible edges from full-body master 01 to downstream nodes 20/21/22.
3. Run only full-body master nodes 01 and 02.
4. Do not run face portrait, expression sheet, or turnaround board.
5. Return the LibTV canvas/project link and ask the user which master to use.

If 4 masters are requested, run 01-04 first.

## Final Chat Response Format After Canvas Creation

Do not paste generated images into chat unless the user explicitly asks.

Use this concise format:

```text
已创建 LibTV 角色画布并完成第一轮全身母版生成。

画布链接：<LibTV project/canvas link>

默认参数：
- Image2
- 标准画质
- 2K

已运行：
- 10_IMAGE2_9x16_FULL_BODY_MASTER_01
- 11_IMAGE2_9x16_FULL_BODY_MASTER_02

已预铺但未运行：
- 20_IMAGE2_FACE_PORTRAIT_CLOSEUP
- 21_IMAGE2_3x3_EXPRESSION_SHEET
- 22_IMAGE2_TURNAROUND_CHARACTER_BOARD

已建立默认连线：
- 10_IMAGE2_9x16_FULL_BODY_MASTER_01 -> 20_IMAGE2_FACE_PORTRAIT_CLOSEUP
- 10_IMAGE2_9x16_FULL_BODY_MASTER_01 -> 21_IMAGE2_3x3_EXPRESSION_SHEET
- 10_IMAGE2_9x16_FULL_BODY_MASTER_01 -> 22_IMAGE2_TURNAROUND_CHARACTER_BOARD

请在画布里选择母版 01 或 02。你确认后，我再把后续节点的连线和引用切换到选中的母版并运行。
```

If the CLI cannot provide a link, explain exactly what was created and which local command/output contains the project ID.

## Failure Handling

If anything fails:

- Do not rebuild the whole canvas.
- Read node status and error messages.
- Identify only failed or empty nodes.
- Diagnose whether the issue is prompt, reference, parameter, model, login, moderation, network, or temporary service.
- Suggest the smallest fix.
- Retry only failed nodes after the user confirms.

If only the edges are missing:

- Do not regenerate images.
- Do not recreate the project.
- Add or repair the missing edges only.
- Re-check that nodes 20/21/22 point to the same selected master in both real canvas edges and prompt references.

If only quality is wrong:

- Do not regenerate images unless the user asks.
- Update node parameters from high quality to standard quality + 2K.
- Return the link and a concise confirmation.

## Important Avoidances

Never do these by default:

- Do not make a text-heavy canvas.
- Do not create giant instruction cards on the canvas.
- Do not place text nodes on top of image nodes.
- Do not create overlapping group frames.
- Do not return generated images in chat.
- Do not run downstream nodes before the user selects a master image.
- Do not force 4 full-body masters unless asked.
- Do not create outfit/scene/video extension areas in v1.
- Do not assume prompt-only node references are visible canvas connections.
- Do not use high quality / 高画质 unless the user explicitly asks for final high quality output.
