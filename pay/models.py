from django.db import models
from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.

class plan (models.Model):
    name=models.CharField(max_length=100)
    price=models.IntegerField()
    validaity=models.CharField(max_length=100)
    
    def __str__(self):
        return self.name



class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    package = models.ForeignKey(plan, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    end_date_time = models.DateField(blank=True, null=True)

    def save(self):
     if not self.end_date_time:
         # (or do something with `self.period`?)
         self.end_date_time = self.start_date+ datetime.timedelta(days=30)
     elif self.package == "forever":
         self.end_date_time = 9999-12-12
     
    
    def str(self):
        return f"{self.user.username}'s {self.package.name} subscription"

class features(models.Model):
    numberVideos =models.IntegerField()
    videoTemplates=models.IntegerField()
    watermark= models.BooleanField()
    plan =models.ForeignKey(plan, on_delete=models.CASCADE)

class PayPal(models.Model):
    PAYPAL_CLIENT_ID = models.CharField(max_length=255, blank=True, null=True)
    PAYPAL_SECRET = models.CharField(max_length=255, blank=True, null=True)
    PAYPAL_ACCESS_TOKEN = models.TextField( blank=True, null=True)
    PAYPAL_CURRENCY = models.CharField(max_length=10, blank=True, null=True)
    
    class Meta:
        verbose_name = ('Paypal')
        verbose_name_plural = ('Paypals')

    