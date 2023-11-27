from django.urls import path
from . import views

urlpatterns = [
    path('DES/', views.crypto_view, name='DES'),
]

