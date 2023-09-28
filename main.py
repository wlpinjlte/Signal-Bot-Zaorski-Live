import subprocess
import os
# Wprowadź URL livestreamu
import time

url = "https://www.youtube.com/watch?v=Cf9klXhb0G8"

program_folder = os.path.dirname(os.path.abspath(__file__))
try:
    os.remove(os.path.join(program_folder,'images/output.jpg'))
except:
    print("this file doesn't exist")

# Utwórz pełną ścieżkę do pliku wynikowego w folderze programu
output_path = os.path.join(program_folder, "images")
print(output_path)
# Komenda ffmpeg do przechwytywania obrazu
cmd_get_stream_url = [
    "yt-dlp",
    "--no-warnings",
    "--format", "best",  # Wybór formatu
    "--get-url",
    url
]
# Uruchomienie polecenia i zapisanie wyniku do zmiennej
stream_url = subprocess.check_output(cmd_get_stream_url, text=True).strip()
cmd_capture_image = [
    "ffmpeg",
    "-i", stream_url,
    "-f", "image2",
    "-frames:v", "1",
    "images/output.jpg"
]
print(cmd_capture_image)

subprocess.run(cmd_capture_image)