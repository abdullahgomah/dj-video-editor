from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="المستخدم")
    image = models.ImageField(default='default.jpg', upload_to='profile_pics/', verbose_name='صورة الملف الشخصي', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"
    

    class Meta:
        verbose_name='ملف شخصي'
        verbose_name_plural ='الملفات الشخصية'