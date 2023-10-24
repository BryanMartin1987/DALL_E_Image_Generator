from django.shortcuts import render
import openai
import json
from datetime import datetime
import cv2
import numpy as np
import urllib
from django.http import HttpResponse


# Create your views here.

def get_images(request):
    openai.api_key = "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"
    urls = []
    if request.method == "POST":
        image_count = int(request.POST.get('count'))

        dimension = request.POST.get('dimensions')

        prompt = request.POST.get('prompt')
        remaining_images_count = image_count % 10

        loop_count = int(image_count/10)

        for _ in range(loop_count):
            urls.append(request_dall_e(prompt, number_of_images= 10))

        if remaining_images_count > 0:
            urls.append(request_dall_e(prompt, remaining_images_count))
            
        context = {
            'urls': [url for sublist in urls for url in sublist]
        }
        return render(request, 'home.html', context)
    
    else:
        return render(request, 'home.html')

def request_dall_e(prompt, number_of_images):
    response = openai.Image.create(
    prompt=prompt,
    n=number_of_images,
    size="1024x1024"
    )
    urls = []
    for i in response['data']:
        urls.append(i['url'])

    return urls

def download_image(request):
    if  request.method == "POST":
        file_name =  datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        image_url = request.POST.get('url')
        dimension = request.POST.get('dimensions')
        height, width = dimension.split('x')
        resp = urllib.request.urlopen(image_url)
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)

        resized_image = cv2.resize(image, (int(height), int(width)))
        cv2.imwrite("./downloads/" + str(file_name) + ".jpg", resized_image)
        return HttpResponse("The image downloaded successfully and it is in downloads folder of current directory", content_type="text/plain")
    else:
        return HttpResponse("Unable to download", content_type="text/plain")