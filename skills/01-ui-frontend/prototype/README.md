# prototype

来自 [emilkowalski/skills](https://github.com/emilkowalski/skills) 的多方案 UI 原型 Skill，为同一个界面构建真正不同的可运行版本，并放进可视化选择器中逐个比较和选定。

## 使用

```text
显式使用 prototype 做四种不同的 Toast 交互方案
用 prototype 为定价卡片创建多个可切换的真实版本
```

该 Skill 只允许显式调用，并会读取 `PICKER.md`。它不是静态概念图工具；应沿用项目现有技术栈并验证每个变体。

## 兼容修正

上游 `disable-model-invocation: true` 已等价迁移为 `agents/openai.yaml` 中的 `policy.allow_implicit_invocation: false`，正文未改。

## 依赖、密钥与许可

不需要 API key；依赖项目技术栈和浏览器验证。固定上游提交 `de33dbed000212b54400a33767d1e4d03654db2a`，采用目录内 MIT License。
