from django.db import models
from django.contrib.auth.models import User 
import datetime
# Create your models here.

class URL(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.TextField()
    Time = models.DateTimeField(auto_now_add=True, blank=True)
    status = models.TextField(default="")

