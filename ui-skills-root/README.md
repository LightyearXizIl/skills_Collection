# ui-skills-root

来自 [ibelick/ui-skills](https://github.com/ibelick/ui-skills) 的 UI Skill 路由入口。它先判断任务类别，再通过官方 CLI 选择最小可用 Skill 集，通常只加载一个，最多三个。

## 使用

```text
用 ui-skills-root 为这个 UI 任务选择最合适的专项 Skill
```

常用命令：

```bash
npx ui-skills start
npx ui-skills categories
npx ui-skills list --category motion
npx ui-skills get baseline-ui
```

## 依赖与密钥

- 不需要 API key。
- 需要 Node.js/npm；`npx ui-skills` 会访问上游当前 Skill registry。

## 来源与许可

固定来源提交：`2b3a114a3fcff079d73639a21710c595d4700a74`。采用目录内的 MIT License。
