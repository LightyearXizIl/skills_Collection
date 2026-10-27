"""干声音轨演唱段边界测量（林依依唱歌视频字幕流水线）。

设计目标：把「哪一段在唱、从哪一秒到哪一秒」测成可复核的数字，
避免两类典型错误：
  1) 单纯靠固定阈值切分，把渐弱的拖腔尾音截断（第08条句7被截掉0.3s）；
  2) 把吸气、唇齿声当成演唱起点（第07条第4句误判0.26s）。

方法：
  - 10ms 步长 / 25ms 窗 RMS -> dBFS；
  - 阈值自适应：以 dB 分布的 p10 作本底、p90 作满幅，取 30% 处为「明确在唱」阈值；
  - 段内用 12% 处的低阈值向两侧延伸，延伸段必须同时满足「有声」与「基频可信」，
    因此能把渐弱拖腔接回来，又不会把伴奏串音或静音底噪算进去；
  - 逐段给出中位基频与音名，便于人工比对歌词落点。

用法：
  python measure_timeline.py DRY16K.wav [--json OUT.json] [--min-gap 0.12] [--min-dur 0.10]

输入要求：16kHz 单声道 16bit PCM wav（ffmpeg -ac 1 -ar 16000 -c:a pcm_s16le 生成）。
只读，不改动任何输入文件。
"""

import argparse
import json
import sys
import wave
from pathlib import Path

import numpy as np

HOP = 0.010
WIN = 0.025
NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def read_wav_mono(path: Path):
    with wave.open(str(path), "rb") as w:
        ch, sw, fr, n = w.getnchannels(), w.getsampwidth(), w.getframerate(), w.getnframes()
        raw = w.readframes(n)
    if sw != 2:
        raise SystemExit(f"需要 16bit PCM wav，实际 sampwidth={sw}")
    if ch != 1 or fr != 16000:
        raise SystemExit("需要 16kHz 单声道 PCM wav")
    data = np.frombuffer(raw, dtype="<i2").astype(np.float64) / 32768.0
    if ch > 1:
        data = data.reshape(-1, ch).mean(axis=1)
    return data, fr


