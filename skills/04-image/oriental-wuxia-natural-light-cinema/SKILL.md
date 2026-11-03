---
name: oriental-wuxia-natural-light-cinema
description: "东方自然光武侠电影感 / Oriental Natural Light Wuxia Cinema Style。以真实自然光、低饱和东方电影色、真人演员质感呈现江湖生活状态，而非拍武侠服装。适用于武侠、江湖、女侠、剑客、竹林、山巅云海、孤舟、客栈、酒馆、看剑、武侠纪录片、wuxia natural light cinema。负责静态画面与 Midjourney 提示词；动态时间线转交 universal-30s-image-to-video。"
---

# 东方自然光武侠电影感

Oriental Natural Light Wuxia Cinema Style

核心：**拍的是人物在江湖中的状态，而不是拍武侠服装。**

## 路由

- 需要完整色卡、摄影参数、尾缀与限制清单时，读 [references/style-guide.md](references/style-guide.md)。
- 需要 30 秒/15 秒分镜、运镜、音效时，转交 `$universal-30s-image-to-video`。

## 工作方法

1. **色彩**：低饱和东方电影色——深蓝灰、墨青、浅灰蓝衣料、米白、旧木色、石灰色，配少量暗红作情绪点缀。
2. **光影**：真实自然光，不人工布光。自然阳光、柔和方向光、暖阳光斑、深而真实的自然阴影。
3. **空气感**：清透而非浓雾——`clear natural atmosphere, transparent air, soft humidity, light mist, sunlight particles`。
4. **摄影**：大场景 24mm（山河、孤舟、骑马、巨佛、云海）；中景 35mm（酒馆、竹林舞剑、客栈、江湖生活）；特写 85mm（回眸、看剑、倒酒、眼神）。
5. **设备**：Canon EOS R5 电影摄影——浅景深、自然焦外、电影级焦点分离、Kodak 胶片色彩。
6. **人物**：真人演员而非角色模型——真实中国女演员、真实面部比例、真实皮肤纹理、可见毛孔、自然发丝；姿态自然，非摆拍。
7. **服装材质**：真实布料——棉麻纹理、可见织物纤维、柔软褶皱。避免金丝仙袍、过度华丽盔甲、游戏装备感。
8. **构图**：16:9 电影画幅，人物 30%–40%、环境 60%–70%，强调人与自然的关系。
9. **情绪**：`quiet, solitary, peaceful, nostalgic, restrained, poetic, slow life`。核心是「不是我要赢天下，而是我终于看见自己」。

## 输出规范

先给中文标题，再给一段可直接粘贴的英文 Midjourney 提示词。尾部使用本 skill 标准尾缀，并叠加真人非 CG 限制词。

## 真人非 CG 限制（必须附带）

```text
not CGI, not 3D render, not anime, not illustration, not game art, no plastic skin, no doll face, no waxy skin, no fantasy costume, no studio lighting, no oversaturated colors, no golden filter, no artificial pose
```
