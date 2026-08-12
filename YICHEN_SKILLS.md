# Yichen Skills

本目录组收录自 [mcncarl/yichen-skills](https://github.com/mcncarl/yichen-skills)，固定上游提交为 `2f916dc58d5d8abb563209d76ca6ba059ef0be3c`。

上游采用 Personal Learning and Non-Commercial Use License。仓库操作者已确认取得作者对本次公开收录的书面授权；该授权不改变下游用户的使用范围。每个目录内的 `LICENSE.upstream` 和 `THIRD_PARTY_NOTICES.upstream.md` 优先适用，根目录 MIT License 不覆盖这些内容。

## 收录内容

| 名称 | 用途 |
|---|---|
| `yichen-agent-memory` | 安装和维护 Markdown/Obsidian 优先的 Agent Memory Vault |
| `yichen-asr` | 在 Step ASR 与火山引擎豆包 ASR 之间按输出需求路由 |
| `yichen-bookmarks-export` | 在当轮明确授权后导出私人收藏链接 |
| `yichen-chatgpt-web-research` | 通过用户已登录的 ChatGPT 官方网页执行研究 |
| `yichen-content-archive` | 读取、下载和归档已知或已确认的内容链接 |
| `yichen-jianying-editor` | 指导剪映/CapCut 桌面端导入、剪辑和导出 |
| `yichen-mac-wechat-dual-open` | 在 macOS 创建、修复和区分第二个微信应用 |
| `yichen-social-bookmarks-exporter` | 导出小红书、抖音和 X 的私人收藏链接 |
| `yichen-summary` | 把当前对话精华整理到 Obsidian |
| `yichen-unified-search` | 跨公共网页和社交平台统一搜索候选 |
| `yichen-video-content` | 拆解对标视频口播稿并生成改进报告 |
| `yichen-volc-asr` | 使用火山引擎转写、生成字幕和口播粗剪 |
| `yichen-web-research` | 为多阶段互联网研究选择搜索、归档和转写路线 |
| `yichen-wechat-local-vault` | 只读解析 macOS 微信本地数据并生成私有资产库 |
| `yichen-wechat-mp-batch-exporter` | 批量导出微信公众号文章历史和可选指标 |
| `yichen-wecom-local-vault` | 只读解析 macOS 企业微信 5.x 本地数据库 |
| `yichen-wecom-operations` | 通过官方 CLI 操作获授权的企微文档、待办、会议和日程 |
| `yichen-x-article-draft-uploader` | 把 Markdown 上传到 X Articles 草稿 |
| `yichen-x-slicer` | 把公开 X 帖子或线程制作成 3:4 图片切片与视频 |
| `plugins/yichen-grok-consult` | 通过官方 Grok CLI 获取第二意见或执行原生 X 搜索的 Codex 插件 |

## 安装

普通 Skill 可把对应 `yichen-*` 目录复制到 `~/.codex/skills/`。Grok Consult 是完整插件，不应只复制其嵌套 Skill；请按 [`plugins/yichen-grok-consult/README.zh.md`](./plugins/yichen-grok-consult/README.zh.md) 的 marketplace 安装说明操作。

部分 Skill 依赖 macOS、浏览器登录态、第三方 CLI 或自行配置的环境变量。运行前以各目录的 `SKILL.md` 和 `README.md` 为准，不要提交真实 cookie、token、数据库密钥或个人数据。
