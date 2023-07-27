from django.db import models
from datetime import datetime
# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    desc = models.TextField()
    date = models.DateField(default=datetime.today)