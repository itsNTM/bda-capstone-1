from pathlib import Path
import yt_dlp
import csv

def read_video_urls(csv_path):
    urls = []

    with open(csv_path, newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            urls.append(row["url"])
    return urls


def download_video(url):
    Path("videos").mkdir(exist_ok=True)

    # Save inside videos/ using the video title as the filename
    ydl_options = {
        "outtmpl": "videos/%(title)s.%(ext)s"
    }

    # Download video
    with yt_dlp.YoutubeDL(ydl_options) as ydl:
        ydl.download([url])