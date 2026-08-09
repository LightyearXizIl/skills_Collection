# astryx

将 Meta 的 Astryx 设计系统工作流适配为 Codex 标准 Skill。它指导 AI 在 React 19+ 项目中安装和使用 Astryx，通过项目实际安装的 CLI 查询组件、模板、设计原则、Token 和主题 API，也覆盖 Astryx 上游组件、主题与结构化文档贡献流程。

## 使用方法

该技能已安装到 Codex 全局技能目录。新对话中可直接使用：

```text
用 astryx 做一个无障碍 React 管理后台
用 astryx 创建一个品牌主题
查询 Astryx DataTable 的真实 API 后实现页面
在 facebook/astryx 中新增组件并补齐文档
```

## 内容

- `SKILL.md`：Codex 入口、CLI 优先工作流和验证要求
- `agents/openai.yaml`：Codex 界面元数据
- `references/`：来自官方仓库的组件创建、主题创建、组件文档、密集压缩协议和上游项目规范
- `LICENSE`：Astryx 官方 MIT License

## 依赖与密钥

- 技能本身不需要 API key、token 或密码。
- 消费端项目需要 React 19+；实际使用时通常安装 `@astryxdesign/core`、一个 Astryx 主题、`@stylexjs/stylex` 和开发依赖 `@astryxdesign/cli`。
- 具体依赖版本应由项目锁文件和当前 npm 包确定，不在技能中写死。

## 来源与授权

- 官方仓库：https://github.com/facebook/astryx
- 本次参考快照：`facebook/astryx@077087f68d5e5fc12b39218a67dfa6a29fa04bcd`
- 上游提交时间：2026-08-08 01:24:42 UTC
- 许可证：MIT，Copyright (c) 2026 Meta Platforms, Inc.

`SKILL.md` 是为 Codex 编写的适配层；`references/` 与 `LICENSE` 保留官方来源和授权。Astryx 仍处于 Beta，组件 API 和 CLI 可能变化，执行任务时应优先查询项目当前安装版本的 CLI。
