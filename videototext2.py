import moviepy.editor as mp
import whisper
import os
import time


BASE_PATH = os.getcwd()
AUDIO_BASE = f"{BASE_PATH}/audio"
VIDEO_BASE = f"{BASE_PATH}/video"

def extract_audio_to_file(video_path, audio_path):
  """
  Uses the moviepy package to extract and write
  audio content to a new file only if it doesn't already exist
  """
  if not os.path.exists(audio_path):
    # Load the video from file
    video = mp.VideoFileClip(video_path)
    # Extract the audio file from the video.
    # The codec is chosen to be a compatible format for Whisper
    video.audio.write_audiofile(audio_path, codec='pcm_s16le')

def video_to_transcript_with_whisper(video_path):
  extract_audio_to_file(video_path, audio_path)
  # First grab the relevant model for the task at hand
  model = whisper.load_model("large", device="cuda")
  # Transcribe the audio file using the selected model
  start_time = time.time()
  result = model.transcribe(audio_path)
  end_time = time.time()
  transcript = result["text"]
  print(f"Transcription took {end_time - start_time} seconds")
  return result["text"]

if __name__ == "__main__":
  filename = "test4"
  audio_path = f"{AUDIO_BASE}/{filename}.wav"
  video_path = f"{VIDEO_BASE}/{filename}.mp4" if os.path.exists(f"{VIDEO_BASE}/{filename}.mp4") else f"{VIDEO_BASE}/{filename}.mkv"
  if not os.path.exists(audio_path):
    transcript = video_to_transcript_with_whisper(video_path, audio_path)
  else:
    # Load the existing audio file into Whisper for transcription
    model = whisper.load_model("large", device="cuda")
    start_time = time.time()
    result = model.transcribe(audio_path)
    end_time = time.time()
    transcript = result["text"]
    print(f"Transcription took {end_time - start_time} seconds")
  print(transcript)