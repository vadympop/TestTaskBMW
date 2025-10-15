from src.transcribing import transcribe
from pathlib import Path


def main() -> None:
    files_dir = Path("data/calls")
    for audio_file in files_dir.rglob("*.mp3"):
        transcribe(
            str(audio_file),
            hf_token="",
            device="cuda",
            compute_type="float16",
            output_path=str(audio_file.with_suffix(".txt")),
        )

if __name__ == "__main__":
    main()
