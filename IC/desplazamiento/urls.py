from django.urls import path
from . import views

urlpatterns = [
    path('printdesplazamiento/', views.print_desplazamiento)
]
