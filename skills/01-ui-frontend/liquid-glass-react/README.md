# liquid-glass-react

将 [rdev/liquid-glass-react](https://github.com/rdev/liquid-glass-react) 适配为 Codex Skill，用于在 React 项目中安装、实现、调参与验证 Apple 风格液态玻璃折射效果。

## 使用

```text
用 liquid-glass-react 给这个按钮加液态玻璃效果
让 LiquidGlass 跟随父容器鼠标移动，并保留键盘操作
排查 Safari 和 Firefox 中位移效果缺失的问题
```

## 依赖与兼容性

- 不需要 API key。
- 上游快照要求 React/React DOM 18+。
- 快照包版本为 `1.1.1`，实际使用时以项目锁文件、已安装类型和当前 npm 信息为准。
- 上游明确提示 Safari/Firefox 仅部分支持，位移效果不可见；需要提供并验证降级表现。

## 来源与许可证

- 上游快照：`rdev/liquid-glass-react@ac48eab18d1f7f444ae30002d240cae29c863a21`
- 许可证：MIT，见 `LICENSE`
- 本技能保存官方 README/package.json 快照和 Codex 适配指令，不包含 npm 包源码。
