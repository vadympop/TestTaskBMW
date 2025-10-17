from pathlib import Path

from src.chatgpt import get_questions_answers
from src.config import Config
from src.saving import save_to_csv
from src.transcribing import transcribe


def pipeline(config: Config, audio_file: Path | str) -> None:
    if isinstance(audio_file, str):
        audio_file = Path(audio_file)

    transcript = transcribe(
        str(audio_file),
        hf_token=config.env.hf_token.get_secret_value(),
        device="cpu" if config.env.low_performance_mode else "cuda",
        compute_type="int8" if config.env.low_performance_mode else "float16",
        output_path=str(audio_file.with_suffix(".txt")),
    )
    answers = get_questions_answers(
        transcript=transcript,
        api_key=config.env.openai_token.get_secret_value(),
        questions=config.questions_config.questions
    )
    save_to_csv(
        transcript=transcript,

    )


def main() -> None:
    config = Config.load_config()

    files_dir = Path("data/calls")
    for audio_file in files_dir.rglob("*.mp3"):
        pipeline(config, audio_file)

if __name__ == "__main__":
    main()
