"""
URL configuration for IC project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from vigenere import views
from django.conf.urls.static import static
from django.conf import settings
from .views import index




urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    #path('vigenere/', views.vigenere, name='vigenere'),
    path('vigenere/',include("vigenere.urls")),
    path('multiplicativo/', include('multiplicativo.urls')),
    path('sustitucion/', include('sustitucion.urls')),
    path('afin/', include('afin.urls')),
    path('rabin/', include('rabin.urls')),
    path('AES1/', include('AES1.urls')),
    #path('vigenere/', views.vigenere, name='vigenere'),
    path('desplazamiento/', include('desplazamiento.urls')),
    path('multiplicativo/', include('multiplicativo.urls')),
    path('sustitucion/', include('sustitucion.urls')),
    path('afin/', include('afin.urls')),
    path('rabin/', include('rabin.urls')),
    path('permutacion/', include('permutacion.urls')),
    path('hillT/', include('HillT.urls')),
    path('hillI/', include('HillI.urls')),
    path('RSA/', include('RSA.urls')),
    path('RSAI/', include('RSAI.urls')),
    path('DES/', include('DES.urls')),
    path('DESimagen/', include('DESimagen.urls')),
    path('ELGAMAL1/',include('ELGAMAL1.urls')),
    path('Menezes/',include('Menezes.urls')),
    path('DSA/',include('DSA.urls')),    
  
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)