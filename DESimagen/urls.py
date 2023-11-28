from django.urls import path
from . import views

urlpatterns = [
    path('DESimagen/', views.crypto_view, name='DESimagen'),
]
