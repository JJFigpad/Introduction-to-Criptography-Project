from django.urls import path
from . import views

urlpatterns = [
    path('printSDES/', views.print_sdes)
]
