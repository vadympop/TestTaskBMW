import subprocess
from pathlib import Path

def convert_to_wav(input_path: str, output_path: str) -> None:
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
