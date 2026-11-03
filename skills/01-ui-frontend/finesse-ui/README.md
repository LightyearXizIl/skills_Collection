# finesse-ui

面向 AI 编码助手的高完成度 Web UI 设计与审查技能。它按页面用途区分品牌展示、产品界面和电商界面，提供设计决策流程、反廉价检查清单、数据可视化规则、动效方案以及可运行的 HTML 示例。

## 适用场景

- 落地页、品牌站、发布页、作品集和 Hero 页面
- Dashboard、管理后台、数据表格、分析界面和设置页
- 商品详情页、商品列表、购物车和结算页
- 对现有页面执行审查、重设计、增强动效或提高信息密度

## 使用方法

将整个 `finesse-ui/` 目录复制到 AI 编码助手的技能目录，然后使用自然语言触发，例如：

```text
用 finesse-ui 做一个高级感的 SaaS 落地页
用 finesse-ui 审查当前 Dashboard
用 finesse-ui redesign 这个商品详情页
```

技能也支持 `audit`、`bolder`、`quieter`、`soul`、`animate`、`depth`、`densify` 和 `redesign` 等定向命令。完整工作流和触发规则见 `SKILL.md`。

## 目录说明

- `SKILL.md`：技能入口和完整工作流
- `references/`：设计规范、动效、数据可视化、电商界面与交付检查资料
- `examples/`：品牌页和产品界面示例
- `scripts/detect.mjs`：页面模式检测脚本

## 依赖与 API Key

- 技能本身不需要 API key、token 或密码。
- `scripts/detect.mjs` 需要 Node.js。
- 具体页面可能按方案使用 Three.js、GSAP、Canvas 或项目原有前端框架；是否联网加载资源取决于实际项目和示例文件。

## 来源与许可证

- 当前收录版本：`0.10.0`（以 `SKILL.md` frontmatter 为准）
- 安装来源：[zhenwusw/finesse-skill](https://github.com/zhenwusw/finesse-skill)（该仓库注明 fork 自 `mouse-lin/finesse-skill`）
- 技能主体：MIT License，见 `LICENSE`
- `examples/lib/gsap.min.js` 与 `examples/lib/ScrollTrigger.min.js`：Copyright GreenSock，遵循其文件头标注的 [GreenSock Standard License](https://gsap.com/standard-license/)

转载、修改或再发布时，请保留对应版权和许可证声明。
