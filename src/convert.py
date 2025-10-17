import subprocess
from pathlib import Path

from src.config import Config
from src.models import AIAnswersOutput, AnswerResult


def convert_audio_to_wav(input_path: str, output_path: str) -> None:
    """
    Convert audio file to wav file using ffmpeg run using subprocess.

    :param input_path:
    :param output_path:
    :return:
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg", "-y",
        "-i", input_path,
        "-ar", "16000",  # 16kHz
        "-ac", "1",      # mono
        "-c:a", "pcm_s16le",  # 16-bit PCM
        output_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def ai_answers_to_result(ai_output: AIAnswersOutput, config: Config) -> list[AnswerResult]:
    """
    Convert ai output model to list of AnswerResult models.
    Basically adds save_to_column field to AIAnswer model's data

    :param ai_output:
    :param config:
    :return: List[AnswerResult]
    """
    return [
        AnswerResult(
            answer=ai.answer,
            save_to_column=config.questions_config.questions[ai.index].save_to_column
        )
        for ai in ai_output.answers
    ]

