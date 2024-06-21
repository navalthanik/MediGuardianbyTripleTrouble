import sqlite3

def init_db():
    conn = sqlite3.connect('medi_guardian.db')  # This will create the database file if it doesn't exist
    c = conn.cursor()
    # Create table
    c.execute('''CREATE TABLE IF NOT EXISTS videos
                 (id INTEGER PRIMARY KEY, video_name TEXT, audio_name TEXT, transcript TEXT, youtube_link TEXT)''')
    conn.commit()
    conn.close()

    
def insert_video_data(video_name, audio_name, transcript, youtube_link):
    conn = sqlite3.connect('medi_guardian.db')
    c = conn.cursor()
    c.execute("INSERT INTO videos (video_name, audio_name, transcript, youtube_link) VALUES (?, ?, ?, ?)",
              (video_name, audio_name, transcript, youtube_link))
    conn.commit()
    conn.close()
    
def get_video_transcript(video_name):
    conn = sqlite3.connect('medi_guardian.db')
    c = conn.cursor()
    c.execute("SELECT transcript FROM videos WHERE video_name = ? OR youtube_link = ?", (video_name, video_name))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None
