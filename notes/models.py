from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE
from django.contrib.auth import get_user_model


# Create your models here.




# class Note(models.Model):
#     content = models.TextField()
#     tags = models.CharField(max_length=100, blank=True)


class Tag(models.Model):
    tag = models.CharField(max_length=200)

class Note(models.Model):
    content = models.TextField()
    tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,null=True)