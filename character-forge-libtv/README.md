# Character Forge LibTV Skill

Version: **1.4 expression-portrait**

This Codex skill turns a rough character direction into a clean LibTV character-generation canvas.

## Main Change in v1.4

This version fixes expression-sheet framing:

> The expression sheet must use **3:4 portrait ratio** and each of the 9 panels must show a **larger face close-up**, similar to a clean portrait reference board.

The face portrait close-up node is also tightened:

> `20_IMAGE2_FACE_PORTRAIT_CLOSEUP` should default to **3:4 portrait** with head-and-shoulders / chest-up framing and much larger face occupancy.

## Main Change in v1.3

This version changes the default image parameters to save credits:

> All Image2 image nodes default to **标准画质 + 2K**.

Do **not** use 高画质 by default.

Only use 高画质 when the user clearly asks for:

- 高画质
- 最终精修
- 最终成品图
- final high quality
- final polished version

## Main Change in v1.2

This version fixed the issue where downstream nodes were created but not visibly connected to the full-body master node.

Hard rule:

> Face portrait, 3x3 expression sheet, and turnaround board must have real LibTV canvas edges/dependencies from the current master node. Prompt-only `{{Node ...}}` references are not enough.

Default connection set after canvas creation:

```text
10_IMAGE2_9x16_FULL_BODY_MASTER_01 -> 20_IMAGE2_FACE_PORTRAIT_CLOSEUP
10_IMAGE2_9x16_FULL_BODY_MASTER_01 -> 21_IMAGE2_3x3_EXPRESSION_SHEET
10_IMAGE2_9x16_FULL_BODY_MASTER_01 -> 22_IMAGE2_TURNAROUND_CHARACTER_BOARD
```

If the user chooses master 02 later, Codex must replace the edges and prompt references so downstream nodes point to master 02 instead.

## What the Canvas Should Contain

Only image generation nodes:

- 2 Image2 9:16 full-body master nodes by default
- face portrait close-up node
- 3x3 expression sheet node
- turnaround / character board node

No heavy text nodes. Candidate roles and character DNA stay in Codex chat, not as large LibTV text cards.

## Default Image Parameters

All core image nodes:

```text
model: image2 / Lib Image when LibTV uses that display name
quality: 标准画质 / standard quality
resolution: 2K
```

Ratios:

```text
full-body master: 9:16
face portrait: 3:4 portrait ratio by default (4:5 only if 3:4 is unavailable)
3x3 expression sheet: 3:4 portrait ratio, but internally arranged as a 3x3 close-up portrait grid
turnaround board: 16:9 or wide landscape ratio
```

## Default Workflow

1. User gives a rough character direction.
2. Codex outputs 3-4 differentiated character candidates in chat.
3. User chooses one candidate.
4. Codex creates a LibTV canvas with picture nodes only.
5. Codex creates real edges from master 01 to downstream nodes.
6. Codex runs only 2 Image2 9:16 full-body master nodes first.
7. Codex prebuilds but does not run:
   - face portrait close-up
   - 3x3 expression sheet
   - turnaround / character board
8. User chooses master 01 or 02 in the LibTV canvas.
9. Codex updates downstream edges + prompt references to the chosen master and runs downstream nodes if asked.

## Suggested Message to Codex

```text
请安装并使用我上传的 character-forge-libtv skill。
阅读 README.md 和 SKILL.md。
以后创建 LibTV 角色画布时：
1. 先在聊天里输出 3-4 个候选角色，不要先建画布。
2. 我选择角色后，再创建 LibTV 画布。
3. 画布只放图片生成节点，不要大量文字节点。
4. 节点不要堆叠，必须使用清晰左右布局。
5. 所有 Image2 图片节点默认使用：标准画质 + 2K，不要使用高画质。
6. 先只运行 2 个 Image2 9:16 全身母版节点。
7. 后续脸部近景、9宫格表情、三视图节点提前创建但不要运行。
7.1 脸部近景默认使用 3:4，并让脸在画面中占比更大。
7.2 9宫格表情默认使用 3:4，并让每一格里的脸部是近景大头参考，不要小头半身。
8. 后续 3 个节点必须和默认全身母版 01 建立真实 LibTV 画布连线，不要只在 prompt 里写 {{Node}} 引用。
9. 如果我之后选择母版 02，就把后续节点的真实连线和 prompt 引用都切换到母版 02。
10. 完成后只发我画布链接、节点状态、连线状态和画质设置，不要把生成图片贴回聊天。
11. 不读取、不打印、不修改任何密钥。
```

## Repair Existing Canvas: Change High Quality to Standard Quality

If a canvas already exists and the nodes were created with 高画质, send this to Codex:

```text
使用 character-forge-libtv skill 修复当前 LibTV 画布。
不要重建画布，不要重新生成图片。
只修改图片节点参数：
1. 检查所有 Image2 图片节点。
2. 将 10/11/12/13/20/21/22 这些角色节点统一改成：标准画质 + 2K。
3. 不要使用高画质。
4. 修改后只返回画布链接、修改结果和节点参数状态，不要贴图片。
```

## Repair Existing Canvas Missing Edges

If a canvas already exists but downstream nodes are not connected, send this to Codex:

```text
使用 character-forge-libtv skill 修复当前 LibTV 画布。
不要重建画布，不要重新生成图片。
只做连线修复：
1. 找到 10_IMAGE2_9x16_FULL_BODY_MASTER_01。
2. 找到 20_IMAGE2_FACE_PORTRAIT_CLOSEUP、21_IMAGE2_3x3_EXPRESSION_SHEET、22_IMAGE2_TURNAROUND_CHARACTER_BOARD。
3. 创建真实 LibTV 画布连线：
   - 10 -> 20
   - 10 -> 21
   - 10 -> 22
4. 同步检查这 3 个子节点的 prompt 是否引用 {{Node "10_IMAGE2_9x16_FULL_BODY_MASTER_01"}}。
5. 修复后只返回画布链接、连线状态和是否成功，不要重新跑图，不要贴图片。
```
