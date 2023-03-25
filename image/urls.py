from django.urls import path
from .import views 

app_name = 'image'

urlpatterns = [
    path('changesize/', views.changesize, name='changesize')
]