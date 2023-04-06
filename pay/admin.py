from django.contrib import admin
from .models import plan,features,Subscription,PayPal



# Register your models here.

admin.site.register(plan)
admin.site.register(features)
admin.site.register(Subscription)
admin.site.register(PayPal)