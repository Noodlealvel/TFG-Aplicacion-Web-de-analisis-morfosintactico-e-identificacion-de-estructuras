import os
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Analysis(models.Model):
    username = models.TextField()
    sentence = models.TextField()
    type = models.TextField()
    resultSyntactic = models.FileField(upload_to=os.path.join(os.path.dirname(os.path.dirname(__file__)), "static/media/svg"))
    resultMorphologic = models.TextField()
    date=models.DateTimeField(auto_now_add=True)
