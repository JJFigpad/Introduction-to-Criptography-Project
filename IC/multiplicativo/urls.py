from django.urls import path
from . import views

urlpatterns = [
    path('printmultiplicativo/', views.print_multiplicativo)
]
