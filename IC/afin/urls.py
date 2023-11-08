from django.urls import path
from . import views

urlpatterns = [
    path('printafin/', views.print_afin)
]
