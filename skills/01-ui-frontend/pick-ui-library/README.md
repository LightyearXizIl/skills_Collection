# pick-ui-library

来自 [emilkowalski/skills](https://github.com/emilkowalski/skills) 的 UI 库选择 Skill，根据维护者的精选清单为数字、OTP、图表、命令菜单、虚拟列表、拖放、Toast、状态和样式等任务选择库。

## 使用

```text
显式使用 pick-ui-library 为这个项目选择 Toast 库
用 pick-ui-library 推荐适合大量列表的虚拟化方案
```

该 Skill 只允许显式调用。候选库的版本、维护状态和项目兼容性会变化，实际安装前必须检查当前官方资料。

## 兼容修正

上游 `disable-model-invocation: true` 已等价迁移为 `agents/openai.yaml` 中的 `policy.allow_implicit_invocation: false`，正文未改。

## 依赖、密钥与许可

不需要 API key；核对当前库状态时需要网络。固定上游提交 `de33dbed000212b54400a33767d1e4d03654db2a`，采用目录内 MIT License。
