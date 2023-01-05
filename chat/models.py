from django.db import models
from django.contrib.auth.models import User
import random
from datetime import date
from django.db.models.signals import post_save, post_delete
import os
from django.core.validators import FileExtensionValidator


sex = (
    ('male', 'male'),
    ('female', 'female')
)

rand = random.randint(10000,99999)
today = date.today()
rand = str(rand)+str(today)+str(rand)

def user_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (rand, ext)
    return os.path.join('user', filename)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to=user_path, blank=True)
    gender = models.CharField(choices=sex, default='male', max_length=15)

    def __str__(self):  
          return "%s's profile" % self.user  

class Room(models.Model):
    creator = models.ForeignKey(User, related_name='room', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return f"{self.name}"

class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('date_added',)
    
class PersonalMessage(models.Model):
    user = models.ForeignKey(User, related_name='personalmessages', on_delete=models.CASCADE)
    sent_user = models.ForeignKey(User, related_name='personalmessages_sent_user', on_delete=models.CASCADE)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('date_added',)
    
class Book(models.Model):
    user = models.ForeignKey(User, related_name='books', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    audio_src = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"


def create_user_profile(sender, instance, created, **kwargs):  
    if created:  
       created = Profile.objects.get_or_create(user=instance)  

post_save.connect(create_user_profile, sender=User) 