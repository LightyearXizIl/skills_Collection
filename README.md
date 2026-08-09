# skills_Collection — AI 技能合集

一个面向 **Codex / Reasonix / Claude Code** 等 AI 编码助手的**技能（Skill）合集**。每个技能是一个独立目录，包含 `SKILL.md`（技能定义）、运行脚本和 `README.md`（用途与配置说明）。

> **安全声明：本合集不包含任何 API key / token / 密钥**，所有密钥由使用者自行申请并通过环境变量注入。

## 技能清单

| 技能 | 用途 | 依赖 |
|------|------|------|
| [DeepSeek_Visualmodel](./DeepSeek_Visualmodel/) | 给无原生视觉的大模型（如 DeepSeek）"看图"：把图片路由到外部视觉模型，返回中文文字描述。支持智谱 / Gemini / SiliconFlow / 百炼 4 家视觉服务 | Python 3、requests |
| [finesse-ui](./finesse-ui/) | 构建和审查高完成度 Web 界面，覆盖品牌站、产品后台、数据可视化与电商页面，并提供可复用示例和设计检查规则 | Node.js（检测脚本）；具体项目的前端技术栈 |
| [web-clone](./web-clone/) | 网站复刻与逆向分析方法论：优先获取真实源码，覆盖静态站、React/Vue/Next、多页面及 WebGL/Canvas 重前端站点 | Node.js；Playwright/浏览器及 wget、gh 等按任务选用工具 |

## 安装方法

### 方式一：复制技能目录

把所需技能目录（如 `DeepSeek_Visualmodel/`、`finesse-ui/` 或 `web-clone/`）整个复制到你的技能目录：

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
```

## 第三方来源与授权

- `finesse-ui`：来源于 [zhenwusw/finesse-skill](https://github.com/zhenwusw/finesse-skill)，技能主体采用 MIT License；其示例中附带的 GSAP/ScrollTrigger 文件遵循文件头标注的 [GreenSock Standard License](https://gsap.com/standard-license/)。
- `web-clone`：来源于 [Jane-xiaoer/claude-skill-web-clone](https://github.com/Jane-xiaoer/claude-skill-web-clone)，采用 MIT License。

各技能目录内的独立许可证和归属说明优先适用于相应第三方内容。

## 新增技能规范

往本合集添加新技能时请遵守：

1. 每个技能一个目录，目录名即技能名，含 `SKILL.md`（frontmatter 必须带 `name` + `description`）
2. 目录内必须有 `README.md`：说明**这个技能是干嘛的**、使用方法、所需 API key 及配置方式
3. **禁止包含任何 API key、token、密码**——一律通过环境变量注入
4. 依赖保持轻量（标准库 + `requests` 级别），Python 3 可运行

## License

MIT
