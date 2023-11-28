from django.urls import path
from . import views

urlpatterns = [
    path('printRSA/', views.print_rsa,name='RSA')
]
