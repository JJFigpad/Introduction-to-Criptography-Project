from django.urls import path
from . import views

urlpatterns = [
    path('MenezesVanstone/', views.crypto_view, name='MenezesVanstone'),
]
