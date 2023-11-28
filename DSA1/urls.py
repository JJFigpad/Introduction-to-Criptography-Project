from django.urls import path
from . import views

urlpatterns = [
    path('DSA/', views.crypto_view, name='DSA'),
]
