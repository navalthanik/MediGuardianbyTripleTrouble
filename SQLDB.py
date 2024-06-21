import sqlite3

def init_db():
    conn = sqlite3.connect('medi_guardian.db')  # This will create the database file if it doesn't exist
    c = conn.cursor()
    # Create table
    c.execute('''CREATE TABLE IF NOT EXISTS videos
                 (id INTEGER PRIMARY KEY, video_name TEXT, audio_name TEXT, transcript TEXT)''')
    conn.commit()
    conn.close()

    
def insert_video_data(video_name, audio_name, transcript):
    conn = sqlite3.connect('medi_guardian.db')
    c = conn.cursor()
    c.execute("INSERT INTO videos (video_name, audio_name, transcript) VALUES (?, ?, ?)",
              (video_name, audio_name, transcript))
    conn.commit()
    conn.close()