
from django.urls import path
from . import views

urlpatterns = [
    path('vigenere/', views.vigenere, name='vigenere'),
]
