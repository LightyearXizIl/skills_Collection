# improve-ui

来自 [ibelick/ui-skills](https://github.com/ibelick/ui-skills) 的只读 UI 审计 Skill。它依据产品真实设计证据寻找最多三个可证明的问题，并为用户选中的问题编写独立实施计划。

## 使用

```text
用 improve-ui 审查这个产品的主要工作台
为我选中的第 1 个问题生成实施计划
```

该 Skill 不直接修改产品源码，只能在 `design-plans/` 下创建或更新计划；如果用户直接要求修复，它仍应先给计划而不是实施。

## 依赖与密钥

- 不需要 API key。
- 只有用户提供渲染证据或明确要求视觉检查时，才使用浏览器证据。

## 来源与许可

固定来源提交：`2b3a114a3fcff079d73639a21710c595d4700a74`。采用目录内的 MIT License。
