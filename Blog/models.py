from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    desc = models.TextField()
    date = models.DateField(default=datetime.today)
    author_id = models.ForeignKey(User,on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)  
    
    def __str__(self):
        return self.title