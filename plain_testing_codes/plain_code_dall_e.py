import cv2
import numpy as np
import urllib
import openai

openai.api_key = "" # put your openai api key

prompt = input("input a prompt")
height = input("Enter output height")
width = input("Enter output width")

try:
    response = openai.Image.create(
    prompt=prompt,
    n=10,
    size="1024x1024"
    )
    image_url = response['data'][0]['url']
    urls = []
    for images in response['data']:
        urls.append(images['url'])


    resp = urllib.request.urlopen(image_url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    if image is not None:
        resized_image = cv2.resize(image, (width, height))
        cv2.imwrite("resized_image.jpg", resized_image)
    else:
        print("Failed to retrieve the image from the URL.")
except:
    print("something went wrong")
