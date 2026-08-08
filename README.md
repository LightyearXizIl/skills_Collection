# skills_Collection — AI 技能合集

一个面向 **Reasonix / Claude Code** 等 AI 编码助手的**技能（Skill）合集**。每个技能是一个独立目录，包含 `SKILL.md`（技能定义）、运行脚本和 `README.md`（用途与配置说明）。

> **安全声明：本合集不包含任何 API key / token / 密钥**，所有密钥由使用者自行申请并通过环境变量注入。

## 技能清单

| 技能 | 用途 | 依赖 |
|------|------|------|
| [DeepSeek_Visualmodel](./DeepSeek_Visualmodel/) | 给无原生视觉的大模型（如 DeepSeek）"看图"：把图片路由到外部视觉模型，返回中文文字描述。支持智谱 / Gemini / SiliconFlow / 百炼 4 家视觉服务 | Python 3、requests |

## 安装方法

### 方式一：复制技能目录

把技能目录（如 `DeepSeek_Visualmodel/`）整个复制到你的技能目录：

- **Reasonix 项目级**：`<工作区>/.reasonix/skills/`
- **Reasonix 全局**：`%AppData%/reasonix/skills/`（或 `<Reasonix home>/skills/`）
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

## 新增技能规范

往本合集添加新技能时请遵守：

1. 每个技能一个目录，目录名即技能名，含 `SKILL.md`（frontmatter 必须带 `name` + `description`）
2. 目录内必须有 `README.md`：说明**这个技能是干嘛的**、使用方法、所需 API key 及配置方式
3. **禁止包含任何 API key、token、密码**——一律通过环境变量注入
4. 依赖保持轻量（标准库 + `requests` 级别），Python 3 可运行

## License

MIT
