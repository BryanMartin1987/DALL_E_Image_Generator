from django.shortcuts import render
from openai import OpenAI
import os
import os
from multiprocessing import Process, Manager
from datetime import datetime
import cv2
import numpy as np
import urllib
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
client = OpenAI()
client.api_key = "" # Replace with your openai key

@login_required(login_url='/admin')
def get_images(request): 
    urls = []
    if request.method == "POST":
        image_count = int(request.POST.get('count'))

        if image_count > 15:
            context = {
                'errors': ['you cant send more than 15 requests images in one call']
            }
            return render(request, 'home.html', context)

        prompt = request.POST.get('prompt')

        size = request.POST.get('size')

        with Manager() as manager:
            urls = manager.list()
            processes = []

            for _ in range(image_count):
                p = Process(target=request_dall_e, args=(prompt, urls, size))
                p.start()
                processes.append(p)

            for p in processes:
                p.join()

            context = {
                'urls': [url for url in urls]
            }
            return render(request, 'home.html', context)
    else:
        return render(request, 'home.html')

def request_dall_e(prompt, urls, size):
    response = client.images.generate(
    model="dall-e-3",
    prompt=prompt,
    n=1,
    size=size,
    quality="standard"
    )

    url = response.data[0].url
    urls.append(url)

def download_image(request):
    if  request.method == "POST":
        file_name =  datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        image_url = request.POST.get('url')
        resp = urllib.request.urlopen(image_url)
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        resized_image = adjust_size(image)
        _, image_data = cv2.imencode('.png', resized_image)
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

        resized_image = adjust_size(image)

        cv2.imwrite('./downloads/' + name[i] + '.jpg', resized_image)
            
        i = i + 1
    return HttpResponse("Images are downloaded and saved in downloads folder in the project", content_type="text/plain")

def adjust_size(image):
    if image is not None:
            shapes = image.shape
            
            ratio = shapes[1] / shapes[0]
            
            if ratio == 1:
                resized_image = cv2.resize(image, (1080, 1080))
            
            elif round(ratio, 2) > 1.7 and ratio < 2.1:
                resized_image = cv2.resize(image, (1080, 566))
            
            elif ratio > 0.7 and ratio < 1.2:
                resized_image = cv2.resize(image, (1080, 1350))
            
            elif ratio > 0.35 and ratio < 0.71:
                resized_image = cv2.resize(image, (1080, 1920))
            else:
                resized_image = image
            return resized_image

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

def logout_view(request):
    logout(request)
    return redirect("")
