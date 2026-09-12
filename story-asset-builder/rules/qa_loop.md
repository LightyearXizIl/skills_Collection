# 质检与重跑规则

## 质检目的
不要只看图好不好看，要看关键设定是否符合。

## 每个资产必须有 QA Checklist

```text
【实操注意】
1. 跑出来重点检查：
   - 核心识别点
   - 版式比例
   - 角色 / 物种 / 道具准确性
   - 材质和色彩
   - 灯光和风格
   - 标签文字准确性
2. 跑歪兜底加强：
   - 如果 X 错了，追加 Y
   - 如果 Y 漏了，追加 Z
3. 版本迭代建议：
   - v2 修哪个点
   - v3 固定哪个参考图
```

## 重跑方式
不要整段重写 Prompt。按失败点追加补丁：

```text
原 Prompt + failure-specific reinforcement sentence
```

示例：

```text
问题：机械兽跑成生物包机械甲
追加：fully mechanical construction, all bronze panel armor surface in place of fur, NO biological tissue, NO real fur, NO real skin
```

## 版本规则

```text
v1：首版
v2：修正主要跑偏点
v3：锁定参考图后稳定版
vFinal：用户确认版
```
