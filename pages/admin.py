from django.contrib import admin
from .models import Contact 

# Register your models here.


admin.site.site_header = 'Video Editor'
admin.site.index_title = 'Video Editor'    # default: "Site administration"
admin.site.site_title = 'Admin Panel'      # default: "Django site admin"


admin.site.register(Contact) 