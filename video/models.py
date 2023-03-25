from django.db import models

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=100)
    images = models.ManyToManyField("ImageList", null=True, blank=True)
    audio = models.FileField(upload_to='media/uploads/audio/')

    def __str__(self):
        return self.name 

class ImageList(models.Model):
    image = models.ImageField(upload_to='media/uploads/')

    def __str__(self):
        return self.image.name 