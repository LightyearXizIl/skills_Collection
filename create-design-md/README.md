# create-design-md

来自 [ibelick/ui-skills](https://github.com/ibelick/ui-skills) 的设计系统提取 Skill，用已有代码仓库或可渲染网站的证据创建、更新 `DESIGN.md`，避免把偶然样式猜成产品规范。

## 使用

```text
用 create-design-md 从这个仓库创建 DESIGN.md
用 create-design-md 根据这个公开网站重建设计语言文档
```

仓库模式只修改项目根目录的 `DESIGN.md`；URL 模式需要真实浏览器检查 DOM、计算样式和公开样式表。输出必须通过 `@google/design.md` 的 lint 与 export 检查。

## 依赖与密钥

- 不需要 API key。
- 需要 Node.js/npm 运行 `npx @google/design.md`。
- URL 模式需要可用的浏览器检查能力。

## 来源与许可

固定来源提交：`2b3a114a3fcff079d73639a21710c595d4700a74`。采用目录内的 MIT License。
