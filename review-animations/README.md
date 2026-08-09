# review-animations

来自 [emilkowalski/skills](https://github.com/emilkowalski/skills) 的严格动画代码评审 Skill，按照 Emil Kowalski 的设计工程标准检查单个动画或相关差异，并默认指出问题，达标后才通过。

## 使用

```text
显式使用 review-animations 评审这个弹窗动效的代码
用 review-animations 检查这次动画改动是否达到上线标准
```

该 Skill 只评审动画，不实现功能或审查无关代码；详细规则位于 `STANDARDS.md`。

## 兼容修正

上游 `disable-model-invocation: true` 已等价迁移为 `agents/openai.yaml` 中的 `policy.allow_implicit_invocation: false`，正文未改。

## 依赖、密钥与许可

不需要 API key；依赖待评审源码，必要时结合浏览器证据。固定上游提交 `de33dbed000212b54400a33767d1e4d03654db2a`，采用目录内 MIT License。
