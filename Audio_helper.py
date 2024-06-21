import os
import moviepy.editor as mp
import whisper
import time
import torch

BASE_PATH = os.getcwd()
AUDIO_BASE = f"{BASE_PATH}/audio"
VIDEO_BASE = f"{BASE_PATH}/video"

def extract_audio_to_file(video_path, audio_path):
    if not os.path.exists(audio_path):
        video = mp.VideoFileClip(video_path)
        video.audio.write_audiofile(audio_path, codec='pcm_s16le')

def video_to_transcript_with_whisper(audio_path):

    # Determine the device to load the model on
    device = "cuda" if torch.cuda.is_available() else "cpu"
    # Load the Whisper model
    model = whisper.load_model("tiny", device=device)
    # Transcribe the audio file using the selected model
    start_time = time.time()
    result = model.transcribe(audio_path)
    end_time = time.time()
    transcript = result["text"]
    print(f"Transcription took {end_time - start_time} seconds")
    return transcript, end_time, start_time