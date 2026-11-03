# fixing-motion-performance

来自 [ibelick/ui-skills](https://github.com/ibelick/ui-skills) 的动画性能审查与修复 Skill，聚焦布局抖动、滚动驱动、合成层、滤镜、模糊和无停止条件的动画循环。

## 使用

```text
用 fixing-motion-performance 修复这个页面的动画卡顿
审查这个滚动动画是否触发布局和重绘
```

它优先选择 `transform` 和 `opacity`，要求批量读取/写入布局并限制昂贵滤镜；不会在未授权时迁移动画库。

## 依赖与密钥

- 不需要 API key。
- 性能结论最好通过目标浏览器的 Performance、Layers 等工具实测。

## 来源与许可

固定来源提交：`2b3a114a3fcff079d73639a21710c595d4700a74`。采用目录内的 MIT License。
