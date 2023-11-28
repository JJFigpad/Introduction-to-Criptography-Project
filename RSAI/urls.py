from django.urls import path
from . import views

urlpatterns = [
    path('printRSAI/', views.print_rsaI)
]
