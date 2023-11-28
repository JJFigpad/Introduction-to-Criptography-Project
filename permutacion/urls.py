from django.urls import path
from . import views

urlpatterns = [
    path('printpermutacion/', views.print_permutacion,name='permutacion')
]
