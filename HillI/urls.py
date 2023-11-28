from django.urls import path
from . import views

urlpatterns = [
    path('printhillI/', views.print_hillI)
]
