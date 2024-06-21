import os
from ytdownloader import download_youtube_video_as_mp3
from transcript_generator import transcribe_audio, transcribe_audio_fast

def main():
    url = input("Enter the YouTube URL: ")
    output_folder = 'audio'
    transcript_folder = 'Transcript'
    
    # Ensure the transcript folder exists
    if not os.path.exists(transcript_folder):
        os.makedirs(transcript_folder)

    download_youtube_video_as_mp3(url, output_folder)
    print(f"Downloaded and saved to {output_folder}")

    # Assuming the audio file is named after the video title in mp3 format
    audio_file_path = os.path.join(output_folder, os.listdir(output_folder)[0])
    transcript_file_path = transcribe_audio_fast(audio_file_path)
    
    # # Move the transcript file to the Transcript folder
    # transcript_file_name = os.path.basename(transcript_file_path)
    # new_transcript_path = os.path.join(transcript_folder, transcript_file_name)
    # os.rename(transcript_file_path, new_transcript_path)
    
    print(f"Transcript saved to {transcript_file_path}")

if __name__ == "__main__":
    main()
