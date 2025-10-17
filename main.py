from pathlib import Path

from src.config import Config
from src.pipeline import run_pipeline


def main() -> None:
    config = Config.load_config()

    files_dir = Path("data/calls")
    for audio_file in files_dir.rglob("*.mp3"):
        run_pipeline(config, audio_file)

if __name__ == "__main__":
    main()
