import os
import moviepy.editor as mp
import time
import torch
from transformers import pipeline, AutoModelForCausalLM, AutoModelForSpeechSeq2Seq, AutoProcessor
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
device = "cuda:0" if torch.cuda.is_available() else "cpu"
BASE_PATH = os.getcwd()
AUDIO_BASE = f"{BASE_PATH}/audio"
VIDEO_BASE = f"{BASE_PATH}/video"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
def extract_audio_to_file(video_path, audio_path):
    if not os.path.exists(audio_path):
        video = mp.VideoFileClip(video_path)
        video.audio.write_audiofile(audio_path, codec='pcm_s16le')

def audio_to_transcript_with_whisper(audio_path):
    audio = mp.AudioFileClip(audio_path)
    audio_duration = audio.duration
    if audio_duration < 60:
        model_id = "openai/whisper-large-v3"
    else:
        assistant_model_id = "distil-whisper/distil-large-v3"
        start_time_loading_assistant_model = time.time()
        assistant_model = AutoModelForCausalLM.from_pretrained(
            assistant_model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True)
        assistant_model.to(device)
        end_time_loading_assistant_model = time.time()
        print(f"Loading assistant model took {end_time_loading_assistant_model - start_time_loading_assistant_model} seconds")
        model_id = "openai/whisper-large-v3"

    start_time_loading_model = time.time()
    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True)
    model.to(device)
    end_time_loading_model = time.time()
    print(f"Loading Whisper model took {end_time_loading_model - start_time_loading_model} seconds")

    start_time_loading_processor = time.time()
    processor = AutoProcessor.from_pretrained(model_id)
    end_time_loading_processor = time.time()
    print(f"Loading processor took {end_time_loading_processor - start_time_loading_processor} seconds")

    start_time_setting_pipeline = time.time()
    pipe = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        max_new_tokens=128,
        generate_kwargs={"assistant_model": assistant_model} if audio_duration >= 60 else {},
        torch_dtype=torch_dtype,
        device=device)
    end_time_setting_pipeline = time.time()
    print(f"Setting up pipeline took {end_time_setting_pipeline - start_time_setting_pipeline} seconds")

    start_time_transcription = time.time()
    transcript = pipe(audio_path)
    end_time_transcription = time.time()
    print(f"Transcription took {end_time_transcription - start_time_transcription} seconds")
    return transcript['text']