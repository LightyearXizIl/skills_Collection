# skills_Collection — AI 技能合集

一个面向 **Codex / Reasonix / Claude Code** 等 AI 编码助手的**技能（Skill）合集**。每个技能是一个独立目录，包含 `SKILL.md`（技能定义）、运行脚本和 `README.md`（用途与配置说明）。

> **安全声明：本合集不包含任何 API key / token / 密钥**，所有密钥由使用者自行申请并通过环境变量注入。

## 技能清单

| 技能 | 用途 | 依赖 |
|------|------|------|
| [DeepSeek_Visualmodel](./DeepSeek_Visualmodel/) | 给无原生视觉的大模型（如 DeepSeek）"看图"：把图片路由到外部视觉模型，返回中文文字描述。支持智谱 / Gemini / SiliconFlow / 百炼 4 家视觉服务 | Python 3、requests |
| [finesse-ui](./finesse-ui/) | 构建和审查高完成度 Web 界面，覆盖品牌站、产品后台、数据可视化与电商页面，并提供可复用示例和设计检查规则 | Node.js（检测脚本）；具体项目的前端技术栈 |
| [web-clone](./web-clone/) | 网站复刻与逆向分析方法论：优先获取真实源码，覆盖静态站、React/Vue/Next、多页面及 WebGL/Canvas 重前端站点 | Node.js；Playwright/浏览器及 wget、gh 等按任务选用工具 |
| [astryx](./astryx/) | 使用 Meta Astryx 设计系统构建无障碍 React 界面；通过项目实际 CLI 查询组件、模板、Token 和主题，并支持上游组件与文档贡献 | React 19+；Astryx 与 StyleX 包按项目安装 |
| [brandkit](./brandkit/) | 生成包含 Logo、字体、配色、图形语言和应用场景的高完成度品牌视觉板 | 支持图片生成的模型或工具 |
| [canvas-ui](./canvas-ui/) | 从 Canvas UI 官方 shadcn registry 选择、安装并验证 Canvas/WebGL 交互组件，不在合集内再分发受限组件源码 | Node.js、对应前端框架；部分完整效果需要浏览器实验能力 |
| [svg-logo-designer](./svg-logo-designer/) | 从设计方向到可编辑 SVG 变体的 Logo 工作流，并附带安全性、可访问性和结构校验脚本 | Python 3（校验脚本） |
| [uiverse-galaxy](./uiverse-galaxy/) | 在 Uiverse Galaxy 上定位真实组件源码，保留作者归属后适配到现有 Web 项目 | 项目原有前端技术栈；浏览器或网络按任务使用 |
| [liquid-glass-react](./liquid-glass-react/) | 在 React 项目中集成并验证 `liquid-glass-react`，包含浏览器回退、性能和无障碍检查 | React 18+；项目当前包管理器 |
| [baseline-ui](./baseline-ui/) | 用明确的间距、层级、字体、布局、交互和动画规则快速清理 UI | 当前项目技术栈；涉及 JS 动画时使用 `motion/react` |
| [create-design-md](./create-design-md/) | 从代码仓库或真实网站证据创建、更新可验证的 `DESIGN.md` | Node.js/npm、`@google/design.md`；URL 模式需要浏览器 |
| [fixing-accessibility](./fixing-accessibility/) | 审查并修复 HTML 语义、ARIA、键盘、焦点、表单错误和对比度问题 | 当前项目技术栈；浏览器与审查工具按任务使用 |
| [fixing-metadata](./fixing-metadata/) | 修复标题、canonical、robots、社交卡片、图标、manifest 和 JSON-LD | 当前项目技术栈；分享卡片验证需要真实 URL |
| [fixing-motion-performance](./fixing-motion-performance/) | 审查并修复布局抖动、滚动驱动、滤镜和动画循环等性能问题 | 当前项目技术栈；浏览器性能工具按任务使用 |
| [improve-ui](./improve-ui/) | 基于产品真实设计证据进行只读 UI 审计，并为选定问题生成实施计划 | 无固定依赖；只在用户授权时使用渲染证据 |
| [ui-skills-root](./ui-skills-root/) | 通过官方 CLI 把 UI 任务路由到最小可用 Skill 集 | Node.js/npm、`npx ui-skills`、网络 |
| [animate](./animate/) | 从动画目的到属性、曲线、时长、中断和退出，设计并实现可上线 Web 动效 | 当前项目的前端与动画技术栈 |
| [animation-vocabulary](./animation-vocabulary/) | 把自然语言描述反查为准确的动画、手势和运动效果术语 | 无固定依赖 |
| [apple-design](./apple-design/) | 把 Apple 的手势、弹簧、动量、材质、字体和流体交互原则转译到 Web | 当前项目技术栈；目标设备与浏览器验证 |
| [emil-design-eng](./emil-design-eng/) | 应用 Emil Kowalski 的 UI 精修、组件与动画决策经验 | 当前项目技术栈 |
| [find-animation-opportunities](./find-animation-opportunities/) | 只读寻找真正值得加入动画的界面时刻，并给出精确建议 | 可读取的源码或用户授权的渲染证据 |
| [improve-animations](./improve-animations/) | 只读审计代码库动效，输出有优先级的问题和独立实施计划 | 可读取的项目源码 |
| [pick-ui-library](./pick-ui-library/) | 从精选清单中为具体前端任务选择合适的 UI 库 | 显式调用；网络用于核对当前维护和兼容状态 |
| [prototype](./prototype/) | 构建多个真正不同的可运行 UI 方案，并通过可视化选择器比较 | 显式调用；当前项目技术栈和浏览器 |
| [review-animations](./review-animations/) | 按严格设计工程标准专项评审动画代码 | 显式调用；待评审源码和可选浏览器证据 |
| [ask-sonner](./ask-sonner/) | 安装、配置、样式化和排查 Sonner React Toast | React、Sonner |
| [cut-motion](./cut-motion/) | 将本地口播素材制作成经过转写、粗剪审核、字幕或动态图形设计与校验的成片 | Python、Node.js、FFmpeg/FFprobe；完整流程按需使用 WSL2、ChatCut、HyperFrames、GSAP |
| [VoxMotion 自动剪辑](./remotion-vox/) | 把中英文旁白脚本制作成 Vox 风格 Remotion 动态图形解说视频，支持拆镜、图表、cutout、旁白对齐与 MP4 渲染 | Node.js、npm；内置 Remotion/React/TypeScript 工程模板，不内置 API key |
| [历代衣冠](./lidai-yiguan/) | 生成覆盖先秦至当代的写实人像 AI 绘画提示词，包含服饰形制、发妆、环境、光影和镜头参数 | 无固定依赖；直接出图需所在平台的图像生成能力 |
| [朝元神会实拍群像](./chaoyuan-shenhui-live-action/) | 将人物、神仙群像、天庭朝会或参考图需求扩写为真人实拍质感的生图、局部编辑与视频提示词 | 无固定依赖；参考图模式需要图片读取能力，直接生成或编辑需对应平台能力 |
| [电商买家秀](./photo-scene-replacement/) | 分析产品图的外观、结构和材质分区，并生成保持产品身份、空间可信和组图一致的换景、换手或换色提示词 | 技术标识 `photo-scene-replacement`；可读取图片的模型或环境；直接改图时需图片编辑工具 |
| [shipswift](./shipswift/) | 为 iOS/macOS 项目查找并集成生产可用的 SwiftUI 动画、图表、组件和完整功能模块配方 | Xcode、Swift、SwiftUI；免费配方无需 API key，Pro 配方需官方 MCP |
| [video-shotcraft](./video-shotcraft/) | 用镜头配方、Remotion 示例、模板和音频资产制作电影感产品宣传视频 | Node.js、Remotion、FFmpeg；完整资源包较大 |
| [MJV8 中式诗意巨物美学](./mjv8-chinese-poetic-worlds/) | 将一句话或参考图扩写为中式诗意巨物美学图片提示词，并可依据成图编写短视频动态提示词 | 无固定依赖；直接生成图片或视频需对应平台能力 |
| [AI 打斗导演](./ai-fight-director/) | 编排具有攻防因果、空间调度、速度感和打击反馈的 AI 视频打斗提示词 | 无固定依赖；成片分析需要视频读取能力 |
| [单图生成电商 TVC](./generate-product-tvc-sd25/) | 从产品参考图生成包含视觉锁定、镜头、声音与连续性约束的 30 秒 Seedance 2.5 广告提示词 | 图片读取能力；直接生成视频需对应平台能力 |
| [中式仙境场景与视频提示词](./write-seedance-image-video-prompt/) | 批量生成中式仙境图片提示词，或根据成图编写受控的 Seedance 图生视频提示词 | 无固定依赖；图生视频阶段需要读取成图 |
| [黄金结构视频提示词优化器](./golden-structure-video-prompt-optimizer/) | 将零散创意、剧本或分镜重构为 6+2 黄金结构的视频生成提示词 | 无固定依赖 |
| [Character Forge LibTV](./character-forge-libtv/) | 从粗略角色方向生成候选设计，并规划带可见连接的 LibTV 角色资产画布 | LibTV Skill/CLI 与相应授权 |
| [Story Asset Builder](./story-asset-builder/) | 将剧本拆解为人物、场景、道具、怪兽、载具、色卡、分镜和视频段落资产提示词 | 实际创建画布需要 LibTV Skill/CLI 与 `LIBTV_ACCESS_KEY` 或平台授权 |
| [短剧悬疑感剧本](./short-drama-suspense-script/) | 为约 60 秒竖屏短剧设计冲突、动作拐点、信息反转和跨镜头一致性 | 无固定依赖；直接生成视频需对应平台能力 |
| DeterminFlow 内置 Skill（6 个） | Agent 定义、自动化、提示模板、脚本库、规则和工作流配置指南 | DeterminFlow 运行时；见各目录 |
| [OpenMontage Skill 集](./OPENMONTAGE_SKILLS.md)（82 个） | 视频制作、媒体处理、语音、图像、三维、Remotion 与服务集成工作流 | 依具体 Skill 而定；部分需要第三方服务或本地工具 |
| [Yichen Skill 集](./YICHEN_SKILLS.md)（19 个 Skill + 1 个插件） | 写作、研究、内容归档、ASR、社交收藏、微信/企微本地工作流和 X 内容制作 | 依具体 Skill 而定；部分仅支持 macOS 或需要浏览器登录态、第三方 CLI |

