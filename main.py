import typer
from pathlib import Path

from src.config import Config
from src.pipeline import run_pipeline


tapp = typer.Typer()
config = Config.load_config()


@tapp.command()
def runmultiple(audios_dir: str, sheet_path: str) -> None:
    """
    Executes the full pipeline for all audios from specified directory:
    1. Transcribes the input.
    2. Generates answers for questions defined in the config file using chatgpt.
    3. Saves the results to the specified output file (csv or xlsx).

    :param audios_dir: Path to the audio folder.
    :param sheet_path: Path to the sheet file(csv or xlsx).
    :return: None
    """
    files_dir = Path(audios_dir)
    for audio_file in files_dir.rglob("*.mp3"):
        run_pipeline(config, sheet_path, audio_file)


@tapp.command()
def runsingle(audio_path: str, sheet_path: str) -> None:
    """
    Executes the full pipeline for specified audio path:
    1. Transcribes the input.
    2. Generates answers for questions defined in the config file using chatgpt.
    3. Saves the results to the specified output file (csv or xlsx).

    :param audio_path: Path to the audio file.
    :param sheet_path: Path to the sheet file(csv or xlsx).
    :return: None
    """
    audio_file = Path(audio_path)
    run_pipeline(config, sheet_path, audio_file)


if __name__ == "__main__":
    tapp()
