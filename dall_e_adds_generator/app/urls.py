
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
   path("", views.get_images, name=""),
   path("download/", views.download_image, name="download"),
   path("uploads/", views.upload_image, name= "upload" ),
   path('logout/', views.logout_view, name='logout'),
   path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login')
]
