# story-asset-builder 使用说明

这是一个通用“剧本资产生成 Skill”，用于配合 LibTV skill / LibTV CLI，把任意剧本自动拆成资产节点，并生成标准化 Prompt。

## 安装

把整个文件夹复制到：

```bash
~/.openclaw/skills/story-asset-builder/
```

或将压缩包解压到：

```bash
~/.openclaw/skills/
```

确认你已经安装并授权 LibTV skill / LibTV CLI：

```bash
export LIBTV_ACCESS_KEY="<your-access-key>"
```

## 最推荐的使用指令

```text
使用 story-asset-builder。
这是一个新项目，请先根据剧本创建 Project Profile，再创建 LibTV 资产准备画布。

剧本：
【粘贴你的剧本】

要求：
1. 自动拆解人物、场景、道具、怪兽、载具、色卡、分镜资产
2. 每个资产按工业化提示词文档格式生成完整 Prompt
3. 调用 LibTV 创建新项目和画布节点
4. 只准备资产图节点，先不要直接生成最终视频
5. 所有节点必须放到画布上
6. 每个节点附带实操注意和跑歪兜底加强
```

## 用已有 Profile

```text
使用 story-asset-builder。
项目 Profile：wansheng。
根据下面剧本创建 LibTV 资产准备画布：
【剧本内容】
```

## 注意

本 Skill 负责“资产拆解 + Prompt 编译 + LibTV 节点编排”。真正生成图片/视频仍由 LibTV skill / LibTV CLI 执行。
