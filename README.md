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
```

## 第三方来源与授权

- `finesse-ui`：来源于 [zhenwusw/finesse-skill](https://github.com/zhenwusw/finesse-skill)，技能主体采用 MIT License；其示例中附带的 GSAP/ScrollTrigger 文件遵循文件头标注的 [GreenSock Standard License](https://gsap.com/standard-license/)。
- `web-clone`：来源于 [Jane-xiaoer/claude-skill-web-clone](https://github.com/Jane-xiaoer/claude-skill-web-clone)，采用 MIT License。
- `astryx`：适配自 [facebook/astryx](https://github.com/facebook/astryx) 的官方 Agent/Claude 指令与文档，保留 Meta 的 MIT License；当前快照为 `077087f68d5e5fc12b39218a67dfa6a29fa04bcd`。
- `brandkit`：原样安装自 [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) 的 `skills/brandkit`，采用 MIT License；当前快照为 `e988add20dab0fa97d7a76781c48961c8184288e`。
- `canvas-ui`：面向 [DavidHDev/canvas-ui](https://github.com/DavidHDev/canvas-ui) 创建的安全适配 Skill，固定参考快照 `81b65e159c63bde7167b9b4b458a775838e4cd39`。上游采用 MIT + Commons Clause，禁止将其组件本身出售、再许可或再分发；本合集只保留官方文档快照和安装工作流，不复制组件源码。
- `svg-logo-designer`：参考 [rknall/claude-skills](https://github.com/rknall/claude-skills) 中同名功能重新独立编写。检查时上游未提供明确许可证，因此没有复制或再分发其原始 Skill 内容；本合集版本采用独立 MIT License。
- `uiverse-galaxy`：面向 [uiverse-io/galaxy](https://github.com/uiverse-io/galaxy) 创建的适配 Skill，保留上游 MIT License 和 README 快照；当前快照为 `adbd2adde0a299a3956ea288fb444ec01891ca41`。
- `liquid-glass-react`：面向 [rdev/liquid-glass-react](https://github.com/rdev/liquid-glass-react) 创建的适配 Skill，保留上游 MIT License、README 和包信息快照；当前快照为 `ac48eab18d1f7f444ae30002d240cae29c863a21`。

各技能目录内的独立许可证和归属说明优先适用于相应第三方内容。

## 新增技能规范

往本合集添加新技能时请遵守：

1. 每个技能一个目录，目录名即技能名，含 `SKILL.md`（frontmatter 必须带 `name` + `description`）
2. 目录内必须有 `README.md`：说明**这个技能是干嘛的**、使用方法、所需 API key 及配置方式
3. **禁止包含任何 API key、token、密码**——一律通过环境变量注入
4. 依赖保持轻量（标准库 + `requests` 级别），Python 3 可运行

## License

MIT
