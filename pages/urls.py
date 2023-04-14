from django.urls import path 
from . import views 
import pages 

app_name = 'pages' 

urlpatterns = [
    path('', views.index, name='index'), 
    path('check/', views.check_plan, name='check'), 
    path('contact/', views.contact_form, name='contact') 
]

