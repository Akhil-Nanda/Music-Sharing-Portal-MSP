from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class ProfileVerify(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    auth_tokens = models.CharField(max_length=250)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.first_name
