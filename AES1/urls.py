# En myapp/urls.py
from django.urls import path
from .views import image_upload, image_list
from django.contrib import admin
from django.urls import path, include
from vigenere import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
   path('upload/', image_upload, name='image_upload'),
   path('list/', image_list, name='image_list'),
    # Agrega más URL según sea necesario
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)