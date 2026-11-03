# 歌词时间轴 JSON

UTF-8 JSON 对象或数组；每个 segment 对应用户的一行歌词，按时间升序且不重叠。

```json
{
  "segments": [
    {"start": 0.8, "end": 2.6, "text": "第一句　保留全角空格", "evidence": "干声起音和尾音已复核"},
    {"start": 3.0, "end": 5.2, "text": "第二句  保留双空格", "fade_in_ms": 80, "fade_out_ms": 160}
  ]
}
```

- start/end 为有限非负秒数，end>start；必须在成片时长内。ASS 以厘秒表示，量化后也不得变为零时长。
- text 必须是字符串，空格与文字不得清洗；换行通过不同记录表示，停顿通过时间缺口表示。
- `--lyrics-text` 必须指定用户原始逐句歌词文件；生成器逐行精确比对，保留行内及行首行尾空格，不跳过空行、不修改断句。可有一个末尾换行。
- `evidence` 建议记录实测、听辨、偏移和拖腔依据；正文不混入来源或说明。
- 可选淡入 80–100 ms、淡出 100–200 ms；默认为 100/120。
- 遇到 ASS 控制字符（反斜杠、花括号）或行内控制字符先报错，不能将用户正文当成排版指令或静默替换。

```powershell
& $PY "$Skill/scripts/build_subtitles.py" `
  --song-title '正式歌名' --lyrics-json $Timeline --lyrics-text $OriginalLyrics `
  --ass-output $Ass --srt-output $Srt --width $W --height $H --duration $Duration
```

只有经过画面复核需要避脸时，传 `--title-y` 与 `--credit-y`，并将原因和实际坐标记入项目清单。脚本无法自行判断脸部位置和拖腔是否准确。
