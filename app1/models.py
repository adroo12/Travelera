from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    phone=models.IntegerField()
    place=models.CharField(max_length=50)