## 安装方法

### 方式一：复制技能目录

把所需技能目录（例如 `brandkit/`、`canvas-ui/` 或 `liquid-glass-react/`）整个复制到你的技能目录：

- **Reasonix 项目级**：`<工作区>/.reasonix/skills/`
- **Reasonix 全局**：`%AppData%/reasonix/skills/`（或 `<Reasonix home>/skills/`）
- **Codex 全局**：`~/.codex/skills/`
- **Claude Code**：`~/.claude/skills/`

### 方式二：注册技能根（Reasonix）

克隆本仓库后，在全局 `config.toml` 的 `[skills]` 中加入：

```toml
[skills]
paths = ["<本仓库克隆路径>"]
```

## API Key 配置（重要）

**所有技能都不内置密钥**。各技能所需的环境变量如下，请自行到对应平台免费申请：

| 环境变量 | 服务 | 申请地址 | 说明 |
|----------|------|----------|------|
| `ZHIPU_API_KEY` | 智谱 BigModel | https://open.bigmodel.cn/ | `glm-4.6v-flash` 等免费视觉模型 |
| `GEMINI_API_KEY` | Google Gemini | https://aistudio.google.com/apikey | Free Tier 免费（国内需代理） |
| `SILICONFLOW_API_KEY` | 硅基流动 SiliconFlow | https://siliconflow.cn/ | 免费 OCR 模型 |
| `DASHSCOPE_API_KEY` | 阿里云百炼 | https://bailian.console.aliyun.com/ | 视觉模型按量付费 |

