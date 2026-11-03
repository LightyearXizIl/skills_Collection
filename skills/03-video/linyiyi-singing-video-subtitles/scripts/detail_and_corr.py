import argparse
import json
import math
import wave
from pathlib import Path

import numpy as np


def read_wav_mono(path: Path):
    with wave.open(str(path), "rb") as w:
        ch = w.getnchannels()
        fr = w.getframerate()
        if w.getsampwidth() != 2 or w.getcomptype() != "NONE":
            raise ValueError("16-bit PCM WAV required")
        raw = w.readframes(w.getnframes())
    data = np.frombuffer(raw, dtype="<i2").astype(np.float64) / 32768.0
    if ch > 1:
        data = data.reshape(-1, ch).mean(axis=1)
    return data, fr


def detail(path, t0, t1, win=0.02):
    d, fr = read_wav_mono(Path(path))
    if not all(math.isfinite(v) for v in (t0, t1, win)) or not 0 <= t0 < t1 <= len(d)/fr or win <= 0 or int(win*fr) < 1:
        raise ValueError("invalid detail interval or window")
    i0, i1 = int(t0 * fr), min(int(t1 * fr), len(d))
    seg = d[i0:i1]
    n = len(seg) // int(win * fr)
    if n == 0:
        raise ValueError("interval shorter than window")
    hop = int(win * fr)
    frames = seg[: n * hop].reshape(n, hop)
    rms = np.sqrt((frames ** 2).mean(axis=1))
    peak = float(rms.max())
    print(f"# {Path(path).name}  {t0}-{t1}s  win={win}s  peak={peak:.5f}")
    for k, v in enumerate(rms):
        t = t0 + k * win
        bar = "#" * int(v / peak * 60) if peak > 0 else ""
        print(f"{t:7.2f}  {v:.5f}  {bar}")


def corr(a_path, b_path, max_lag_sec=1.5):
    a, fa = read_wav_mono(Path(a_path))
    b, fb = read_wav_mono(Path(b_path))
    length_a, length_b = len(a)/fa, len(b)/fb
    if fa != fb:
        raise ValueError("sample rate mismatch")
    if not math.isfinite(max_lag_sec) or max_lag_sec < 0:
        raise ValueError("invalid maximum lag")
    if min(len(a), len(b)) < fa * 2:
        raise ValueError("at least two seconds of overlap required")
    a = a - a.mean()
    b = b - b.mean()
    n = min(len(a), len(b))
    a, b = a[:n], b[:n]
    nfft = 1 << (2*n-1).bit_length()
    cross = np.fft.irfft(np.conj(np.fft.rfft(a, nfft))*np.fft.rfft(b, nfft), nfft)
    limit = min(int(max_lag_sec*fa), n-2*fa)
    lags = np.arange(-limit, limit+1)
    a0, b0 = np.maximum(0, -lags), np.maximum(0, lags)
    a1, b1 = n-np.maximum(0, lags), n-np.maximum(0, -lags)
    ea = np.r_[0.0, np.cumsum(a*a)]
    eb = np.r_[0.0, np.cumsum(b*b)]
    denom = np.sqrt(np.maximum(0, ea[a1]-ea[a0])*np.maximum(0, eb[b1]-eb[b0]))
    valid = denom > 1e-15
    if not valid.any():
        raise ValueError("no usable correlation: silent or zero-energy input")
    scores = np.full(len(lags), -np.inf)
    scores[valid] = np.clip(cross[lags[valid] % nfft]/denom[valid], -1, 1)
    best_i = int(np.argmax(scores))
    lag, c = int(lags[best_i]), float(scores[best_i])
    print(f"# corr {Path(a_path).name} vs {Path(b_path).name}")
    print(f"best lag = {lag} samples = {lag/fa:+.4f}s  corr = {c:.6f}")
    print(f"len a={length_a:.3f}s  len b={length_b:.3f}s")
    return {"lag_samples": lag, "lag_seconds": lag/fa, "correlation": c,
            "zero_lag_correlation": float(scores[limit]) if valid[limit] else None,
            "length_a_seconds": length_a,
            "length_b_seconds": length_b,
            "near_zero_strong_match": abs(lag/fa) <= 0.02 and c >= 0.99,
            "direction": "positive lag means B is later than A; t_B = t_A + lag"}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    commands = ap.add_subparsers(dest="mode", required=True)
    cp = commands.add_parser("corr")
    cp.add_argument("a"); cp.add_argument("b")
    cp.add_argument("--max-lag", type=float, default=1.5)
    cp.add_argument("--json", type=Path)
    dp = commands.add_parser("detail")
    dp.add_argument("wav"); dp.add_argument("start", type=float); dp.add_argument("end", type=float)
    dp.add_argument("window", nargs="?", type=float, default=0.02)
    args = ap.parse_args()
    if args.mode == "detail":
        detail(args.wav, args.start, args.end, args.window)
    else:
        if args.json and args.json.exists():
            raise ValueError("correlation JSON already exists")
        result = corr(args.a, args.b, args.max_lag)
        if args.json:
            with args.json.open("x", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
        print(json.dumps(result, ensure_ascii=False))
