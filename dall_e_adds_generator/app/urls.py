

from django.urls import path, include
from . import views


urlpatterns = [
   path("", views.get_images, name=""),
   path("download/", views.download_image, name="download")
]
