import random
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    avatar=models.ImageField(default='#')
    bio=models.TextField(max_length=50,default="Hello i am a user of infoCric")

    def __str__(self):
        return self.user.username   