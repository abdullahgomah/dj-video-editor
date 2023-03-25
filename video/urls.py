from django.urls import path
from .views import *

app_name = 'video' 

urlpatterns = [
    path('', all, name='all'), 
    path('upload/', upload, name='upload'),
    path('create/', create_project, name='create_project'),
    path('project/<int:id>/', project, name='project'), 
    path('del/<int:id>/', del_img, name='del-img'),
    path('details/<int:id>/', test_function, name='test-function'),
    path('createvideo/', combine_images, name='combine-images'),
    path('createvideowithlogo/', combine_video_withlogo, name='combine-images-withlogo'),
    path('remove_audio/', remove_audio, name='remove-audio'),
    path('changespeed/', change_speed, name='change-speed'),
]