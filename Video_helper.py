import yt_dlp
import uuid
def download_youtube_audio(youtube_link, output_path):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': output_path,
        'prefer_ffmpeg': True,
        'keepvideo': False
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_link])
        
def generate_unique_filename(extension):
    return str(uuid.uuid4()) + extension