def rms_db(a, fr):
    hop, L = int(HOP * fr), int(WIN * fr)
    n = max(0, 1 + (len(a) - L) // hop)
    frames = np.lib.stride_tricks.as_strided(
        a, shape=(n, L), strides=(a.strides[0] * hop, a.strides[0])
    )
    rms = np.sqrt((frames ** 2).mean(axis=1))
    return 20 * np.log10(rms + 1e-9), n


def f0_score(a, fr, t_center, win=0.030, fmin=70.0, fmax=800.0):
    """自相关基频与可信度。返回 (f0, score)；score<0.5 视为无稳定基频。"""
    i0 = int((t_center - win / 2) * fr)
    i1 = int((t_center + win / 2) * fr)
    if i0 < 0 or i1 > len(a) or i1 - i0 < 64:
        return 0.0, 0.0
    seg = a[i0:i1].copy()
    seg -= seg.mean()
    if np.sqrt((seg ** 2).mean()) < 0.004:
        return 0.0, 0.0
    seg *= np.hanning(len(seg))
    cc = np.correlate(seg, seg, "full")[len(seg) - 1:]
    cc /= (cc[0] + 1e-12)
    lo, hi = int(fr / fmax), int(fr / fmin)
    if hi >= len(cc):
        return 0.0, 0.0
    k = int(np.argmax(cc[lo:hi])) + lo
    return fr / k, float(cc[k])


def close_gaps(mask, max_gap_frames):
    out = mask.copy()
    i = 0
    while i < len(out):
        if not out[i]:
            j = i
            while j < len(out) and not out[j]:
                j += 1
            if i > 0 and j < len(out) and (j - i) <= max_gap_frames:
                out[i:j] = True
            i = j
        else:
            i += 1
    return out


def mask_to_ranges(mask):
    out, start = [], None
    for i, v in enumerate(mask):
        if v and start is None:
            start = i
        elif not v and start is not None:
            out.append((start, i))
            start = None
    if start is not None:
        out.append((start, len(mask)))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("wav")
    ap.add_argument("--json")
    ap.add_argument("--min-gap", type=float, default=0.12, help="小于该值的静音视为连唱")
    ap.add_argument("--min-dur", type=float, default=0.10, help="短于该值的段丢弃")
    ap.add_argument("--tail", type=float, default=0.60, help="收尾最大延伸秒数")
    args = ap.parse_args()
    if any(not np.isfinite(v) or v < 0 for v in (args.min_gap, args.min_dur, args.tail)):
        raise SystemExit("时间参数必须为有限非负数")
    if args.json and Path(args.json).exists():
        raise SystemExit("JSON 已存在，请检查旧结果或另选输出名")

    path = Path(args.wav).resolve()
    a, fr = read_wav_mono(path)
    db, n = rms_db(a, fr)
    if n < 10:
        raise SystemExit("音频过短")
    t = np.arange(n) * HOP

    p10, p90 = np.percentile(db, 10), np.percentile(db, 90)
    thr_hi = p10 + 0.30 * (p90 - p10)
    thr_lo = p10 + 0.12 * (p90 - p10)

    mask = close_gaps(db > thr_hi, int(round(args.min_gap / HOP)))
    raw = [(s, e) for s, e in mask_to_ranges(mask) if (e - s) * HOP >= args.min_dur]

    print(f"file={path.name}  sr={fr}  dur={len(a)/fr:.3f}s  frames={n}")
    print(f"dBFS p10={p10:6.1f}  p90={p90:6.1f}  thr_hi={thr_hi:6.1f}  thr_lo={thr_lo:6.1f}")
    print()
    print(" idx    onset     offset     dur    peak   median_f0   note   tail")
    print("------------------------------------------------------------------")

    segs = []
    tail_max = int(round(args.tail / HOP))
    for k, (s, e) in enumerate(raw):
        # 起点：段内找到第一个「基频可信」的帧，再回退 50ms 带上辅音。
        # 只认能量会把吸气、气声、字头噪声当成演唱起点（第08条第5句曾提前 0.37s）。
        onset_i, low_conf = None, False
        for i in range(s, min(e, s + int(0.80 / HOP))):
            f, sc = f0_score(a, fr, t[i] + WIN / 2)
            if sc > 0.60:
                onset_i = max(s - int(0.05 / HOP), i - int(0.05 / HOP), 0)
                break
        if onset_i is None:
            onset_i, low_conf = s, True
        # 收尾：过阈末帧之后，按低阈值 + 基频可信度继续延伸，接住渐弱拖腔
        off_i = e - 1
        next_start = raw[k + 1][0] if k + 1 < len(raw) else n
        for i in range(e, min(n, next_start, e + tail_max)):
            f, sc = f0_score(a, fr, t[i] + WIN / 2)
            if db[i] > thr_lo and sc > 0.5:
                off_i = i
            elif db[i] <= thr_lo:
                break

        seg_a = db[s:e]
        peak = float(seg_a.max())
        f0s = []
        for i in range(onset_i, off_i + 1, 3):
            f, sc = f0_score(a, fr, t[i] + WIN / 2)
            if f > 0 and sc > 0.5:
                f0s.append(f)
        med = float(np.median(f0s)) if f0s else 0.0
        note = ""
        if med > 0:
            midi = int(round(69 + 12 * np.log2(med / 440.0)))
            note = f"{NOTE_NAMES[midi % 12]}{midi // 12 - 1}"
        onset, offset = onset_i * HOP, (off_i + 1) * HOP
        flag = "  <-- 低置信：段内未找到稳定基频，起点按能量给出，需人工复核" if low_conf else ""
        print(f"{k:4d}  {onset:7.3f}   {offset:7.3f}  {offset-onset:6.3f}  {peak:6.1f}  "
              f"{med:9.1f}   {note:>4s}   {(off_i - (e - 1)) * HOP:+.2f}{flag}")
        segs.append(
            {
                "index": k,
                "onset": round(onset, 3),
                "offset": round(offset, 3),
                "duration": round(offset - onset, 3),
                "peak_dbfs": round(peak, 1),
                "median_f0": round(med, 1),
                "note": note,
                "tail_seconds": round((off_i - (e - 1)) * HOP, 3),
                "low_confidence": low_conf,
                "requires_sentence_review": True,
            }
        )

    print()
    print("--- 间隙（含首尾）---")
    prev = 0.0
    for s in segs:
        if s["onset"] - prev >= 0.08:
            print(f"  {prev:7.3f} - {s['onset']:7.3f}  ({s['onset']-prev:5.3f}s)")
        prev = s["offset"]
    if len(a) / fr - prev >= 0.08:
        print(f"  {prev:7.3f} - {len(a)/fr:7.3f}  ({len(a)/fr-prev:5.3f}s)  [尾部]")

    if args.json:
        Path(args.json).write_text(
            json.dumps(
                {"file": str(path), "duration": len(a) / fr,
                 "thresholds": {"p10": p10, "p90": p90, "thr_hi": thr_hi, "thr_lo": thr_lo},
                 "segments": segs},
                ensure_ascii=False, indent=2),
            encoding="utf-8")
        print(f"\njson -> {args.json}")


if __name__ == "__main__":
    sys.exit(main())
