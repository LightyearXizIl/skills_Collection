# 资产拆解规则

## 目标
把剧本拆成可生成、可管理、可复用的 LibTV 资产节点。

## 必须识别的资产类型

### 1. Character / 人物
包括主角、反派、配角、群众、士兵、导师、怪人、变体形态。

判断依据：
- 有名字或称谓
- 有行动决策
- 有情绪或人物弧线
- 后续多镜头复用

默认模板：`templates/character_sheet.md`

### 2. Creature / 怪兽、生物、机械兽
包括巨兽、异形、机械动物、怪物、宠物、坐骑、变异生命体。

默认模板：`templates/creature_sheet.md`

### 3. Prop / 道具、武器、设备
包括手持物、武器、机关、钥匙、收音机、电脑、法器、产品。

默认模板：`templates/prop_sheet.md`

### 4. Vehicle / 载具
包括飞船、车、沙艇、机甲、船、摩托、飞行器。

默认模板：`templates/vehicle_sheet.md`

### 5. Environment / 场景
包括房间、村庄、街道、集市、宫殿、峡谷、飞船内部、地下室。

默认模板：`templates/environment_sheet.md`

### 6. Color / Material DNA
包括色卡、材质体系、灯光规则、世界观视觉规范。

默认模板：`templates/color_palette.md`

### 7. Storyboard / Keyframe
包括九宫格分镜、关键帧、场景动作拆解、镜头运动参考。

默认模板：`templates/storyboard_grid.md`

### 8. Video Segment
包括单段视频、转场、口播、动作、音乐 MV、短片段落。

默认模板：`templates/video_prompt.md`

## 资产优先级

```text
P0：必须先生成，否则后续无法保持一致
P1：核心剧情资产
P2：增强世界观资产
P3：可后补细节资产
```

默认优先级：
- 主角 / 反派 / 核心怪兽 / 核心场景：P0
- 重要道具 / 载具 / 第二场景：P1
- 群众 / 背景道具 / 色卡：P2
- 纹理、贴图、细节补充：P3

## 输出格式

```yaml
assets:
  - asset_id: CHR_001
    asset_name: 主角名称
    asset_type: character
    asset_role: 主角 / 反派 / 配角 / 群众
    priority: P0
    template: templates/character_sheet.md
    libtv_node_group: 01_Character_Assets
    aspect_ratio: 9:16
    required_views: FRONT FACE / SIDE FACE / BODY FRONT / BACK
    prompt_status: draft
    qa_risk:
      - 脸型不稳定
      - 服装跑偏
      - 年龄错误
```
