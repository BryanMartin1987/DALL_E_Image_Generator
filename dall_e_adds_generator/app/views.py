from django.shortcuts import render
import openai
import os
from datetime import datetime
import cv2
import numpy as np
import urllib
import time
import concurrent.futures
from django.http import HttpResponse

def get_images(request):
    openai.api_key = "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"
    urls = []
    if request.method == "POST":
        image_count = int(request.POST.get('count'))

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
        _, image_data = cv2.imencode('.jpg', resized_image)
        image_bytes = image_data.tobytes()

        response = HttpResponse(image_bytes, content_type='image/jpeg')
        response['Content-Disposition'] = f'attachment; filename='+ file_name +'.jpg'
        return response
    else:
        return HttpResponse("Unable to download", content_type="text/plain")
  
def upload_image(request):
    directory_path ="./uploads"
    image_files = []
    name = []
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path) and (filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'))):
            name.append(filename)
            image_files.append(file_path)
    i = 0
    for image_path in image_files:
        image = cv2.imread(image_path)

        if image is not None:
            shapes = image.shape
            
            ratio = shapes[1] / shapes[0]
            
            if ratio == 1:
                resized_image = cv2.resize(image, (1080, 1080))
            
            if round(ratio, 2) > 1.8 and ratio < 2:
                resized_image = cv2.resize(image, (1080, 566))
            
            if ratio > 0.75 and ratio < 1:
                resized_image = cv2.resize(image, (1080, 1350))
            
            if ratio > 0.45 and ratio < 0.65:
                resized_image = cv2.resize(image, (1080, 1920))

            cv2.imwrite('./downloads/' + name[i] + '.jpg', resized_image)
            
        else:
            continue
        i = i + 1
    return HttpResponse("Images are downloaded and saved in downloads folder in the project", content_type="text/plain")


# def testing(request):
#     directory_path ="./uploads"
#     image_files = []
#     name = []
#     for filename in os.listdir(directory_path):
#         file_path = os.path.join(directory_path, filename)
#         if os.path.isfile(file_path) and (filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'))):
#             name.append(filename)
#             image_files.append(file_path)
    
#     resolution = '1080x566'

#     i = 0
#     for image_path in image_files:
#         image = cv2.imread(image_path)

#         if image is not None:
#             print(image.shape[0], image.shape[1])

#             resized_image = cv2.resize(image, (540, 283))
#             print(name[i])
#             cv2.imwrite('./uploads/' + resolution + name[i]+ '.jpg', resized_image)
#         i = i + 1
#     return HttpResponse("Unable to download", content_type="text/plain")