from django.urls import path
from . import views
urlpatterns = [
    path('', views.indexRabin, name='indexRabin'),
    path('encrypt/', views.encrypt, name='encrypt'),
    path('decrypt/', views.decrypt, name='decrypt'),
]