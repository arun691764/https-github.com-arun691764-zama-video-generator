import requests
from bs4 import BeautifulSoup
import textwrap
import subprocess
import os
from gtts import gTTS

def fetch_text(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    blocks = []
    for tag in soup.find_all(["h1", "h2", "h3", "p"]):
        t = tag.get_text(" ", strip=True)
        if len(t) > 5:
            blocks.append(t)
    return blocks

def save_audio(text, path):
    gTTS(text, lang='en').save(path)

def generate_video(url):
    print("Fetching text...")
    blocks = fetch_text(url)
    if not blocks:
        raise SystemExit("No text found on page.")

    full_text = ". ".join(blocks)

    print("Generating TTS...")
    audio_path = "voice.mp3"
    save_audio(full_text, audio_path)

    print("Generating slides file…")
    with open("slides.txt", "w", encoding="utf-8") as f:
        for t in blocks:
            t = t.replace("\n", " ").replace("%", "%%")
            f.write(t + "\n")

    print("Building video using FFmpeg…")
    cmd = [
        "ffmpeg",
        "-y",
        "-f", "lavfi",
        "-i", "color=size=1920x1080:duration=30:rate=1:color=000000",
        "-i", audio_path,
        "-vf",
        "drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:"
        "fontsize=36:fontcolor=white:x=100:y=100:textfile=slides.txt",
        "-c:v", "libx264",
        "-c:a", "aac",
        "-shortest",
        "zama_video.mp4"
    ]

    subprocess.run(cmd, check=True)
    print("VIDEO READY: zama_video.mp4")

if __name__ == "__main__":
    generate_video("https://www.zama.org/blog")
