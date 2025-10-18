import os.path

import typer
from pathlib import Path
from itertools import chain

from src.config import Config
from src.pipeline import run_pipeline


tapp = typer.Typer()
config = Config.load_config()


def _validate_paths(audio_path: Path, sheet_path: str) -> None:
    """
    Raise exception if audio path is not exists or if sheet path is not exists.

    :param audio_path: Path object to audio path.
    :param sheet_path: String object to sheet path.
    :return: None
    """
    if not audio_path.exists():
        raise ValueError(f"{audio_path} invalid audio path")

    if not os.path.exists(sheet_path):
        raise ValueError(f"{sheet_path} invalid sheet path")



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
    if not files_dir.is_dir():
        raise ValueError(f"{audios_dir} is not a directory")

    _validate_paths(files_dir, sheet_path)

    for audio_file in chain(files_dir.rglob("*.mp3"), files_dir.rglob("*.wav")):
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
    _validate_paths(audio_file, sheet_path)

    run_pipeline(config, sheet_path, audio_file)


if __name__ == "__main__":
    tapp()
