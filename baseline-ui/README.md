# baseline-ui

来自 [ibelick/ui-skills](https://github.com/ibelick/ui-skills) 的快速 UI 基线 Skill，用一套明确规则清理常见的间距、层级、字体、布局、交互和动画问题。

## 使用

```text
用 baseline-ui 清理这个页面的视觉和布局问题
用 baseline-ui 审查 src/components/Dashboard.tsx
```

它优先沿用项目已有组件和 Token，并对 Tailwind、交互原语和动画方式给出较强约束。应用规则前应先确认项目技术栈；不要为了满足规则擅自迁移框架。

## 依赖与密钥

- Skill 本身不需要 API key。
- 具体修改依赖当前项目的前端技术栈；涉及 JavaScript 动画时，上游规则优先使用 `motion/react`。

## 来源与许可

固定来源提交：`2b3a114a3fcff079d73639a21710c595d4700a74`。采用目录内的 MIT License。
