<div align="center">

# skills_Collection

**AI 技能合集 · 165 个可插拔 Skill · 8 大分类**

面向 **Codex / Claude Code / Reasonix** 等 AI 编程助手的技能库。
每个技能是一个独立目录，含 `SKILL.md` 定义、运行脚本与使用说明。

[![Skills](https://img.shields.io/badge/Skills-165-2ea44f?style=flat-square)](./skills)
[![Categories](https://img.shields.io/badge/Categories-8-2563eb?style=flat-square)](#分类目录)
[![License](https://img.shields.io/badge/License-MIT-16a34a?style=flat-square)](./LICENSE)
[![Secrets](https://img.shields.io/badge/Secrets-None-critical?style=flat-square)](#api-key-配置重要)

[![开始使用](https://img.shields.io/badge/开始使用-快速安装-2563eb?style=for-the-badge)](#安装方法)
[![技能目录](https://img.shields.io/badge/技能目录-分类浏览-16a34a?style=for-the-badge)](#分类目录)
[![自建技能](https://img.shields.io/badge/自建技能-16%20个-ea580c?style=for-the-badge)](#我的自建技能)

[最近更新](#最近更新) · [分类目录](#分类目录) · [自建技能](#我的自建技能) · [安装方法](#安装方法) · [API Key](#api-key-配置重要) · [原创声明](#原创-skill) · [参与贡献](#新增技能规范)

</div>

> **安全声明**：本合集不包含任何 API key / token / 密钥，所有密钥由使用者自行申请并通过环境变量注入。

## 最近更新

- **2026-11-03** — 目录重构：原本散落在根目录的 153 个条目收敛为 `skills/` 下 8 个分类，根目录只保留一个总文件夹；同时收录 16 个自建技能（图像美学 7、产品视觉 3、视频 2、平台与工具 3、工作流 1），并为全部 165 个技能补齐可检索目录。
- **2026-10-28** — 新增 `xiaohongshu-3c-brand-visual`：小红书 3C 数码配件视觉方案生成器。
- **2026-10-27** — 收录 Yichen Skill 集（19 个 Skill）与 `yichen-grok-consult` Codex 插件。

## 目录结构

```text
skills_Collection/
├── skills/
│   ├── 01-ui-frontend/        前端与 UI 工程
│   ├── 02-animation/          动画与动效
│   ├── 03-video/              视频制作
│   ├── 04-image/              图像与视觉风格
│   ├── 05-audio/              语音与音频
│   ├── 06-ai-platforms/       AI 平台接入
│   ├── 07-content-ops/        内容运营
│   ├── 08-toolkit-guides/     工具与规范指南
│   └── _plugins/              Codex 插件包
├── .agents/plugins/marketplace.json
├── OPENMONTAGE_SKILLS.md      82 个技能索引
├── YICHEN_SKILLS.md           19 个技能索引
└── README.md
```

> `.agents/` 为 Codex marketplace 发现所需的隐藏配置，保留在根目录；插件本体已归入 `skills/_plugins/`。

## 分类目录

### 01 前端与 UI 工程 · 26 个

<sub>界面实现、设计系统、可访问性与 Web 逆向</sub>

| 技能 | 用途 | 依赖 |
|---|------|------|
| [apple-design](./skills/01-ui-frontend/apple-design/) | 把 Apple 的手势、弹簧、动量、材质、字体和流体交互原则转译到 Web | 当前项目技术栈；目标设备与浏览器验证 |
| [ask-sonner](./skills/01-ui-frontend/ask-sonner/) | 安装、配置、样式化和排查 Sonner React Toast | React、Sonner |
| [astryx](./skills/01-ui-frontend/astryx/) | 使用 Meta Astryx 设计系统构建无障碍 React 界面；通过项目实际 CLI 查询组件、模板、Token 和主题，并支持上游组件与文档贡献 | React 19+；Astryx 与 StyleX 包按项目安装 |
| [baseline-ui](./skills/01-ui-frontend/baseline-ui/) | 用明确的间距、层级、字体、布局、交互和动画规则快速清理 UI | 当前项目技术栈；涉及 JS 动画时使用 `motion/react` |
| [beautiful-mermaid](./skills/01-ui-frontend/beautiful-mermaid/) | Render Mermaid diagrams as SVG and PNG using the… | — |
| [brandkit](./skills/01-ui-frontend/brandkit/) | 生成包含 Logo、字体、配色、图形语言和应用场景的高完成度品牌视觉板 | 支持图片生成的模型或工具 |
| [canvas-ui](./skills/01-ui-frontend/canvas-ui/) | 从 Canvas UI 官方 shadcn registry 选择、安装并验证 Canvas/WebGL 交互组件，不在合集内再分发受限组件源码 | Node.js、对应前端框架；部分完整效果需要浏览器实验能力 |
| [create-design-md](./skills/01-ui-frontend/create-design-md/) | 从代码仓库或真实网站证据创建、更新可验证的 `DESIGN.md` | Node.js/npm、`@google/design.md`；URL 模式需要浏览器 |
| [d3-viz](./skills/01-ui-frontend/d3-viz/) | Creating interactive data visualisations using d3.js.… | — |
| [emil-design-eng](./skills/01-ui-frontend/emil-design-eng/) | 应用 Emil Kowalski 的 UI 精修、组件与动画决策经验 | 当前项目技术栈 |
| [finesse-ui](./skills/01-ui-frontend/finesse-ui/) | 构建和审查高完成度 Web 界面，覆盖品牌站、产品后台、数据可视化与电商页面，并提供可复用示例和设计检查规则 | Node.js（检测脚本）；具体项目的前端技术栈 |
| [fixing-accessibility](./skills/01-ui-frontend/fixing-accessibility/) | 审查并修复 HTML 语义、ARIA、键盘、焦点、表单错误和对比度问题 | 当前项目技术栈；浏览器与审查工具按任务使用 |
| [fixing-metadata](./skills/01-ui-frontend/fixing-metadata/) | 修复标题、canonical、robots、社交卡片、图标、manifest 和 JSON-LD | 当前项目技术栈；分享卡片验证需要真实 URL |
| [improve-ui](./skills/01-ui-frontend/improve-ui/) | 基于产品真实设计证据进行只读 UI 审计，并为选定问题生成实施计划 | 无固定依赖；只在用户授权时使用渲染证据 |
| [liquid-glass-react](./skills/01-ui-frontend/liquid-glass-react/) | 在 React 项目中集成并验证 `liquid-glass-react`，包含浏览器回退、性能和无障碍检查 | React 18+；项目当前包管理器 |
| [pick-ui-library](./skills/01-ui-frontend/pick-ui-library/) | 从精选清单中为具体前端任务选择合适的 UI 库 | 显式调用；网络用于核对当前维护和兼容状态 |
| [prototype](./skills/01-ui-frontend/prototype/) | 构建多个真正不同的可运行 UI 方案，并通过可视化选择器比较 | 显式调用；当前项目技术栈和浏览器 |
| [shipswift](./skills/01-ui-frontend/shipswift/) | 为 iOS/macOS 项目查找并集成生产可用的 SwiftUI 动画、图表、组件和完整功能模块配方 | Xcode、Swift、SwiftUI；免费配方无需 API key，Pro 配方需官方 MCP |
| [svg-logo-designer](./skills/01-ui-frontend/svg-logo-designer/) | 从设计方向到可编辑 SVG 变体的 Logo 工作流，并附带安全性、可访问性和结构校验脚本 | Python 3（校验脚本） |
| [tailwind-design-system](./skills/01-ui-frontend/tailwind-design-system/) | Build scalable design systems with Tailwind CSS v4,… | — |
| [ui-skills-root](./skills/01-ui-frontend/ui-skills-root/) | 通过官方 CLI 把 UI 任务路由到最小可用 Skill 集 | Node.js/npm、`npx ui-skills`、网络 |
| [uiverse-galaxy](./skills/01-ui-frontend/uiverse-galaxy/) | 在 Uiverse Galaxy 上定位真实组件源码，保留作者归属后适配到现有 Web 项目 | 项目原有前端技术栈；浏览器或网络按任务使用 |
| [vercel-composition-patterns](./skills/01-ui-frontend/vercel-composition-patterns/) |  | — |
| [vercel-react-best-practices](./skills/01-ui-frontend/vercel-react-best-practices/) | React and Next.js performance optimization guidelines… | — |
| [web-clone](./skills/01-ui-frontend/web-clone/) | 网站复刻与逆向分析方法论：优先获取真实源码，覆盖静态站、React/Vue/Next、多页面及 WebGL/Canvas 重前端站点 | Node.js；Playwright/浏览器及 wget、gh 等按任务选用工具 |
| [web-design-guidelines](./skills/01-ui-frontend/web-design-guidelines/) | Review UI code for Web Interface Guidelines… | — |

### 02 动画与动效 · 45 个

<sub>GSAP / Three.js / Remotion / HyperFrames / Manim 等动效代码</sub>

| 技能 | 用途 | 依赖 |
|---|------|------|
| [animate](./skills/02-animation/animate/) | 从动画目的到属性、曲线、时长、中断和退出，设计并实现可上线 Web 动效 | 当前项目的前端与动画技术栈 |
| [animation-vocabulary](./skills/02-animation/animation-vocabulary/) | 把自然语言描述反查为准确的动画、手势和运动效果术语 | 无固定依赖 |
| [canvas-procedural-animation](./skills/02-animation/canvas-procedural-animation/) | Use p5.js/canvas for local procedural character… | — |
| [character-animation-qa](./skills/02-animation/character-animation-qa/) | Review local character animation with schema checks,… | — |
| [character-rigging](./skills/02-animation/character-rigging/) | Build data-driven 2D character rigs for local… | — |
| [find-animation-opportunities](./skills/02-animation/find-animation-opportunities/) | 只读寻找真正值得加入动画的界面时刻，并给出精确建议 | 可读取的源码或用户授权的渲染证据 |
| [fixing-motion-performance](./skills/02-animation/fixing-motion-performance/) | 审查并修复布局抖动、滚动驱动、滤镜和动画循环等性能问题 | 当前项目技术栈；浏览器性能工具按任务使用 |
| [framer-motion](./skills/02-animation/framer-motion/) | implementing Disney's 12 animation principles with… | — |
| [gsap-core](./skills/02-animation/gsap-core/) | Official GSAP skill for the core API — gsap.to(),… | — |
| [gsap-frameworks](./skills/02-animation/gsap-frameworks/) | Official GSAP skill for Vue, Svelte, and other… | — |
| [gsap-performance](./skills/02-animation/gsap-performance/) | Official GSAP skill for performance — prefer… | — |
| [gsap-plugins](./skills/02-animation/gsap-plugins/) | Official GSAP skill for GSAP plugins — registration,… | — |
| [gsap-react](./skills/02-animation/gsap-react/) | Official GSAP skill for React — useGSAP hook, refs,… | — |
| [gsap-scrolltrigger](./skills/02-animation/gsap-scrolltrigger/) | Official GSAP skill for ScrollTrigger — scroll-linked… | — |
| [gsap-timeline](./skills/02-animation/gsap-timeline/) | Official GSAP skill for timelines — gsap.timeline(),… | — |
| [gsap-utils](./skills/02-animation/gsap-utils/) | Official GSAP skill for gsap.utils — clamp, mapRange,… | — |
| [hyperframes](./skills/02-animation/hyperframes/) | READ THIS FIRST for any request to make, create, edit… | — |
| [hyperframes-animation](./skills/02-animation/hyperframes-animation/) | All animation knowledge for HyperFrames — atomic… | — |
| [hyperframes-cli](./skills/02-animation/hyperframes-cli/) | HyperFrames CLI dev loop. Use when running npx… | — |
| [hyperframes-core](./skills/02-animation/hyperframes-core/) | The HyperFrames composition contract — build one… | — |
| [hyperframes-creative](./skills/02-animation/hyperframes-creative/) | Non-animation creative direction for HyperFrames… | — |
| [hyperframes-media](./skills/02-animation/hyperframes-media/) | Audio and media assets for HyperFrames compositions,… | — |
| [hyperframes-registry](./skills/02-animation/hyperframes-registry/) | Install and wire registry blocks and components into… | — |
| [improve-animations](./skills/02-animation/improve-animations/) | 只读审计代码库动效，输出有优先级的问题和独立实施计划 | 可读取的项目源码 |
| [lottie-bodymovin](./skills/02-animation/lottie-bodymovin/) | implementing Disney's 12 animation principles with… | — |
| [manim-composer](./skills/02-animation/manim-composer/) | Trigger when: (1) User wants to create an… | — |
| [manimce-best-practices](./skills/02-animation/manimce-best-practices/) | Trigger when: (1) User mentions "manim" or "Manim… | — |
| [manimgl-best-practices](./skills/02-animation/manimgl-best-practices/) | Trigger when: (1) User mentions "manimgl" or… | — |
| [motion-graphics](./skills/02-animation/motion-graphics/) | the user wants a short, design-led motion graphic… | — |
| [remotion](./skills/02-animation/remotion/) | Toolkit-specific Remotion patterns — custom… | — |
| [remotion-best-practices](./skills/02-animation/remotion-best-practices/) | Best practices for Remotion - Video creation in React | — |
| [remotion-to-hyperframes](./skills/02-animation/remotion-to-hyperframes/) | Port an existing Remotion (React) composition to… | — |
| [VoxMotion 自动剪辑](./skills/02-animation/remotion-vox/) | 把中英文旁白脚本制作成 Vox 风格 Remotion 动态图形解说视频，支持拆镜、图表、cutout、旁白对齐与 MP4 渲染 | Node.js、npm；内置 Remotion/React/TypeScript 工程模板，不内置 API key |
| [review-animations](./skills/02-animation/review-animations/) | 按严格设计工程标准专项评审动画代码 | 显式调用；待评审源码和可选浏览器证据 |
| [svg-character-animation](./skills/02-animation/svg-character-animation/) | Animate SVG character rigs with GSAP, CSS transforms,… | — |
| [threejs-animation](./skills/02-animation/threejs-animation/) | Three.js animation - keyframe animation, skeletal… | — |
| [threejs-fundamentals](./skills/02-animation/threejs-fundamentals/) | Three.js scene setup, cameras, renderer, Object3D… | — |
| [threejs-geometry](./skills/02-animation/threejs-geometry/) | Three.js geometry creation - built-in shapes,… | — |
| [threejs-interaction](./skills/02-animation/threejs-interaction/) | Three.js interaction - raycasting, controls,… | — |
| [threejs-lighting](./skills/02-animation/threejs-lighting/) | Three.js lighting - light types, shadows, environment… | — |
| [threejs-loaders](./skills/02-animation/threejs-loaders/) | Three.js asset loading - GLTF, textures, images,… | — |
| [threejs-materials](./skills/02-animation/threejs-materials/) | Three.js materials - PBR, basic, phong, shader… | — |
| [threejs-postprocessing](./skills/02-animation/threejs-postprocessing/) | Three.js post-processing - EffectComposer, bloom, DOF… | — |
| [threejs-shaders](./skills/02-animation/threejs-shaders/) | Three.js shaders - GLSL, ShaderMaterial, uniforms,… | — |
| [threejs-textures](./skills/02-animation/threejs-textures/) | Three.js textures - texture types, UV mapping,… | — |

### 03 视频制作 · 25 个

<sub>生成、剪辑、数字人、字幕与发布包装</sub>

| 技能 | 用途 | 依赖 |
|---|------|------|
| [AI 打斗导演](./skills/03-video/ai-fight-director/) | 编排具有攻防因果、空间调度、速度感和打击反馈的 AI 视频打斗提示词 | 无固定依赖；成片分析需要视频读取能力 |
| [ai-video-gen](./skills/03-video/ai-video-gen/) | Generate AI videos from text prompts using multiple… | — |
| [avatar-video](./skills/03-video/avatar-video/) | Create AI avatar videos with precise control over… | — |
| [Character Forge LibTV](./skills/03-video/character-forge-libtv/) | 从粗略角色方向生成候选设计，并规划带可见连接的 LibTV 角色资产画布 | LibTV Skill/CLI 与相应授权 |
| [create-video](./skills/03-video/create-video/) | Create videos from a text prompt using HeyGen's Video… | — |
| [cut-motion](./skills/03-video/cut-motion/) | 将本地口播素材制作成经过转写、粗剪审核、字幕或动态图形设计与校验的成片 | Python、Node.js、FFmpeg/FFprobe；完整流程按需使用 WSL2、ChatCut、HyperFrames、GSAP |
| [抖音作品包装师](./skills/03-video/douyin-video-publish-kit/) | 分析待发布视频并生成标题、作品描述、话题标签和实际可用的 9:16 海报封面 | FFmpeg/FFprobe、视频或图像读取能力；制作海报需图像生成或编辑能力 |
| [faceswap](./skills/03-video/faceswap/) | Swap faces in a video using AI via the HeyGen API.… | — |
| [单图生成电商 TVC](./skills/03-video/generate-product-tvc-sd25/) | 从产品参考图生成包含视觉锁定、镜头、声音与连续性约束的 30 秒 Seedance 2.5 广告提示词 | 图片读取能力；直接生成视频需对应平台能力 |
| [黄金结构视频提示词优化器](./skills/03-video/golden-structure-video-prompt-optimizer/) | 将零散创意、剧本或分镜重构为 6+2 黄金结构的视频生成提示词 | 无固定依赖 |
| [linyiyi-singing-video-subtitles](./skills/03-video/linyiyi-singing-video-subtitles/) | 为林依依已有的无字幕演唱视频添加歌名、署名和逐句歌词，测量干声时间轴，归档配套素材并交付… | — |
| [music-to-video](./skills/03-video/music-to-video/) | the user has a music track (an audio file, or a video… | — |
| [playwright-recording](./skills/03-video/playwright-recording/) | Record browser interactions as video using… | — |
| [短剧悬疑感剧本](./skills/03-video/short-drama-suspense-script/) | 为约 60 秒竖屏短剧设计冲突、动作拐点、信息反转和跨镜头一致性 | 无固定依赖；直接生成视频需对应平台能力 |
| [Story Asset Builder](./skills/03-video/story-asset-builder/) | 将剧本拆解为人物、场景、道具、怪兽、载具、色卡、分镜和视频段落资产提示词 | 实际创建画布需要 LibTV Skill/CLI 与 `LIBTV_ACCESS_KEY` 或平台授权 |
| [synthetic-screen-recording](./skills/03-video/synthetic-screen-recording/) | Synthetic terminal-style screen recording guidance… | — |
| [universal-30s-image-to-video](./skills/03-video/universal-30s-image-to-video/) | 通用图生视频时间线规范。把已定稿的静态图片资产转成 30 秒（或 15 秒、5… | — |
| [video-download](./skills/03-video/video-download/) | Download video and audio from YouTube and 1000+ sites… | — |
| [video-edit](./skills/03-video/video-edit/) | Edit videos locally using ffmpeg. Trim, concat,… | — |
| [video-shotcraft](./skills/03-video/video-shotcraft/) | 用镜头配方、Remotion 示例、模板和音频资产制作电影感产品宣传视频 | Node.js、Remotion、FFmpeg；完整资源包较大 |
| [video-toolkit](./skills/03-video/video-toolkit/) | Create professional videos autonomously using… | — |
| [video-translate](./skills/03-video/video-translate/) | Translate and dub existing videos into multiple… | — |
| [video-understand](./skills/03-video/video-understand/) | Understand video content locally using ffmpeg frame… | — |
| [website-to-video](./skills/03-video/website-to-video/) | Capture a general website/URL and turn it into a… | — |
| [中式仙境场景与视频提示词](./skills/03-video/write-seedance-image-video-prompt/) | 批量生成中式仙境图片提示词，或根据成图编写受控的 Seedance 图生视频提示词 | 无固定依赖；图生视频阶段需要读取成图 |

### 04 图像与视觉风格 · 20 个

<sub>生图提示词、视觉母版、产品图与品牌视觉</sub>

| 技能 | 用途 | 依赖 |
|---|------|------|
| [DeepSeek_Visualmodel](./skills/04-image/DeepSeek_Visualmodel/) | 给无原生视觉的大模型（如 DeepSeek）"看图"：把图片路由到外部视觉模型，返回中文文字描述。支持智谱 / Gemini / SiliconFlow / 百炼 4 家视觉服务 | Python 3、requests |
| [bfl-api](./skills/04-image/bfl-api/) | BFL FLUX API integration guide covering endpoints,… | — |
| [朝元神会实拍群像](./skills/04-image/chaoyuan-shenhui-live-action/) | 将人物、神仙群像、天庭朝会或参考图需求扩写为真人实拍质感的生图、局部编辑与视频提示词 | 无固定依赖；参考图模式需要图片读取能力，直接生成或编辑需对应平台能力 |
| [dunhuang-liquid-gold-civilization](./skills/04-image/dunhuang-liquid-gold-civilization/) | 敦煌流金东方幻想文明 / Dunhuang Liquid Gold Civilization… | — |
| [flux-best-practices](./skills/04-image/flux-best-practices/) | Comprehensive guide for BFL FLUX image generation… | — |
| [jiangnan-natural-light-hanfu-cinema](./skills/04-image/jiangnan-natural-light-hanfu-cinema/) | 江南自然光汉服生活电影感 / Jiangnan Natural Hanfu Documentary… | — |
| [历代衣冠](./skills/04-image/lidai-yiguan/) | 生成覆盖先秦至当代的写实人像 AI 绘画提示词，包含服饰形制、发妆、环境、光影和镜头参数 | 无固定依赖；直接出图需所在平台的图像生成能力 |
| [minimal-cold-warm-horizon-lighting](./skills/04-image/minimal-cold-warm-horizon-lighting/) | 极简冷暖交界电影光影美学 / Minimal Cold-Warm Horizon Cinematic… | — |
| [MJV8 中式诗意巨物美学](./skills/04-image/mjv8-chinese-poetic-worlds/) | 将一句话或参考图扩写为中式诗意巨物美学图片提示词，并可依据成图编写短视频动态提示词 | 无固定依赖；直接生成图片或视频需对应平台能力 |
| [oriental-ancient-clear-natural-light](./skills/04-image/oriental-ancient-clear-natural-light/) | 东方古韵清透自然光电影美学 2.1。创建清透淡粉嫩肤色、自然太阳光包裹、东方生活纪录片电影感画面… | — |
| [oriental-underworld-cold-warm-minimal](./skills/04-image/oriental-underworld-cold-warm-minimal/) | 东方幽冥极简冷暖电影美学。以极简空间、单一人物、大面积留白、冷暖渐层、长裙流线为骨架… | — |
| [oriental-wuxia-natural-light-cinema](./skills/04-image/oriental-wuxia-natural-light-cinema/) | 东方自然光武侠电影感 / Oriental Natural Light Wuxia Cinema… | — |
| [电商买家秀](./skills/04-image/photo-scene-replacement/) | 分析产品图的外观、结构和材质分区，并生成保持产品身份、空间可信和组图一致的换景、换手或换色提示词 | 技术标识 `photo-scene-replacement`；可读取图片的模型或环境；直接改图时需图片编辑工具 |
| [pose-library-design](./skills/04-image/pose-library-design/) | Design reusable 2D character pose libraries, action… | — |
| [product-analysis-master](./skills/04-image/product-analysis-master/) | 产品分析母版（中文名：产品分析母版 / Product Analysis Master）… | — |
| [product-photo-retouch](./skills/04-image/product-photo-retouch/) | 实拍产品图精修/重渲染提示词生成器。当用户上传产品实拍图（手机壳、数码配件、包装商品等）并要求"精修 /… | — |
| [visual-style](./skills/04-image/visual-style/) | Create, extract, and apply portable visual design… | — |
| [wuzhou-visual-system](./skills/04-image/wuzhou-visual-system/) | Design and review a consistent Wu Zhou dynasty visual… | — |
| [xiaohongshu-3c-brand-visual](./skills/04-image/xiaohongshu-3c-brand-visual/) | 面向 3C 数码配件（手机壳、支架、充电器、磁吸配件）品牌的小红书图片视觉方案生成器，基于… | — |
| [簪花女郎](./skills/04-image/zanhua-nulang/) | 将人物设想或参考图扩写为簪花冠饰、金青重工织物、花影逆光和电影近景的中式幻想人像提示词 | 无固定依赖；参考图模式需要图片读取能力，直接生成或编辑需对应平台能力 |

### 05 语音与音频 · 11 个

<sub>TTS、ASR、音乐生成与音效</sub>

| 技能 | 用途 | 依赖 |
|---|------|------|
| [acestep](./skills/05-audio/acestep/) | AI music generation with ACE-Step 1.5 — background… | — |
| [azure-speech-to-text](./skills/05-audio/azure-speech-to-text/) | Transcribe audio to text using Azure AI Speech (Fast… | — |
| [doubao-tts](./skills/05-audio/doubao-tts/) | Generate Mandarin and multilingual narration with… | — |
| [elevenlabs](./skills/05-audio/elevenlabs/) | Generate AI voiceovers, sound effects, and music… | — |
| [lyria](./skills/05-audio/lyria/) | Generate and validate music with Google Lyria 3… | — |
| [music](./skills/05-audio/music/) | Generate music using ElevenLabs Music API. Use when… | — |
| [sound-effects](./skills/05-audio/sound-effects/) | Generate sound effects from text descriptions using… | — |
| [speech-to-text](./skills/05-audio/speech-to-text/) | Transcribe audio to text using ElevenLabs Scribe v2.… | — |
| [text-to-speech](./skills/05-audio/text-to-speech/) | Generate speech audio from text using HeyGen's… | — |
| [yichen-asr](./skills/05-audio/yichen-asr/) | 逸尘自用的统一音视频转写入口，在 StepFun Step ASR 与火山引擎豆包 ASR… | — |
| [yichen-volc-asr](./skills/05-audio/yichen-volc-asr/) | 火山引擎音视频转写 + 口播自动粗剪 skill。用于语音转文字、视频转文字、音频识别、生成时间戳/SRT… | — |

### 06 AI 平台接入 · 10 个

<sub>模型与云服务 API 的调用适配</sub>

| 技能 | 用途 | 依赖 |
|---|------|------|
| [comfyui](./skills/06-ai-platforms/comfyui/) | working with ComfyUI workflows in OpenMontage,… | — |
| [comfyui-model-ops](./skills/06-ai-platforms/comfyui-model-ops/) | ComfyUI 模型运维——下载/校验大模型文件、判断模型是否真正被 ComfyUI… | — |
| [dashscope](./skills/06-ai-platforms/dashscope/) | DashScope (Alibaba Cloud Bailian / 阿里云百炼) integration… | — |
| [gemini-omni](./skills/06-ai-platforms/gemini-omni/) | Generate and conversationally edit short videos with… | — |
| [grok-media](./skills/06-ai-platforms/grok-media/) | xAI Grok image and video generation guide covering… | — |
| [heygen](./skills/06-ai-platforms/heygen/) | [DEPRECATED] Use `create-video` for prompt-based… | — |
| [kling-official](./skills/06-ai-platforms/kling-official/) | Official Kling direct API guidance for OpenMontage… | — |
| [ltx2](./skills/06-ai-platforms/ltx2/) | AI video generation with LTX-2.3 22B — text-to-video,… | — |
| [media-use](./skills/06-ai-platforms/media-use/) | Agent Media OS — resolve any media need (BGM, SFX,… | — |
| [seedance-2-0](./skills/06-ai-platforms/seedance-2-0/) | Generate cinematic clips with ByteDance Seedance 2.0… | — |

### 07 内容运营 · 17 个

<sub>研究、采集、归档与多平台发布（yichen 系列）</sub>

| 技能 | 用途 | 依赖 |
|---|------|------|
| [yichen-agent-memory](./skills/07-content-ops/yichen-agent-memory/) | Install, upgrade, inspect, and maintain the public… | — |
| [yichen-bookmarks-export](./skills/07-content-ops/yichen-bookmarks-export/) | 在用户当轮明确授权后，只读导出其小红书收藏、抖音收藏或 X/Twitter 书签为本地链接文件，复用现有… | — |
| [yichen-chatgpt-web-research](./skills/07-content-ops/yichen-chatgpt-web-research/) | Use the user's already signed-in official ChatGPT… | — |
| [yichen-content-archive](./skills/07-content-ops/yichen-content-archive/) | 读取、下载并归档用户已提供的普通网页、Twitter/X 推文与 Article、小红书、抖音、微信公众号、… | — |
| [yichen-jianying-editor](./skills/07-content-ops/yichen-jianying-editor/) | 当用户让 Codex 操作剪映/CapCut 桌面端、导入视频/音频素材、把素材放入时间线、在剪映内手动剪辑… | — |
| [yichen-mac-wechat-dual-open](./skills/07-content-ops/yichen-mac-wechat-dual-open/) | Create, inspect, repair, and polish a second WeChat… | — |
| [yichen-social-bookmarks-exporter](./skills/07-content-ops/yichen-social-bookmarks-exporter/) | 批量导出小红书、抖音与 X/Twitter 的私人收藏或书签为本地链接文件，支持 Chrome… | — |
| [yichen-summary](./skills/07-content-ops/yichen-summary/) | 将当前对话的精华内容提取并保存到 Obsidian。触发条件：用户说… | — |
| [yichen-unified-search](./skills/07-content-ops/yichen-unified-search/) | 逸尘自用的统一网页与社交平台搜索编排器。用于关键词驱动的实时公共网页检索、并行批量搜索、金融/学术/法律/安… | — |
| [yichen-video-content](./skills/07-content-ops/yichen-video-content/) | 对标视频内容拆解。输入视频口播稿，输出逐句作用拆解 + 问题诊断 + 可模仿报告。… | — |
| [yichen-web-research](./skills/07-content-ops/yichen-web-research/) | 逸尘自用的互联网研究总入口。用于跨平台且跨阶段，或用户尚未确定工具的研究任务… | — |
| [yichen-wechat-local-vault](./skills/07-content-ops/yichen-wechat-local-vault/) | 微信 Mac 4.x 本地数据库全量/增量解析与数字资产库。用于本机微信聊天记录、联系人、群聊、朋友圈、收藏… | — |
| [yichen-wechat-mp-batch-exporter](./skills/07-content-ops/yichen-wechat-mp-batch-exporter/) | 批量下载微信公众号文章正文、历史文章列表、原创文章筛选、历史计数口径、阅读量、点赞/转发等指标、评论和评论回… | — |
| [yichen-wecom-local-vault](./skills/07-content-ops/yichen-wecom-local-vault/) | Read, decrypt, query, search, and export local… | — |
| [yichen-wecom-operations](./skills/07-content-ops/yichen-wecom-operations/) | 企业微信官方 wecom-cli 操作入口。用于把本地 Markdown… | — |
| [yichen-x-article-draft-uploader](./skills/07-content-ops/yichen-x-article-draft-uploader/) | 将 Obsidian 或本地 Markdown 文章上传到 X/Twitter Articles 草稿… | — |
| [yichen-x-slicer](./skills/07-content-ops/yichen-x-slicer/) | Convert a public X/Twitter Post, Quote Post, or… | — |

### 08 工具与规范指南 · 11 个

<sub>工程工具、配置规范与 Skill 编写指南</sub>

| 技能 | 用途 | 依赖 |
|---|------|------|
| [agent-definition-guide](./skills/08-toolkit-guides/agent-definition-guide/) | 创建、修改、删除或排查 DeterminFlow Agent Definition 时必须加载此技能… | — |
| [agents](./skills/08-toolkit-guides/agents/) | Build voice AI agents with ElevenLabs. Use when… | — |
| [automation-guide](./skills/08-toolkit-guides/automation-guide/) | 创建、查看、更新、暂停、恢复、立即运行、删除或排查 DeterminFlow Cron… | — |
| [codex-local-plugin-install](./skills/08-toolkit-guides/codex-local-plugin-install/) | 把第三方 GitHub 仓库作为本地插件安装进本机 Codex（桌面端/CLI），包括本地… | — |
| [ffmpeg](./skills/08-toolkit-guides/ffmpeg/) | Video and audio processing with FFmpeg. Use for… | — |
| [prompt-template-guide](./skills/08-toolkit-guides/prompt-template-guide/) | 查看、创建、修改、删除或排查 DeterminFlow Prompt Template 与 system… | — |
| [script-library-guide](./skills/08-toolkit-guides/script-library-guide/) | 创建、更新、删除、引用或排查 DeterminFlow Script Library 脚本时必须加载此技能… | — |
| [setup-api-key](./skills/08-toolkit-guides/setup-api-key/) | Guides users through setting up an ElevenLabs API key… | — |
| [skill-rule-authoring-guide](./skills/08-toolkit-guides/skill-rule-authoring-guide/) | 创建、更新、修补、删除、分组或排查 DeterminFlow Skill 与 Rule 时必须加载此技能… | — |
| [topic-auto-title](./skills/08-toolkit-guides/topic-auto-title/) | WorkBuddy 话题标题自动命名。按固定「emoji 对象｜目标」规范持续更新当前会话标题… | — |
| [workflow-guide](./skills/08-toolkit-guides/workflow-guide/) | 创建、编辑、校验、运行或排查 DeterminFlow 工作流时必须先加载此技能… | — |

## 我的自建技能

以下 16 个技能由本仓库维护者原创维护，覆盖东方美学提示词、产品视觉、程序化视频与工作流工具，与第三方收录内容分开管理。

| 技能 | 分类 | 用途 |
|---|---|---|
| [dunhuang-liquid-gold-civilization](./skills/04-image/dunhuang-liquid-gold-civilization/) | `skills/04-image/` | 敦煌流金东方幻想文明 / Dunhuang Liquid Gold Civilization… |
| [jiangnan-natural-light-hanfu-cinema](./skills/04-image/jiangnan-natural-light-hanfu-cinema/) | `skills/04-image/` | 江南自然光汉服生活电影感 / Jiangnan Natural Hanfu Documentary Cinema… |
| [minimal-cold-warm-horizon-lighting](./skills/04-image/minimal-cold-warm-horizon-lighting/) | `skills/04-image/` | 极简冷暖交界电影光影美学 / Minimal Cold-Warm Horizon Cinematic Lighting… |
| [oriental-ancient-clear-natural-light](./skills/04-image/oriental-ancient-clear-natural-light/) | `skills/04-image/` | 东方古韵清透自然光电影美学 2.1。创建清透淡粉嫩肤色、自然太阳光包裹、东方生活纪录片电影感画面，并输出可直接粘贴的… |
| [oriental-underworld-cold-warm-minimal](./skills/04-image/oriental-underworld-cold-warm-minimal/) | `skills/04-image/` | 东方幽冥极简冷暖电影美学。以极简空间、单一人物、大面积留白、冷暖渐层、长裙流线为骨架… |
| [oriental-wuxia-natural-light-cinema](./skills/04-image/oriental-wuxia-natural-light-cinema/) | `skills/04-image/` | 东方自然光武侠电影感 / Oriental Natural Light Wuxia Cinema Style… |
| [wuzhou-visual-system](./skills/04-image/wuzhou-visual-system/) | `skills/04-image/` | Design and review a consistent Wu Zhou dynasty visual system… |
| [product-analysis-master](./skills/04-image/product-analysis-master/) | `skills/04-image/` | 产品分析母版（中文名：产品分析母版 / Product Analysis Master）… |
| [product-photo-retouch](./skills/04-image/product-photo-retouch/) | `skills/04-image/` | 实拍产品图精修/重渲染提示词生成器。当用户上传产品实拍图（手机壳、数码配件、包装商品等）并要求"精修 / 修图 /… |
| [photo-scene-replacement](./skills/04-image/photo-scene-replacement/) | `skills/04-image/` | 用户上传产品白底图、实拍图、多角度商品图或买家秀时，自动分析并总结产品外观、结构、配色、材质观感、标识及细节依据… |
| [xiaohongshu-3c-brand-visual](./skills/04-image/xiaohongshu-3c-brand-visual/) | `skills/04-image/` | 面向 3C 数码配件（手机壳、支架、充电器、磁吸配件）品牌的小红书图片视觉方案生成器，基于… |
| [remotion-vox](./skills/02-animation/remotion-vox/) | `skills/02-animation/` | 用 Remotion(React 代码生成视频)做 Vox 风格解说/特效片——锁定背景 + 黑白半调 cutout 弹入… |
| [universal-30s-image-to-video](./skills/03-video/universal-30s-image-to-video/) | `skills/03-video/` | 通用图生视频时间线规范。把已定稿的静态图片资产转成 30 秒（或 15 秒、5… |
| [comfyui-model-ops](./skills/06-ai-platforms/comfyui-model-ops/) | `skills/06-ai-platforms/` | ComfyUI 模型运维——下载/校验大模型文件、判断模型是否真正被 ComfyUI 识别、按底模架构修正工作流参数… |
| [codex-local-plugin-install](./skills/08-toolkit-guides/codex-local-plugin-install/) | `skills/08-toolkit-guides/` | 把第三方 GitHub 仓库作为本地插件安装进本机 Codex（桌面端/CLI），包括本地 marketplace… |
| [topic-auto-title](./skills/08-toolkit-guides/topic-auto-title/) | `skills/08-toolkit-guides/` | WorkBuddy 话题标题自动命名。按固定「emoji 对象｜目标」规范持续更新当前会话标题，让任务列表一眼可辨… |
## 安装方法

### 方式一：复制技能目录

把所需技能目录（例如 `skills/01-ui-frontend/brandkit/`、`skills/01-ui-frontend/canvas-ui/` 或 `skills/01-ui-frontend/liquid-glass-react/`）整个复制到你的技能目录：

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
python "skills/04-image/DeepSeek_Visualmodel/eyes.py" "图片.png" --prompt "这张图里写了什么？"

# 指定视觉服务商（Gemini 更强、SiliconFlow 适合文字提取）
python "skills/04-image/DeepSeek_Visualmodel/eyes.py" "图片.png" --prompt "详细描述这张截图" --provider gemini
python "skills/04-image/DeepSeek_Visualmodel/eyes.py" "图片.png" --prompt "提取图中所有文字" --provider siliconflow
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
用抖音作品包装师分析这个视频并生成标题、描述、标签和 9:16 海报封面
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

**维护者原创（16 个）**：`dunhuang-liquid-gold-civilization`、`jiangnan-natural-light-hanfu-cinema`、`minimal-cold-warm-horizon-lighting`、`oriental-ancient-clear-natural-light`、`oriental-underworld-cold-warm-minimal`、`oriental-wuxia-natural-light-cinema`、`wuzhou-visual-system`、`product-analysis-master`、`product-photo-retouch`、`photo-scene-replacement`、`xiaohongshu-3c-brand-visual`、`remotion-vox`、`universal-30s-image-to-video`、`comfyui-model-ops`、`codex-local-plugin-install`、`topic-auto-title`，均位于 `skills/04-image/`、`skills/02-animation/`、`skills/03-video/`、`skills/06-ai-platforms/`、`skills/08-toolkit-guides/` 下，采用 MIT License。

**早期收录**：


- `lidai-yiguan`（历代衣冠）：由本仓库维护者 [LightyearXizIl](https://github.com/LightyearXizIl) 原创，采用 MIT License。
- `remotion-vox`（VoxMotion 自动剪辑）：由本仓库维护者 [LightyearXizIl](https://github.com/LightyearXizIl) 原创，采用 MIT License。
- `chaoyuan-shenhui-live-action`（朝元神会实拍群像）：由本仓库维护者 [LightyearXizIl](https://github.com/LightyearXizIl) 编写，采用 MIT License；风格基准仅归纳公开参考视频的视觉语法，不收录或再分发视频及其中素材。
- `zanhua-nulang`（簪花女郎）：由本仓库维护者 [LightyearXizIl](https://github.com/LightyearXizIl) 编写，采用 MIT License；风格基准来自用户提供的 9 张本地教程截图的独立视觉归纳，不收录、分发或逐字复制原截图内容，当前素材无法可靠确认的作者和原始链接不作猜测。
- `douyin-video-publish-kit`（抖音作品包装师）：由本仓库维护者 [LightyearXizIl](https://github.com/LightyearXizIl) 编写，采用 MIT License。

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
