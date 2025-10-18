# call2sheet

Transcribes a voice call of manager and client into text using [WhisperX](https://github.com/m-bain/whisperX) library, diarize audio using `pyannote/speaker-diarization-3.1` model, analyzes the transcript with openai chatgpt models according to user-defined questions and puts these results to the csv or xlsx sheet.

## 🧩 Installation (Windows)

### 1. Install dependencies with poetry 
```shell
poetry install
```
### 2. Customize analysis questions
Edit the `configs/questions.json` file to define the questions ChatGPT should answer about each transcript
### 3. Configure environment variables
Copy the .env.dist file to .env and fill in your API key

## ⚡ For better performance, accuracy and speed recommended to use CUDA, so you need

1. Download and install CUDA ToolKit from [CUDA 12.8](https://developer.nvidia.com/cuda-12-8-0-download-archive?target_os=Windows&target_arch=x86_64)
2. Then install the compatible PyTorch build:
```shell
poetry run pip install -U torch==2.8.0 torchaudio==2.8.0 --index-url https://download.pytorch.org/whl/cu128
```

>💡 If you have a different CUDA version (e.g. 12.6 or 13.0), replace cu128 with cu126 or cu130 respectively.

## ▶️ Usage
Once everything is configured, run the program:
```shell
python main.py runmultiple --audios-dir 'PATH TO THE FOLDER' --sheet-path 'PATH TO THE FILE' 
```

Or you can either run pipeline for only single audio with:
```shell
python main.py runsingle --audio-path 'PATH TO THE AUDIO' --sheet-path 'PATH TO THE FILE' 
```

The tool will:
1. Take input audio files from local folder.
2. Transcribe them to text using WhisperX.
3. Analyze each transcript via OpenAI ChatGPT.
4. Export the results to .csv or .xlsx file.
