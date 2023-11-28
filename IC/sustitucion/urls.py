from django.urls import path
from . import views

urlpatterns = [
    path('printsustitucion/', views.print_sustitucion)
]
