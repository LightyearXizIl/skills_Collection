import json
import sys
import wave
from pathlib import Path

import numpy as np


def read_wav_mono(path: Path):
    with wave.open(str(path), "rb") as w:
        ch = w.getnchannels()
        sw = w.getsampwidth()
        fr = w.getframerate()
        n = w.getnframes()
        raw = w.readframes(n)
    if sw != 2:
        raise SystemExit(f"expect 16-bit pcm, got sampwidth={sw}")
    data = np.frombuffer(raw, dtype="<i2").astype(np.float32) / 32768.0
    if ch > 1:
        data = data.reshape(-1, ch).mean(axis=1)
    return data, fr


def envelope(data, fr, win_sec):
    win = max(1, int(round(win_sec * fr)))
    hop = win
    n = len(data) // hop
    frames = data[: n * hop].reshape(n, hop)
    rms = np.sqrt((frames ** 2).mean(axis=1))
    return rms, hop


def segments_from_mask(mask, hop, fr, min_gap_frames=2):
    segs = []
    start = None
    for i, v in enumerate(mask):
        if v and start is None:
            start = i
        elif not v and start is not None:
            segs.append((start, i))
            start = None
    if start is not None:
        segs.append((start, len(mask)))
    merged = []
    for s, e in segs:
        if merged and s - merged[-1][1] < min_gap_frames:
            merged[-1] = (merged[-1][0], e)
        else:
            merged.append((s, e))
    return [(s * hop / fr, e * hop / fr) for s, e in merged]


def main():
    wav_path = Path(sys.argv[1])
    win_sec = float(sys.argv[2]) if len(sys.argv) > 2 else 0.05
    factor = float(sys.argv[3]) if len(sys.argv) > 3 else 0.06
    out_path = Path(sys.argv[4]) if len(sys.argv) > 4 else None

    data, fr = read_wav_mono(wav_path)
    rms, hop = envelope(data, fr, win_sec)
    peak = float(rms.max())
    thr = peak * factor
    mask = rms >= thr
    segs = segments_from_mask(mask, hop, fr)

    print(f"file={wav_path.name} sr={fr} dur={len(data)/fr:.3f}s win={win_sec}s peak={peak:.5f} thr={thr:.5f}")
    print("--- 发声段（>=阈值）---")
    for s, e in segs:
        print(f"  {s:7.3f} - {e:7.3f}  ({e-s:6.3f}s)")
    print("--- 静默段 ---")
    sil = segments_from_mask(~mask, hop, fr)
    for s, e in sil:
        print(f"  {s:7.3f} - {e:7.3f}  ({e-s:6.3f}s)")

    if out_path:
        out_path.write_text(
            json.dumps(
                {
                    "file": str(wav_path),
                    "sr": fr,
                    "duration": len(data) / fr,
                    "win_sec": win_sec,
                    "peak": peak,
                    "threshold": thr,
                    "times": [round(i * hop / fr, 4) for i in range(len(rms))],
                    "rms": [round(float(v), 6) for v in rms],
                    "voiced_segments": segs,
                    "silent_segments": sil,
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )


if __name__ == "__main__":
    main()
