from django.urls import path
from . import views

urlpatterns = [
    path('Menezes/', views.crypto_view, name='Menezes'),
]
