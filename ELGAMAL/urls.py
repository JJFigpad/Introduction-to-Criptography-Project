from django.urls import path
from . import views

urlpatterns = [
    path('ELGAMAL/', views.crypto_view, name='ELGAMAL'),
]
