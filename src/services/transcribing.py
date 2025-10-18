import logging
import time

import whisperx
import gc
import torch

from whisperx.diarize import DiarizationPipeline
from src.convert import convert_audio_to_wav


torch.backends.cuda.matmul.allow_tf32 = False
torch.backends.cudnn.allow_tf32 = False


logger = logging.getLogger(__name__)


def format_diarized_text(diarized_text: dict) -> str:
    """
    Format diarized text into a string with format:
    [SPEAKER 0] Text Text Text\n
    [SPEAKER 1] ...

    :param diarized_text: Result of diarization pipeline
    :return: Formatted text
    """
    lines = []
    last_speaker = None
    for x in diarized_text["segments"]:
        # In case if segment has no assigment speaker at all
        if x.get("speaker") is None:
            x["speaker"] = last_speaker

        if last_speaker is None or x["speaker"] != last_speaker:
            lines.append([f"[{x["speaker"]}]"])
            last_speaker = x["speaker"]

        lines[-1].append(x["text"].strip())

    return "\n".join([" ".join(line) for line in lines])


def transcribe(
        audio_file: str,
        *,
        hf_token: str,
        device: str = "cuda",
        batch_size: int = 12, # reduce if low on GPU mem
        compute_type: str = "float16", # change to "int8" if low on GPU mem (may reduce accuracy)
        output_path: str = None
) -> str:
    """
    Applies whisper large-v3 language model to transcript text from converted to wav audio file,
    and then use diarization model from huggingface service to separate text by speakers.
    If specified output_path writes transcribed text to file

    :param audio_file: str
    :param hf_token: str
    :param device: str
    :param batch_size: int
    :param compute_type: str
    :param output_path: str
    :return: transcribed text(str)
    """
    model = "large-v3"
    start_time = time.time()

    if not torch.cuda.is_available():
        device = "cpu"
        compute_type = "int8"
        logger.warning("No cuda available, using cpu instead")
    else:
        vram_size = torch.cuda.get_device_properties(0).total_memory / (1024 ** 3)
        if vram_size < 7.5:
            model = "medium"

    converted_audio_output = "converted_audio.wav"
    convert_audio_to_wav(audio_file, converted_audio_output)

    model = whisperx.load_model(model, device, compute_type=compute_type)
    logger.info("Whisper model was loaded")

    audio = whisperx.load_audio(converted_audio_output)
    result = model.transcribe(audio, language="uk", batch_size=batch_size)
    logger.info("Audio was transcribed")

    # delete model if low on GPU resources
    gc.collect(); torch.cuda.empty_cache(); del model

    model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
    result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False)

    # delete model if low on GPU resources
    gc.collect(); torch.cuda.empty_cache(); del model_a

    diarize_model = DiarizationPipeline(use_auth_token=hf_token, device=device)
    diarize_segments = diarize_model(audio, min_speakers=2, max_speakers=2)

    result = whisperx.assign_word_speakers(diarize_segments, result)
    logger.info("Audio was diarized")

    gc.collect(); torch.cuda.empty_cache(); del diarize_model

    result = format_diarized_text(result)
    if output_path:
        with open(output_path, "w", encoding="utf8") as f:
            f.write(result)

    finish_time = time.time()

    logger.info(f"Finished transcribing in {finish_time - start_time}s")

    return result
