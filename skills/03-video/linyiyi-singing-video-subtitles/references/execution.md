# S1–S8 操作流程

以下在 PowerShell 执行，变量须使用当前任务的真实绝对路径。先按 `local-environment.md` 设置 `$FF`、`$FP`、`$PY`、`$Model`、`$Font`、`$Skill`，验证 Test-Path 和 Python 模块可导入。缺任务参数时询问，不执行示例占位符。

## S1 探测与归档

```powershell
& $FP -v error -count_frames -show_entries 'format=duration,size:format_tags:stream=codec_type,codec_name,width,height,pix_fmt,r_frame_rate,avg_frame_rate,nb_frames,nb_read_frames,duration' -of json $Video
& "$Skill/scripts/archive_sources.ps1" -ProjectsRoot $ProjectsRoot `
  -ProjectDate $Date -ItemNumber $Number -SongTitle $Title `
  -VideoPath $Video -DryVocalPath $Dry -FullMixPath $Music
```

登记视频基准和三份素材的参数、哈希、来源。归档后将后续变量指向项目内素材。若存在 workflow/prompt tag，保存原始内容至输入素材目录；没有则记未留存，禁止补写上游参数。`03_生成过程` 只放一份过程说明。

## S2 提取工作音频并核对偏移

`$Work` 是项目的 `04_剪辑字幕工程/04_工作副本与备份`。工作文件已存在时先核实对应源，避免覆写其他任务结果。

```powershell
& $FF -v error -n -i $Dry -ac 1 -ar 16000 -c:a pcm_s16le "$Work/_dry16k.wav"
& $FF -v error -n -i $Dry -ac 1 -ar 44100 -c:a pcm_s16le "$Work/_dry44k.wav"
& $FF -v error -n -i $Music -ac 1 -ar 16000 -c:a pcm_s16le "$Work/_music16k.wav"
& $FF -v error -n -i $Video -map 0:a:0 -ac 1 -ar 16000 -c:a pcm_s16le "$Work/_video16k.wav"
& $PY "$Skill/scripts/detail_and_corr.py" corr "$Work/_video16k.wav" "$Work/_music16k.wav"
& $PY "$Skill/scripts/detail_and_corr.py" corr "$Work/_dry16k.wav" "$Work/_music16k.wav"
```

先看时长差；超过 0.1 s 停下来查素材对应关系。视频与完整混音 `|lag|≤0.02 s 且 corr≥0.99` 可视为强一致的近零偏移；其他情况保留数值并听辨。干声与伴奏混音内容不同，相关度较低不能据此证明配错，也不能据此认定零偏移。必要时按多个实际人声起落点交叉核验。

相关脚本定义：正 lag 表示第二条 B 相对第一条 A 更晚，`t_B = t_A + lag`。若 `L_vm=corr(video,music)`、`L_dm=corr(dry,music)` 均可信，则 `t_video=t_dry+L_dm-L_vm`。偏移超过 20 ms 时整体校正字幕并登记；缺强证据时不要自动平移。

## S3 测量演唱边界

```powershell
& $PY "$Skill/scripts/measure_timeline.py" "$Work/_dry16k.wav" --json "$Work/_timeline.json"
& $PY "$Skill/scripts/detail_and_corr.py" detail "$Work/_dry16k.wav" $Start $End 0.02
```

脚本沿用原包阈值：10 ms 步长、25 ms RMS 窗，p10/p90 的 30% 与 12% 为高低阈值，起音基频 score>0.60，尾音延伸 score>0.5，最大延伸 0.60 s。原始数值只作证据，逐句按生产标准裁决，不自行调整判据掩盖错误。保留低置信标记和 tail 延伸量。

## S4 离线核句序

```powershell
& $PY "$Skill/scripts/transcribe_faster_whisper.py" "$Work/_dry16k.wav" $RawAsrJson $Model
```

只用于句数、句序和漏唱判断。ASR 时间可能有偏差，不能把某次片段的固定偏差套到新视频；逐字时间戳不用于字幕定位。原始识别与采用的用户歌词分开保存。

离线模型也会在纯音或无演唱片段输出字幕套话。保留原始 JSON，结合 `no_speech_prob`、实际听辨和输入时长检查；明显套话、超出音频范围或无可靠人声证据的结果不得作为句序核对通过的依据。

## S5 生成 ASS / SRT

按 `lyrics-timeline-schema.md` 写轴，`text` 与原始歌词逐行相同。用 `build_subtitles.py`，宽高和 duration 必须来自探测。它从 `subtitle_template.ass` 生成固定版式，保留全部歌词空格；另写歌词核对稿，记录每句测量依据、偏移、人工复核情况。

## S6 烧录

```powershell
& "$Skill/scripts/render_subtitles.ps1" -InputVideo $Video -AssPath $Ass `
  -OutputVideo $Out -FfmpegPath $FF -FontPath $Font
```

脚本创建唯一 ASCII 临时目录，复制 ASS 与指定字体；滤镜仅使用相对路径，`ass=sub.ass:fontsdir=fonts`。默认 `libx264 -preset slow -crf 18 -pix_fmt yuv420p -c:a copy -movflags +faststart`；无裁切、缩放、变速、重采样或混音。不同内容不覆盖，标准成片失败时不改原件。

## S7 验收

```powershell
& "$Skill/scripts/validate_output.ps1" -InputVideo $Video -OutputVideo $Out `
  -ReportPath $Report -FfmpegPath $FF -FfprobePath $FP
& $FF -v error -n -i $Out -ss 1.6 -frames:v 1 $CheckPng
```

自动报告包含完整解码、分辨率/帧率/帧数、逐音轨哈希、时长差、成片 SHA-256。必须再逐句和逐边界查看检查图、必要时听辨，尤其关注起音、吸气、拖腔、空格、长句安全区和标题不遮口型。自动报告通过不等于这些人工项通过。

## S8 文档与交付

至少补齐项目清单、素材清单、唯一生成过程说明、抖音发布文案、歌词核对稿，以及剪辑规范副本和字体授权说明。发布文案是本地交付，不自动发布或发送给他人。

把本技能的脚本复制到项目 `04_剪辑字幕工程/03_工具脚本`，并把 `references/subtitle_template.ass` 一并复制到该工具脚本目录。生成器找不到技能相对目录时会读取同目录模板，也可用 `--template` 显式指定，保证项目归档后仍能独立重建。

项目清单记录实际标题坐标、歌词来源（用户提供）、测量/识别/复核状态、音轨哈希和成片哈希；上游生成资料缺失就记未留存。若 H3 duration 与实际片长不符，记录数值与后段口型待核实，不猜生成参数。词曲版权和字体许可分别说明。
