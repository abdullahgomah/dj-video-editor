from django.urls import path 
from .import views 

app_name = 'audio'

urlpatterns = [
    path('changespeed/', views.change_audio_speed, name='change-speed'),
    path('download-audio/', views.download_audio, name='download-audio'), 
]
