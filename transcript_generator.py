import whisper
from faster_whisper import WhisperModel
import os

os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

def transcribe_audio(audio_path):
    model = whisper.load_model("small")
    result = model.transcribe(audio_path)
    transcript = result["text"]
    
    # Save the transcript to a .txt file in the 'Transcript' folder
    transcript_folder = 'Transcript'
    if not os.path.exists(transcript_folder):
        os.makedirs(transcript_folder)
    transcript_file_name = os.path.basename(os.path.splitext(audio_path)[0] + ".txt")
    transcript_file_path = os.path.join(transcript_folder, transcript_file_name)
    
    with open(transcript_file_path, 'w') as file:
        file.write(transcript)
    
    return transcript_file_path

def transcribe_audio_fast(audio_path):
    model_size = "large-v2"
    model = WhisperModel(model_size, device="cuda", compute_type="float16")
    segments, info = model.transcribe(audio_path, beam_size=5)

    full_transcript = ""
    for segment in segments:
        print(segment.text)
        full_transcript += segment.text + " "
    
    print(full_transcript)
    transcript = full_transcript
    
    transcript_folder = 'Transcript'
    if not os.path.exists(transcript_folder):
        os.makedirs(transcript_folder)
    transcript_file_name = os.path.basename(os.path.splitext(audio_path)[0] + ".txt")
    transcript_file_path = os.path.join(transcript_folder, transcript_file_name)
    
    with open(transcript_file_path, 'w') as file:
        file.write(transcript)
    
    return transcript_file_path



