# improve-animations

来自 [emilkowalski/skills](https://github.com/emilkowalski/skills) 的全库动画审计与规划 Skill。它只读检查代码，输出有优先级的发现和可交给其他 Agent 执行的独立计划。

## 使用

```text
用 improve-animations 审计这个应用的全部动效
为优先级最高的动画问题生成实施计划
```

该 Skill 不直接修改产品源码；配套的 `AUDIT.md` 和 `PLAN-TEMPLATE.md` 定义审计及计划格式。

## 依赖、密钥与许可

不需要 API key；依赖可读取的项目源码。固定上游提交 `de33dbed000212b54400a33767d1e4d03654db2a`，采用目录内 MIT License。
