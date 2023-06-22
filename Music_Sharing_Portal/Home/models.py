from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import User
from django.http import HttpResponse


# Create your models here.

# for storing all audio files to each user.
class AudioFiles(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_image = models.ImageField(upload_to='image/')
    file_name = models.CharField(max_length=250)
    files = models.FileField(upload_to='audio/')
    visibility = models.CharField(max_length=250)


# for storing email address for protected files along with file access(foreignkey)
class ProtectedFiles(models.Model):
    file = models.ForeignKey(AudioFiles, on_delete=models.CASCADE)
    email = models.EmailField(max_length=150, blank=True)