## 使用示例

```bash
# 让 DeepSeek 看懂图片（默认智谱免费模型）
python "DeepSeek_Visualmodel/eyes.py" "图片.png" --prompt "这张图里写了什么？"

# 指定视觉服务商（Gemini 更强、SiliconFlow 适合文字提取）
python "DeepSeek_Visualmodel/eyes.py" "图片.png" --prompt "详细描述这张截图" --provider gemini
python "DeepSeek_Visualmodel/eyes.py" "图片.png" --prompt "提取图中所有文字" --provider siliconflow
```

不需要 API key 的方法论类技能可直接通过自然语言触发，例如：

```text
用 finesse-ui 设计一个高完成度的数据看板
用 web-clone 复刻这个网站：https://example.com
用 astryx 构建一个无障碍 React 管理后台
用 brandkit 为这个产品生成完整品牌视觉板
用 canvas-ui 给 React 项目加入可回退的液态按钮
用 svg-logo-designer 设计三个可编辑的 SVG Logo 方向
用 uiverse-galaxy 找一个合适的加载动画并适配现有样式
用 liquid-glass-react 为卡片加入兼容性良好的液态玻璃效果
用 baseline-ui 清理这个页面的基础 UI 问题
用 create-design-md 从当前仓库创建 DESIGN.md
用 fixing-accessibility 修复这个表单的键盘和焦点问题
用 fixing-metadata 审查网站的 SEO 与分享卡片
用 fixing-motion-performance 排查滚动动画卡顿
用 improve-ui 只读审计产品工作台并提出有证据的问题
用 ui-skills-root 为这个 UI 任务选择最合适的专项 Skill
用 animate 为这个弹窗设计并实现进入与退出动画
用 animation-vocabulary 告诉我这个回弹效果的准确名称
用 apple-design 设计一个可中断的拖拽底部面板
用 emil-design-eng 改善这个组件的完成度
用 find-animation-opportunities 找出真正值得加入动效的地方
用 improve-animations 审计整个应用的动画系统
显式使用 pick-ui-library 为这个项目选择 Toast 库
显式使用 prototype 构建四种不同的 Toast 交互方案
显式使用 review-animations 评审这次动画改动
用 ask-sonner 排查这个 React 项目里重复出现的 Toast
用 cut-motion 把本地口播视频制作成带字幕和局部 MG 的成片
用 VoxMotion 自动剪辑把这段旁白制作成 16:9 的 Vox 风格解说视频
用历代衣冠写一个明制仕女的写实人像提示词
用朝元神会实拍群像写一幅二十位神仙在白玉云台朝会的真人实拍提示词
用电商买家秀总结这组产品图的外观结构，并生成统一场景的换景提示词
用 shipswift 给 SwiftUI 页面加入 shimmer 加载效果
用 video-shotcraft 为桌面产品制作一支宣传视频
用 mjv8-chinese-poetic-worlds 写一组巨荷水乡的中式诗意图片提示词
用 ai-fight-director 把双人剑斗创意编排成有因果的打斗提示词
用 generate-product-tvc-sd25 为这张产品图写一支 30 秒电商广告提示词
用 write-seedance-image-video-prompt 生成 10 个中式仙境场景
用 golden-structure-video-prompt-optimizer 优化这段零散的视频分镜
用 character-forge-libtv 规划一个角色资产画布
用 story-asset-builder 把这份剧本拆成 LibTV 资产节点
用 short-drama-suspense-script 设计一支 60 秒竖屏悬疑短剧
使用 workflow-guide 编写 DeterminFlow 工作流
使用 video-edit 剪辑并导出产品演示视频
```

