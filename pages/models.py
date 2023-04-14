from django.db import models

# Create your models here.
class Contact(models.Model):
    email = models.EmailField(verbose_name="البريد الإلكتروني") 

    plan = models.CharField(max_length=100, verbose_name="الباقة" ) 

    details = models.TextField(verbose_name="التفاصيل")

    def __str__(self):
        return self.email 
    
    class Meta:
        verbose_name = 'طلب' 
        verbose_name_plural = 'طلبات التواصل' 