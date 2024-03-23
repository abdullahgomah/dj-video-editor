from django.urls import path
from .import views 

app_name = 'image'

urlpatterns = [
    path('changesize/', views.changesize, name='changesize'),
    path('bulk-change-size/', views.bulk_size_change, name='bulk-change-size'),
]