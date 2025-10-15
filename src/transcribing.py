import whisperx
import gc
from whisperx.diarize import DiarizationPipeline


import torch

from src.convert import convert_to_wav

torch.backends.cuda.matmul.allow_tf32 = False
torch.backends.cudnn.allow_tf32 = False

YOUR_HF_TOKEN = ""
device = "cuda"
batch_size = 16 # reduce if low on GPU mem
compute_type = "float16" # change to "int8" if low on GPU mem (may reduce accuracy)

def transcribe(audio_file: str) -> str:
    convert_to_wav(audio_file, "converted.wav")

    model = whisperx.load_model("large-v3", device, compute_type=compute_type)

    audio = whisperx.load_audio("converted.wav")
    result = model.transcribe(audio, language="uk", batch_size=batch_size)

    print("Before alignment:")
    for x in result["segments"]:
        print(f"[{x['start']} --> {x['end']}] {x['text']}")

    # delete model if low on GPU resources
    gc.collect(); torch.cuda.empty_cache(); del model

    # 2. Align whisper output
    model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
    result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False)

    print("\n\nAfter alignment:")
    for x in result["segments"]:
        print(f"[{x['start']} --> {x['end']}] {x['text']}")

    # delete model if low on GPU resources
    gc.collect(); torch.cuda.empty_cache(); del model_a

    diarize_model = DiarizationPipeline(use_auth_token=YOUR_HF_TOKEN, device=device)
    diarize_segments = diarize_model(audio, min_speakers=2, max_speakers=2)

    result = whisperx.assign_word_speakers(diarize_segments, result)

    lines = []
    last_speaker = None
    for x in result["segments"]:
        if last_speaker is None or x["speaker"] != last_speaker:
            lines.append([f"[{x["speaker"]}]"])
            last_speaker = x["speaker"]

        lines[-1].append(x["text"].strip())

    return "\n".join([" ".join(line) for line in lines])
