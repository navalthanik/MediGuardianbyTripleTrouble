import os
from ytdownloader import download_youtube_video_as_mp3

def main():
    url = input("Enter the YouTube URL: ")
    output_folder = 'audio'
    
    download_youtube_video_as_mp3(url, output_folder)
    print(f"Downloaded and saved to {output_folder}")

if __name__ == "__main__":
    main()
