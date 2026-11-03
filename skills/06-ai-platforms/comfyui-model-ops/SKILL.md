---
name: comfyui-model-ops
description: ComfyUI 模型运维——下载/校验大模型文件、判断模型是否真正被 ComfyUI 识别、按底模架构修正工作流参数。当需要下载 safetensors 权重、核对文件完整性、排查"工作流跑不出图/出糊图"、或修改 ComfyUI 工作流 JSON 参数时使用。Triggers: ComfyUI 模型下载, safetensors 校验, 模型完整性, /object_info, 工作流参数修正, model download verify, safetensors integrity check, ComfyUI workflow params, 底模不匹配.
agent_created: true
---

# ComfyUI 模型运维

处理 ComfyUI 的模型文件与工作流参数。核心是**先确认事实，再动手**——这个领域最常见的坑是"以为模型在，其实不在"。

## 铁律：可用性以 API 为准，不看目录、不看配置

判断一个模型能否用，**唯一权威来源**是 ComfyUI 运行实例的 `/object_info`：

```python
# 端口默认 8188，先探测
curl -s "http://127.0.0.1:8188/object_info" -o oi.json
```

然后读这几个字段：
- `UNETLoader.input.required.unet_name[0]` → diffusion_models 实际清单
- `CLIPLoader.input.required.clip_name[0]` → text_encoders 实际清单
- `VAELoader.input.required.vae_name[0]` → vae 实际清单
- `UnetLoaderGGUF.unet_name[0]` → GGUF 模型（**必须单独查**，普通 loader 看不到）
- `CLIPLoader.input.required.type[0]` → 支持的编码器类型（确认如 `krea2` / `lumina2` 是否存在）

**为什么不能用目录/配置判断**：
1. `extra_model_paths.yaml` 里可能有**指向不存在磁盘**的死配置段（本机曾出现 F 盘整盘不存在，两个配置段全废）
2. 该列表是**ComfyUI 进程启动时扫描并缓存**的 → 启动后放进去的模型不会出现，必须重启
3. 模型可能放在未被注册的目录里

**核对磁盘盘符用 PowerShell，不要用 bash**：
```powershell
Get-Volume | Select DriveLetter, FileSystemLabel, Size
Test-Path "F:\"
```
bash 的 `ls /f/` 在盘符不存在时可能给出误导性结果。

## 下载大模型

### 用 Python urllib，不要用 bash curl

**本机实测：Git Bash 的 `curl -w "%{http_code}"` 经常无任何输出**（即使 exit 0），无法用于连通性判断。用 Python：

```python
import os, ssl, urllib.request
# 关键：清空代理变量（本机代理会让国内镜像不通）
for k in ('http_proxy','https_proxy','HTTP_PROXY','HTTPS_PROXY','ALL_PROXY','all_proxy'):
    os.environ.pop(k, None)
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE   # 部分镜像证书链不全

def remote_size(url):
    req = urllib.request.Request(url, method='HEAD', headers={'User-Agent':'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=30, context=ctx) as r:
        return int(r.headers.get('Content-Length'))
```

### 下载必须带断点续传 + 重试

镜像站会中途断流（实测出现 `SSL: UNEXPECTED_EOF_WHILE_READING`）。用 `Range` 头续传，失败原地重试 5 次。完整脚本骨架见 `references/download-template.py`。

要点：
- 每次重试前用 `os.path.getsize` 读已下字节，`headers['Range'] = 'bytes=%d-' % have`
- 打开文件用 `'ab'` 追加模式
- 每 30 秒打印一次进度（GB + MB/s），否则长任务无反馈
- 结束后核对 `have >= total`，不相等就明确报"未完成"

### 下载源优先级

1. **hf-mirror.com**（国内可直连，`Comfy-Org/*` 官方 repack 基本都在）
2. modelscope.cn
3. 官方 huggingface.co（本机不可达）

URL 模板：`https://hf-mirror.com/<repo>/resolve/main/<子路径>`

**先 HEAD 探大小再决定下哪个精度变体**——同一模型常有 bf16 / fp8_scaled / int8_convrot 多版本，体积差一倍。int8 版对 16GB 显存友好。

## 校验：三层，逐层加深

### 第 1 层：字节数比对
用 HEAD 拿到的 `Content-Length` 与本地 `os.path.getsize()` 严格相等。

### 第 2 层：safetensors 头部可解析
```python
import struct, json
with open(p,'rb') as f:
    hlen = struct.unpack('<Q', f.read(8))[0]     # 前 8 字节 = 头部长度
    head = json.loads(f.read(hlen).decode('utf-8').rstrip('\x00'))
keys = [k for k in head if k != '__metadata__']
```
能解析出张量名 + `dtype` + `shape` 说明结构完好。

### 第 3 层（关键）：数据区区间覆盖检查
**这是唯一能发现"续传拼接出错/文件被截断"的方法**，第 1、2 层都发现不了。

