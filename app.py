import os
import shutil
import pytube
from moviepy.editor import *
from art import *
from termcolor import colored
import inquirer


def download_audio(url):
    temp_dir = "temp_audio"
    os.makedirs(temp_dir, exist_ok=True)

    youtube = pytube.YouTube(url)
    video = youtube.streams.filter(only_audio=True).first()
    audio_path = video.download(output_path=temp_dir)

    file_name = os.path.splitext(os.path.basename(audio_path))[0]
    audio_file = os.path.join(temp_dir, file_name + ".mp3")

    if os.path.exists(audio_file):
        os.remove(audio_file)

    os.rename(audio_path, audio_file)

    return audio_file


def generate_tiktok_video(audio_file, video_output):
    bg_color = (204, 204, 204)
    video = ColorClip(size=(720, 1280), color=bg_color, duration=10)

    audio = AudioFileClip(audio_file)

    video = video.set_audio(audio)

    video = video.resize(height=1280, width=720)
    video = video.set_fps(30)

    try:
        video.write_videofile(video_output, codec="libx264", audio_codec="aac")
        shutil.rmtree("temp_audio")

    except OSError as e:
        raise ValueError("Error: Failed to generate the TikTok video.") from e


def generate_tiktok():
    questions = [
        inquirer.Text("youtube_url", message="Enter the YouTube URL:"),
        inquirer.Text("output_path", message="Enter the output video path:")
    ]
    answers = inquirer.prompt(questions)

    youtube_url = answers["youtube_url"]
    output_path = answers["output_path"]

    try:
        audio_file_path = download_audio(youtube_url)
        generate_tiktok_video(audio_file_path, output_path)

        print("TikTok video generated successfully!")

    except (ValueError, pytube.exceptions.PytubeError) as e:
        print(colored(str(e), "red"))


if __name__ == "__main__":
    art_text = text2art("Ventiasso", chr_ignore=True)
    colored_art_text = colored(art_text, "yellow")
    print(colored_art_text)

    generate_tiktok()
