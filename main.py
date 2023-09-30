import subprocess
import os
from PIL import Image
import numpy as np
# Wprowadź URL livestreamu
import time

url = "https://www.youtube.com/watch?v=bdaoxG6wYcY"
previous_image_path="images/output_previous.jpg"
new_image_path='images/output_new.jpg'
program_folder = os.path.dirname(os.path.abspath(__file__))


def deleteImage(path):
    try:
        os.remove(os.path.join(program_folder, path))
    except:
        print("this file doesn't exist")

def downloadNewImage():
    # Komenda ffmpeg do przechwytywania obrazu
    cmd_get_stream_url = [
        "yt-dlp",
        "--no-warnings",
        "--format", "b*",  # Wybór formatu
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
        "images/output_new.jpg"
    ]
    # print(cmd_capture_image)
    subprocess.run(cmd_capture_image)

def getImage():
    return Image.open(new_image_path)

def cutImage(image):
    top=921
    left=738
    bottom=1050
    right=805
    image_after_cut=image.crop((left,top,right,bottom))
    image_after_cut.show()
    # deleteImage(new_image_path)
    return image_after_cut

def changeImage():
    new_image=Image.open(new_image_path)
    deleteImage(previous_image_path)
    new_image.save(previous_image_path)

def compareImage():
    new_image=Image.open(new_image_path)
    previous_image=Image.open(previous_image_path)

    new_image=cutImage(new_image)
    previous_image=cutImage(previous_image)

    array_new_image=np.array(new_image)
    array_previous_image = np.array(previous_image)

    hist1, _ = np.histogram(array_new_image, bins=256, range=(0, 256))
    hist2, _ = np.histogram(array_previous_image, bins=256, range=(0, 256))

    # Oblicz różnicę histogramów
    difference = np.abs(hist1 - hist2)

    # Określ próg podobieństwa
    threshold = 4000  # Dostosuj ten próg do swoich potrzeb
    # print(difference)
    # print(np.sum(difference))
    # Porównaj obrazy
    if np.sum(difference) < threshold:
        return True
    else:
        return False

def main():
    time_befor=0
    while(1):
        if time.time()-time_befor>=120:
            time_befor = time.time()
            deleteImage(new_image_path)
            downloadNewImage()
            print(compareImage())
            changeImage()


main()