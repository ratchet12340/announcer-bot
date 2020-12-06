import youtube_dl
import subprocess

def progress_hook(download):
    if download['status'] == 'finished':
        print('Download finished! Converting...')

def download(output_name, url):
    parms = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'progress_hooks': [progress_hook],
        'outtmpl': output_name,
    }

    with youtube_dl.YoutubeDL(parms) as ydl:
        urls = [url]
        ydl.download(urls)

    print("Conversion finished. Trimming...")

    full_name = output_name

    ffmpeg_cmd = [
        f"ffmpeg -ss 00:00:00 -to 00:00:03 -i {full_name} {full_name}"
    ]

    subprocess.run(ffmpeg_cmd)

    print("Trimming finished. Done!")
