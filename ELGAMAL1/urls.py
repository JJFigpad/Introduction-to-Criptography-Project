from django.urls import path
from . import views

urlpatterns = [
    path('ELGAMAL1/', views.crypto_view, name='ELGAMAL1'),
]
