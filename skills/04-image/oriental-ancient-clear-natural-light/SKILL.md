---
name: oriental-ancient-clear-natural-light
description: "东方古韵清透自然光电影美学 2.1。创建清透淡粉嫩肤色、自然太阳光包裹、东方生活纪录片电影感画面，并输出可直接粘贴的 Midjourney 提示词。适用于东方古韵、清透自然光、淡粉嫩肤色、江南村落、古村日常、汉服生活纪录、生活化古风、纪录片电影感、translucent soft pink skin tone、Eastern ancient life documentary cinema。负责静态图像风格与提示词；时间线、运镜、对白等动态部分请转交 universal-30s-image-to-video。"
---

# 东方古韵清透自然光电影美学 2.1

Eastern Ancient Life Clear Natural Light Cinema Style

核心：真实存在的东方古代世界，被电影摄影机记录下来。不是古风写真，不是仙侠大片，而是**东方生活纪录片电影感**。

## 路由

- 需要完整视觉拆解（色彩、光影、材质、构图、空气感、情绪、尾缀、负面词）时，读 [references/visual-spec.md](references/visual-spec.md)。
- 需要动态时间线、分镜秒数、运镜或音效时，转交 `$universal-30s-image-to-video`，不要在本 skill 内自建运镜体系。

## 三条核心原则

1. **世界先于人物**：人物只是生活环境中的一部分，环境占主要叙事空间。
2. **动作先于姿态**：禁止摆拍，人物必须正在生活——洗衣、采摘、晒谷、做饭、编织、赶集、聊天。
3. **拍的是生活，不是拍汉服。**

## 工作方法

1. 先确认场景类型（村落 / 森林 / 古镇 / 田园 / 室内生活），据此选择焦段与光型。
2. 肤色与光感先行：清透淡粉嫩肤色 + 人物自然发光感，面部柔和高光、发丝边缘光，保留真实皮肤纹理。
3. 光影取自然太阳光包裹感，而非强烈戏剧光；阴影柔和、保留层次，禁止死黑。
4. 大场景可加入自然光穿透（树叶间透光、屋檐光、竹林光、空气中的自然光束），但必须是真实摄影光线，不做仙侠光效。
5. 色彩保持低饱和东方自然色：人物粉嫩柔和暖色，环境蓝灰、米白、旧木色。
6. 摄影体系默认 Canon EOS R5 + RF85mm F1.2L（人物 85mm、环境 35mm）。
7. 材质强调棉麻质感、自然褶皱、生活痕迹，建筑用水渍白墙、灰瓦、旧木门、石面。
8. 构图为 16:9 电影画幅，环境 60%–70%、人物 30%–40%，强调人与环境的关系。
9. 空气感是「透明空气」而非雾气，禁止厚重白雾与梦幻磨砂感。
10. 情绪保持东方克制、温暖、安静。

## 输出规范

- 先给中文标题，再给**一段可直接粘贴的英文 Midjourney 提示词**。
- 生成指令全部写在英文提示词内，不要在提示词里夹中文操作说明。
- 英文提示词末尾使用本 skill 的统一尾缀与 Negative Prompt（见 references）。

## 禁止项（速查）

`anime, fantasy, fairy costume, palace clothing, luxury hanfu, studio lighting, plastic skin, CGI, 3D render, oversaturated colors, golden filter, modern elements, fashion photography, perfect pose, artificial smile, heavy shadow, dramatic contrast`

## 修订纪律

用户说「只改服饰 / 妆容 / 构图 / 背景」时，只改该片段，其余从句与其顺序保持不变。用户要求完整版时，再把该处改动合并回完整提示词。
