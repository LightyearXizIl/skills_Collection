# canvas-ui

将 [DavidHDev/canvas-ui](https://github.com/DavidHDev/canvas-ui) 的官方文档适配为 Codex Skill，用于选择、安装、定制和验证 Canvas UI 的 WebGL、流体、玻璃、粒子、着色器与 3D 效果。

## 使用

```text
用 canvas-ui 给这个 React Hero 加 Liquid 效果
选择一个适合产品页的 Canvas UI 组件并验证降级体验
修复 Canvas UI 在 Safari/Firefox 中的兼容问题
```

技能会根据当前项目框架，从官方 shadcn 兼容 registry 获取组件；不会在技能目录中重复保存组件源码。

## 依赖与密钥

- 技能本身不需要 API key 或 token。
- 实际组件依赖由官方 registry 和所选框架决定。
- 完整 HTML-in-canvas 效果目前依赖实验性浏览器能力，其他环境应验证 WebGL fallback。

## 来源与许可证

- 官方仓库快照：`DavidHDev/canvas-ui@81b65e159c63bde7167b9b4b458a775838e4cd39`
- 上游许可证：MIT + Commons Clause，见 `LICENSE.md`
- 许可证允许在应用、网站或产品中使用，但禁止销售、再许可或重新分发组件本体。
- 本技能仅包含适配指令和官方 `llms.txt` 快照，不包含 Canvas UI 组件源码。
