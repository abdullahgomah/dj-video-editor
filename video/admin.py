from django.contrib import admin

# Register your models here.
from .models import Project, ImageList 

admin.site.register(Project)
admin.site.register(ImageList)