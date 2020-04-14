from bs4 import BeautifulSoup
import urllib.request
import imquality.brisque as brisque
from PIL import Image
import requests
from io import BytesIO
import threading

fp = urllib.request.urlopen("https://www.darahome.com")
mybytes = fp.read()

html_of_dara = mybytes.decode("utf8")
fp.close()
soup = BeautifulSoup(html_of_dara)

list_of_all_images_in_the_page = soup.findAll('img')


def thread_manager(workers):
    worker_threads = []
    for i in range(len(workers)):
        t = threading.Thread(target=workers[i][0], args=workers[i][1])
        worker_threads.append(t)
        t.start()
    for t in worker_threads:
        t.join()


def get_image_url(image):
    url_of_the_image = image.get("src")
    if url_of_the_image.startswith("//"):
        url_of_the_image = url_of_the_image[2:]
    full_url = f'http://{url_of_the_image}'
    return full_url


images_score = {}


def add_image_to_dict(full_url: str):
    try:
        image_response = requests.get(full_url)
        img = Image.open(BytesIO(image_response.content))
        image_score = brisque.score(img)
        images_score[full_url] = image_score
    except Exception as e:
        print(e)

workers = []
for image_instance in list_of_all_images_in_the_page:
    try:
        full_url = get_image_url(image_instance)
        workers.append((add_image_to_dict, (full_url,)))
    except Exception as e:
        print(e)
thread_manager(workers)

print(images_score)
# print(mystr)
