#!/usr/bin/env python3
"""Build fixed ASS/SRT after exact comparison with the user's lyric lines."""
import argparse
import json
import math
import re
from pathlib import Path


def ass_time(seconds):
    cs = round(seconds * 100)
    h, cs = divmod(cs, 360000)
    m, cs = divmod(cs, 6000)
    s, cs = divmod(cs, 100)
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


def srt_time(seconds):
    ms = round(seconds * 1000)
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def plain_text(text, label):
    if not isinstance(text, str) or not text.strip():
        raise ValueError(f"{label}: expected a nonempty string")
    if any(c in text for c in "\\{}") or any(ord(c) < 32 or ord(c) == 127 for c in text):
        raise ValueError(f"{label}: ASS/control characters require manual review")
    if "\u2028" in text or "\u2029" in text:
        raise ValueError(f"{label}: line separators require separate lyric rows")
    return text  # Do not strip, split, or normalize whitespace.


def load_segments(path, duration):
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    rows = payload.get("segments") if isinstance(payload, dict) else payload
    if not isinstance(rows, list) or not rows:
        raise ValueError("lyrics JSON must contain a nonempty segment list")
    previous_end = -1.0
    result = []
    for index, row in enumerate(rows, 1):
        if not isinstance(row, dict):
            raise ValueError(f"segment {index}: expected an object")
        start, end = float(row["start"]), float(row["end"])
        if not (math.isfinite(start) and math.isfinite(end)):
            raise ValueError(f"segment {index}: timing must be finite")
        if start < 0 or end <= start or end > duration or start < previous_end:
            raise ValueError(f"segment {index}: invalid, overlapping, or out-of-range timing")
        if round(end * 100) <= round(start * 100):
            raise ValueError(f"segment {index}: zero ASS duration after centisecond rounding")
        text = plain_text(row["text"], f"segment {index}")
        fade_in, fade_out = row.get("fade_in_ms", 100), row.get("fade_out_ms", 120)
        if type(fade_in) is not int or type(fade_out) is not int:
            raise ValueError(f"segment {index}: fades must be integer milliseconds")
        if not 80 <= fade_in <= 100 or not 100 <= fade_out <= 200:
            raise ValueError(f"segment {index}: fade outside fixed production range")
        if fade_in + fade_out > (end - start) * 1000:
            raise ValueError(f"segment {index}: fades exceed subtitle duration")
        result.append(dict(start=start, end=end, text=text, fade_in=fade_in, fade_out=fade_out))
        previous_end = end
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    for option in ("song-title", "lyrics-json", "lyrics-text", "ass-output", "srt-output"):
        ap.add_argument(f"--{option}", required=True, type=str if option == "song-title" else Path)
    ap.add_argument("--width", type=int, required=True)
    ap.add_argument("--height", type=int, required=True)
    ap.add_argument("--duration", type=float, required=True)
    ap.add_argument("--title-y", type=int)
    ap.add_argument("--credit-y", type=int)
    ap.add_argument("--template", type=Path, help="optional project-local ASS template")
    ap.add_argument("--credit", default="— 林依依")
    args = ap.parse_args()
    if args.width <= 0 or args.height <= 0 or not math.isfinite(args.duration) or args.duration < 3.6:
        raise ValueError("positive resolution and at least 3.6 seconds required for the fixed intro")
    title = plain_text(args.song_title, "song title")
    if title.startswith("《") or title.endswith("》"):
        raise ValueError("provide the verified title without book-title brackets")
    credit = plain_text(args.credit, "credit")
    if credit != "— 林依依":
        raise ValueError("the fixed credit is — 林依依")
    segments = load_segments(args.lyrics_json, args.duration)
    with args.lyrics_text.open(encoding="utf-8-sig", newline=None) as f:
        original = f.read()
    if original.endswith("\n"):
        original = original[:-1]
    if original.split("\n") != [row["text"] for row in segments]:
        raise ValueError("lyric rows differ from the user's original lines, including whitespace")
    template_path = args.template or (Path(__file__).resolve().parents[1] / "references" / "subtitle_template.ass")
    if not args.template and not template_path.is_file():
        template_path = Path(__file__).resolve().with_name("subtitle_template.ass")
    template_path = template_path.resolve()
    template = template_path.read_text(encoding="utf-8")
    k = args.height / 2048
    title_y = args.title_y if args.title_y is not None else round(0.479 * args.height)
    credit_y = args.credit_y if args.credit_y is not None else round(0.535 * args.height)
    if not 0 <= title_y < credit_y < args.height:
        raise ValueError("title/credit positions must be ordered within the frame")
    values = {
        "PLAYRESX": args.width, "PLAYRESY": args.height, "SONG_TITLE": title,
        "FS_TITLE": max(1, round(100*k)), "FS_CREDIT": max(1, round(54*k)),
        "FS_LYRIC": max(1, round(74*k)), "MARGIN_V": max(1, round(235*k)),
        "CX": args.width / 2, "Y_TITLE": title_y, "Y_CREDIT": credit_y,
        "MARGIN_LR": round(84 * args.width / 1088),
        "TITLE_MARGIN_LR": round(63 * args.width / 1088),
    }
    header = "\n".join(line for line in template.split("; 歌词逐句追加", 1)[0].splitlines()
                       if not line.startswith(";")) + "\n"
    for name, value in values.items():
        header = header.replace("{{" + name + "}}", str(value))
    if re.search(r"\{\{[A-Z_]+\}\}", header):
        raise ValueError("unresolved ASS template token")
    ass_lines = [header.rstrip()]
    srt = []
    for index, row in enumerate(segments, 1):
        ass_lines.append(
            f"Dialogue: 0,{ass_time(row['start'])},{ass_time(row['end'])},Lyrics,,0,0,0,,"
            + "{\\fad(" + f"{row['fade_in']},{row['fade_out']}" + ")}" + row["text"]
        )
        srt.append(f"{index}\n{srt_time(row['start'])} --> {srt_time(row['end'])}\n{row['text']}")
    outputs = (args.ass_output.resolve(), args.srt_output.resolve())
    inputs = {args.lyrics_json.resolve(), args.lyrics_text.resolve(), template_path}
    if outputs[0] == outputs[1] or any(p in inputs or p.exists() for p in outputs):
        raise ValueError("output paths must be distinct, new, and different from inputs")
    for path, data in zip(outputs, ("\n".join(ass_lines)+"\n", "\n\n".join(srt)+"\n")):
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("x", encoding="utf-8", newline="\n") as f:
            f.write(data)
    print(json.dumps({"ass": str(outputs[0]), "srt": str(outputs[1]), "segments": len(segments),
                      "lyrics_exact_match": True, "title_y": title_y, "credit_y": credit_y}, ensure_ascii=False))


if __name__ == "__main__":
    main()
