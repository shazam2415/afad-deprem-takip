# deprem/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # '/' adresine gelen isteği views.deprem_listesi fonksiyonuna gönder
    path('', views.deprem_listesi, name='deprem_listesi'), 
]