```python
data_start = 8 + hlen
patches = sorted(head[k]['data_offsets'] for k in keys if 'data_offsets' in head[k])
expected = os.path.getsize(p) - data_start
cur = 0; contiguous = True
for s, e in patches:
    if s != cur: contiguous = False      # 有空洞 = 续传拼接错位
    cur = max(cur, e)
ok = contiguous and (cur == expected)    # 末尾精确吻合 = 无截断
```

判读技巧：
- `dtype` 分布能验证精度是否如标称。例：`int8_convrot` 应出现 `I8`+`U8`（量化块）+`F32`（scale）；纯 `BF16` 说明是全精度版
- 文本编码器可用张量形状反查模型。例：`model.embed_tokens.weight shape=[151936, 2560]` → Qwen3 系词表大小

## 修改工作流参数

### 先定位格式：新版 subgraph 工作流的两层结构

ComfyUI 新版工作流常把主链封装成 **subgraph**，顶层只放一个「subgraph 实例节点」。参数分两层存：

- **子图内节点**（`definitions.subgraphs[0].nodes`）—— 真实节点
- **顶层实例节点** —— 它把部分参数「提升」为可编辑 widget

**提升过的参数会覆盖子图内的值**，所以两层都要改。顶层 `widgets_values` 是**按 `inputs` 数组顺序**存的平行数组：

```python
# 先打印 inputs 顺序，再按序号改 widgets_values
print([(i.get('label') or i.get('name'), i.get('name'), i.get('type'))
       for i in n['inputs']])
```

`inputs` 里带 `"widget": {"name": ...}` 的条目就是提升的 widget；`origin_id: -10` 的连线表示"来自子图输入槽位 N"。

### 加"真正的负面提示词"节点

很多官方模板的负面分支是 `ConditioningZeroOut` —— **结构上永远是空负面**。要换成真的：
1. `deepcopy` 已有的 `CLIPTextEncode` 节点（保证字段格式完全一致）
2. 改 `id` / `pos` / `title` / `widgets_values`
3. `inputs` 设为 `[{clip, link:新id}]`（去掉原来的 promoted text link）
4. 新增两条连线：`CLIPLoader → 负面节点`、`负面节点 → KSampler.negative`
5. CLIPLoader 的 `outputs[0].links` 追加新 link id
6. KSampler 的 `negative` input link 改指新 id
7. 删除 `ConditioningZeroOut` 节点 + 旧连线，并从上游输出 links 里摘掉旧 id

**改完必须校验**：遍历所有节点的 inputs/outputs，确认每个引用的 link id 都存在于 `sg['links']` 中（无孤立引用）。脚本见 `references/verify-workflow.py`。

### 官方模板是权威参数来源（本地就有）

不要在 GitHub 上找模板（路径常猜错）。ComfyUI 安装目录里就带着：

```
<install>/.venv/Lib/site-packages/comfyui_workflow_templates_json/templates/
```

注意：**同一个大版本可能有多个 ComfyUI install 目录**（如 `ComfyUI-Installs/ComfyUI/` 与 `ComfyUI-Installs/ComfyUI (1)/`），模板可能只存在于其中一个。按 `*z_image*`、`*krea*` 之类的关键词全盘搜。

## 已知的架构级陷阱

### CFG=1.0 时负面提示词完全无效
采样公式 `uncond + cfg × (cond − uncond)`，cfg=1.0 时化简后**只剩 cond**，负面被完全抵消。
- 蒸馏加速模型（Krea 2 Turbo、Z-Image Turbo）官方要求 CFG=1.0 → **结构性无法用负面**
- 非蒸馏 Base 模型（CFG 3–5）负面**高度生效**
- 所以"负面词写了没用"往往不是写法问题，是**数学上没参与计算**

### 蒸馏版与非蒸馏版的参数不可混用
用 Turbo 参数（8 步 / CFG 1）跑 Base 模型 → **出糊图**；反之 Base 参数跑 Turbo 会失去加速意义。

| | Turbo（蒸馏） | Base（非蒸馏） |
|---|---|---|
| 步数 | 8（固定） | 25～50 |
| CFG | 1.0 | 3～5 |
| 负面提示词 | 无效 | 高度响应 |

采样器/调度器/shift/分辨率**通常两版相同**（例：Z-Image 都是 res_multistep + simple + shift 3）。

### 架构决定兼容性，不是 checkpoint
LoRA / 文本编码器 / VAE 全部**按架构隔离**：Flux、SDXL、Krea 2、Z-Image、Qwen-Image 各自独立，跨架构加载直接报错。
判断某工作流属于哪套生态，看它的 `UNETLoader` / `CLIPLoader` 文件名与 `CLIPLoader.type`——比看文件名可靠得多（文件名可能已经和内容不符）。

## 磁盘

大模型动辄 6–13GB，容易把系统盘/软件盘撑满。**先 `shutil.disk_usage()` 看各盘余量再决定下载位置**。
若某盘告急：把模型放到空间大的盘，再在 `extra_model_paths.yaml` 加一段注册（`base_path` + 各分类子目录），重启生效。
