import os
import sys
import ssl
from yt_dlp import YoutubeDL
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, TIT2, TPE1, TALB

DOWNLOAD_DIR = os.path.join(os.path.expanduser('~'), 'Music', 'YOUTUBE_DOWNLOAD')

# Ensure SSL support
try:
    ssl._create_default_https_context = ssl._create_unverified_context
except AttributeError:
    pass

def download_playlist(playlist_url):
    if not os.path.isdir(DOWNLOAD_DIR):
        os.mkdir(DOWNLOAD_DIR)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'noplaylist': False,
        'ignoreerrors': True
    }

    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(playlist_url, download=True)
        for entry in info_dict['entries']:
            title = entry.get('title', 'Unknown Title')
            artist = entry.get('uploader', 'Unknown Artist')
            album = entry.get('playlist_title', 'Unknown Album')
            file_path = os.path.join(DOWNLOAD_DIR, f"{title}.mp3")
            if os.path.exists(file_path):
                add_metadata(file_path, title, artist, album)

def add_metadata(file_path, title, artist, album):
    try:
        audio = EasyID3(file_path)
    except Exception:
        audio = ID3()

    audio['title'] = title
    audio['artist'] = artist
    audio['album'] = album
    audio.save()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python download_playlist.py <playlist_url>")
        sys.exit(1)

    playlist_url = sys.argv[1]
    download_playlist(playlist_url)
    print(f"Download complete. Files saved to {DOWNLOAD_DIR}")
