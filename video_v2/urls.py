from django.urls import path
from .views import *

app_name = 'video_v2'

urlpatterns = [
    path('combine/', combine_images, name='combine')   
]
