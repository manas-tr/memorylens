import os

video_path = "vid01.mp4"
audio_path = "vid01.wav"

command = f'ffmpeg -i "{video_path}" -q:a 0 -map a "{audio_path}" -y'

os.system(command)

print("audio extracted!")