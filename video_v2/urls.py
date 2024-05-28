from django.urls import path
from .views import *

app_name = 'video_v2'

urlpatterns = [
    path('combine/', combine_images, name='combine'),
    # path('combine/', combine_imgs_v2, name='combine'),
    path('new-combine/', new_create, name='new-create'),
    path('ffmpeg-create/', upload_and_create_video_with_ffmpeg, name='ffmpeg-create'), 
    path('test_prev/', text_preview_export, name='text_preview_export'), 
]
