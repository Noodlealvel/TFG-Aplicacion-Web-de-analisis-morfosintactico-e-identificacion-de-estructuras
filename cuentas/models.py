import os
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Analysis(models.Model):
    username = models.TextField()
    sentence = models.TextField()
    type = models.TextField()
    date=models.DateTimeField(auto_now_add=True)