## 原创 Skill

- `lidai-yiguan`（历代衣冠）：由本仓库维护者 [LightyearXizIl](https://github.com/LightyearXizIl) 原创，采用 MIT License。
- `remotion-vox`（VoxMotion 自动剪辑）：由本仓库维护者 [LightyearXizIl](https://github.com/LightyearXizIl) 原创，采用 MIT License。
- `chaoyuan-shenhui-live-action`（朝元神会实拍群像）：由本仓库维护者 [LightyearXizIl](https://github.com/LightyearXizIl) 编写，采用 MIT License；风格基准仅归纳公开参考视频的视觉语法，不收录或再分发视频及其中素材。

## 第三方来源与授权

- `finesse-ui`：来源于 [zhenwusw/finesse-skill](https://github.com/zhenwusw/finesse-skill)，技能主体采用 MIT License；其示例中附带的 GSAP/ScrollTrigger 文件遵循文件头标注的 [GreenSock Standard License](https://gsap.com/standard-license/)。
- `web-clone`：来源于 [Jane-xiaoer/claude-skill-web-clone](https://github.com/Jane-xiaoer/claude-skill-web-clone)，采用 MIT License。
- `astryx`：适配自 [facebook/astryx](https://github.com/facebook/astryx) 的官方 Agent/Claude 指令与文档，保留 Meta 的 MIT License；当前快照为 `077087f68d5e5fc12b39218a67dfa6a29fa04bcd`。
- `brandkit`：原样安装自 [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) 的 `skills/brandkit`，采用 MIT License；当前快照为 `e988add20dab0fa97d7a76781c48961c8184288e`。
- `canvas-ui`：面向 [DavidHDev/canvas-ui](https://github.com/DavidHDev/canvas-ui) 创建的安全适配 Skill，固定参考快照 `81b65e159c63bde7167b9b4b458a775838e4cd39`。上游采用 MIT + Commons Clause，禁止将其组件本身出售、再许可或再分发；本合集只保留官方文档快照和安装工作流，不复制组件源码。
- `svg-logo-designer`：参考 [rknall/claude-skills](https://github.com/rknall/claude-skills) 中同名功能重新独立编写。检查时上游未提供明确许可证，因此没有复制或再分发其原始 Skill 内容；本合集版本采用独立 MIT License。
- `uiverse-galaxy`：面向 [uiverse-io/galaxy](https://github.com/uiverse-io/galaxy) 创建的适配 Skill，保留上游 MIT License 和 README 快照；当前快照为 `adbd2adde0a299a3956ea288fb444ec01891ca41`。
- `liquid-glass-react`：面向 [rdev/liquid-glass-react](https://github.com/rdev/liquid-glass-react) 创建的适配 Skill，保留上游 MIT License、README 和包信息快照；当前快照为 `ac48eab18d1f7f444ae30002d240cae29c863a21`。
- `baseline-ui`、`create-design-md`、`fixing-accessibility`、`fixing-metadata`、`fixing-motion-performance`、`improve-ui`、`ui-skills-root`：安装自 [ibelick/ui-skills](https://github.com/ibelick/ui-skills)，采用 MIT License，固定快照为 `2b3a114a3fcff079d73639a21710c595d4700a74`。其中 `fixing-metadata` 仅将上游不兼容的顶层 `version` 移入 `metadata.version`，其余技能正文保持上游内容。
- `animate`、`animation-vocabulary`、`apple-design`、`emil-design-eng`、`find-animation-opportunities`、`improve-animations`、`pick-ui-library`、`prototype`、`review-animations`：安装自 [emilkowalski/skills](https://github.com/emilkowalski/skills)，采用 MIT License，固定快照为 `de33dbed000212b54400a33767d1e4d03654db2a`。`pick-ui-library`、`prototype`、`review-animations` 的上游 `disable-model-invocation: true` 已等价迁移到 `agents/openai.yaml` 的 `policy.allow_implicit_invocation: false`；正文不变。
- `ask-sonner`：安装自 [emilkowalski/skills](https://github.com/emilkowalski/skills)，采用 MIT License，固定快照为 `78761e1b57f97dce65b983d640c70a68f39e8163`。
- `cut-motion`：适配自 [Endless1936/cut-motion](https://github.com/Endless1936/cut-motion)，完整内置固定快照 `b4afa7f2823db07322caf624ffc9096ea48145c9` 的 145 个上游文件，另含快照来源清单、Codex Skill 适配入口和安全工作区准备脚本。上游代码、文档及模板采用 Apache-2.0；已保留 `LICENSE`、`NOTICE`，人物参考图与第三方工具、字体、用户媒体继续受各自权利和许可约束。
- `shipswift`：安装自 [signerlabs/shipswift-skills](https://github.com/signerlabs/shipswift-skills) 的 `skills/shipswift`，包含 84 个免费 SwiftUI 配方和完整索引；该仓库 README 声明采用 MIT License，目录内许可文本取自关联的 [signerlabs/ShipSwift](https://github.com/signerlabs/ShipSwift) 主仓库，固定快照为 `b1dcfcd85dfae0202591642b8c9efe3edd32410b`。5 个 Pro 配方仅通过官方 MCP 提供，未收录在本合集。
- `video-shotcraft`：完整安装自 [Vincentwei1021/video-shotcraft](https://github.com/Vincentwei1021/video-shotcraft)，采用 Apache-2.0，固定快照为 `41ee360d82f4c491ba9d88a24a4add7d8ff1cf8b`。其音频、示例素材和镜头归属说明以目录内 `assets/audio/ATTRIBUTION.md`、`references/shots/ATTRIBUTION.md` 为准。
- `agent-definition-guide`、`automation-guide`、`prompt-template-guide`、`script-library-guide`、`skill-rule-authoring-guide`、`workflow-guide`：安装自 [alikon-art/DeterminFlow](https://github.com/alikon-art/DeterminFlow)，固定快照为 `fe217de1e58bf53581cdfe973e134902d8ee062a`，均遵循目录内 AGPLv3。
- [OpenMontage Skill 集](./OPENMONTAGE_SKILLS.md)：从 [calesthio/OpenMontage](https://github.com/calesthio/OpenMontage) 的 `.agents/skills` 收录 82 个实际 Skill 目录，固定快照为 `4eab34c5cfcccaa4f1970554928feccce73ee930`，均遵循目录内 AGPLv3。`gsap/` 是上游容器目录而非 Skill；`.claude/skills/video_toolkit` 与 `video-toolkit` 内容相同，因此未重复收录。12 个仅有 frontmatter 兼容问题的目录做了最小字段清理或 YAML 转义，正文未改。
- [Yichen Skill 集](./YICHEN_SKILLS.md)：从 [mcncarl/yichen-skills](https://github.com/mcncarl/yichen-skills) 收录 19 个顶层 Skill 和 `yichen-grok-consult` Codex 插件，固定快照为 `2f916dc58d5d8abb563209d76ca6ba059ef0be3c`。上游采用个人学习与非商业使用许可；仓库操作者确认已获得作者对本次公开收录的书面授权。各目录继续受上游许可约束，授权不等于改为 MIT，也不扩大下游用户权限。
- `mjv8-chinese-poetic-worlds`、`ai-fight-director`、`generate-product-tvc-sd25`、`write-seedance-image-video-prompt`、`golden-structure-video-prompt-optimizer`、`character-forge-libtv`、`story-asset-builder`、`short-drama-suspense-script`：来自[飞书“操作流程教程合集”](https://ei5ttplwuwy.feishu.cn/wiki/BSLqw36K3iMKxZkkX2ucYkxznrb)中的公开附件或页面内嵌 Skill。仓库维护者确认已取得原作者对本次公开收录的许可；原始内容没有附带开放源代码许可证，因此版权仍归原作者，根目录 MIT 不覆盖这些目录，也不向下游额外授予再使用或再分发许可。每个目录的来源页面、原包名称、SHA-256 和兼容性改动见其 `SOURCE.md`。

各技能目录内的独立许可证和归属说明优先适用于相应第三方内容。根目录 MIT 许可证只适用于本合集自行创作的内容及未另行声明的部分，**不覆盖** `cut-motion`、`video-shotcraft` 的 Apache-2.0 内容、DeterminFlow/OpenMontage 的 AGPLv3 内容、Yichen Skills 的个人学习与非商业使用许可内容，或上述 8 个仅获本次收录许可、未采用开放许可证的飞书 Skill；这些目录按各自权利边界分发。

## 新增技能规范

往本合集添加新技能时请遵守：

1. 每个技能一个目录，目录名即技能名，含 `SKILL.md`（frontmatter 必须带 `name` + `description`）
2. 目录内必须有 `README.md`：说明**这个技能是干嘛的**、使用方法、所需 API key 及配置方式
3. **禁止包含任何 API key、token、密码**——一律通过环境变量注入
4. 依赖保持必要且明确；不得为了一个 Skill 无关地迁移项目框架或工具链
5. 收录第三方内容时必须保留其独立许可证、来源提交和归属/资产说明；不得把子目录内容错误地宣称为根目录 MIT

## License

MIT
