# fixing-metadata

来自 [ibelick/ui-skills](https://github.com/ibelick/ui-skills) 的网页元数据审查与修复 Skill，覆盖标题、描述、canonical、robots、Open Graph、Twitter Card、图标、manifest 和 JSON-LD。

## 使用

```text
用 fixing-metadata 审查这个网站的 SEO 和分享卡片
修复新页面的 canonical、Open Graph 和 robots 设置
```

应遵循项目现有的元数据实现方式，避免重复标签和无关框架迁移；结构化数据只能描述页面真实呈现的内容。

## 兼容修正

上游 `SKILL.md` 的顶层 `version: 1.0.1` 不符合当前 Codex Skill frontmatter 校验规则。本地版本只将它移入 `metadata.version`，正文与其余上游字段保持不变。

## 依赖与密钥

- 不需要 API key。
- 验证分享卡片时需要可访问的真实 URL；不能用 localhost 代替上线结果。

## 来源与许可

固定来源提交：`2b3a114a3fcff079d73639a21710c595d4700a74`。采用目录内的 MIT License。
