from django.db import models
from cloudinary.models import CloudinaryField



# Create your models here.


class Picture(models.Model):
    description = models.CharField(max_length=200)
    image = models.FileField(upload_to='photo_for_users',max_length=200)
