from src.transcribing import transcribe


def main() -> None:
    audio_file = "data/calls/2025-08-04_12-50_0934991939_incoming.mp3"
    with open("data/transcript.txt", "w", encoding="utf8") as f:
        f.write(transcribe(audio_file))

if __name__ == "__main__":
    main()
