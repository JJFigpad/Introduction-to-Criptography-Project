from django.urls import path
from . import views

urlpatterns = [
    path('printhillT/', views.print_hillT,name='hillT')
]
