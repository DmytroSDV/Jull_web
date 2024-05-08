from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model



# Create your models here.


class Picture(models.Model):
    description = models.CharField(max_length=200)
    image = models.FileField(upload_to='photo_for_users',max_length=500)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,null=True)
