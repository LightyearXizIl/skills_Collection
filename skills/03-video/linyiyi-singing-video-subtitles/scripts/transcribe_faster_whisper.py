import json
import sys
from pathlib import Path

from faster_whisper import WhisperModel


def main() -> None:
    if len(sys.argv) != 4:
        raise SystemExit("usage: transcribe_faster_whisper.py INPUT OUTPUT_JSON LOCAL_MODEL_DIR")

    input_path = Path(sys.argv[1]).resolve()
    output_path = Path(sys.argv[2]).resolve()
    model_name = Path(sys.argv[3]).resolve()
    if not input_path.is_file() or not model_name.is_dir() or not (model_name / "model.bin").is_file():
        raise SystemExit("输入或本地模型不完整；不会下载模型")
    if output_path.exists() or output_path == input_path:
        raise SystemExit("识别输出必须是新文件")

    model = WhisperModel(str(model_name), device="cpu", compute_type="int8", local_files_only=True)
    segments, info = model.transcribe(
        str(input_path),
        language="zh",
        beam_size=5,
        best_of=5,
        vad_filter=False,
        word_timestamps=False,
        condition_on_previous_text=True,
    )

    result = {
        "input": str(input_path),
        "language": info.language,
        "language_probability": info.language_probability,
        "duration": info.duration,
        "segments": [],
    }
    for segment in segments:
        result["segments"].append(
            {
                "start": segment.start,
                "end": segment.end,
                "text": segment.text.strip(),
                "avg_logprob": segment.avg_logprob,
                "no_speech_prob": segment.no_speech_prob,
                "words": [
                    {
                        "start": word.start,
                        "end": word.end,
                        "word": word.word,
                        "probability": word.probability,
                    }
                    for word in (segment.words or [])
                ],
            }
        )

    result["usage"] = "sentence order only; do not use ASR timestamps for subtitle alignment"
    result["local_model"] = str(model_name)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("x", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
