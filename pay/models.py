from django.db import models
from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.

class Plan(models.Model):
    name=models.CharField(max_length=100, verbose_name='اسم الباقة')
    price=models.IntegerField(verbose_name="سعر الباقة")
    validaity=models.CharField(max_length=100, verbose_name="دورة الباقة (30 يوم)")
    unlimited=models.BooleanField(default=False, verbose_name='غير محدودة')
    videos_per_months = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name



class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    end_date_time = models.DateField(blank=True, null=True)
    videos_per_months = models.IntegerField(default=0)

    # def save(self, *args, **kwargs ):
    #     if not self.end_date_time:
    #      # (or do something with `self.period`?)
    #         self.end_date_time = datetime.datetime.strptime(self.start_date, "%YYYY-%MM-%DD") + datetime.timedelta(days=int(self.plan.validaity))
    #     elif self.plan.unlimited == True:
    #         self.end_date_time = 9999-12-12

    #     super(Subscription, self).save(*args, **kwargs)
    
    
    def __str__(self):
        return f"{self.user.username}'s {self.plan.name} subscription"


class Feature(models.Model):
    plan =models.OneToOneField(Plan, on_delete=models.CASCADE)
    numberVideos =models.IntegerField()
    template1 = models.BooleanField(default=True, verbose_name="النموذج الأول") 
    template2 = models.BooleanField(default=False, verbose_name="نموذج فيديو مع لوجو") 
    template3 = models.BooleanField(default=False, verbose_name="نموذج تقييم") 

    change_img_size = models.BooleanField(default=False, verbose_name="تغيير حجم الصور") 
    remove_audio = models.BooleanField(default=False, verbose_name="إزالة الصوت من الفيديو")
    change_video_speed = models.BooleanField(default=False, verbose_name="تغيير سرعة الفيديو") 
    change_audio_speed = models.BooleanField(default=False, verbose_name="تغيير سرعة الصوت") 

    watermark= models.BooleanField(default=True, verbose_name="العلامة المائية")

    def __str__(self):
        return f"{self.plan} Features"

class PayPal(models.Model):
    PAYPAL_CLIENT_ID = models.CharField(max_length=255, blank=True, null=True)
    PAYPAL_SECRET = models.CharField(max_length=255, blank=True, null=True)
    PAYPAL_ACCESS_TOKEN = models.TextField( blank=True, null=True)
    PAYPAL_CURRENCY = models.CharField(max_length=10, blank=True, null=True)
    
    class Meta:
        verbose_name = ('Paypal')
        verbose_name_plural = ('Paypals')

    