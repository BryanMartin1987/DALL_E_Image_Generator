

from django.urls import path, include
from . import views


urlpatterns = [
   path("", views.get_images, name=""),
   path("download/", views.download_image, name="download"),
   path("uploads/", views.upload_image, name= "upload" )
   # path("testing/", views.testing, name='testing')
]
