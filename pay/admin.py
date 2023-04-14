from django.contrib import admin
from .models import Plan,Feature,Subscription,PayPal


# Register your models here.

admin.site.register(Plan)
admin.site.register(Feature)
admin.site.register(Subscription)
admin.site.register(PayPal)