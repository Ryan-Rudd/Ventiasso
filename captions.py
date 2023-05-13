import os
import youtube_dl


def fetch_captions(url):
    temp_dir = "temp_captions"
    os.makedirs(temp_dir, exist_ok=True)

    ydl_opts = {
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': ['en'],
        'skip_download': True,
        'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s')
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    file_name = info['title']
    captions_file = os.path.join(temp_dir, f"{file_name}.en.vtt")

    return captions_file
