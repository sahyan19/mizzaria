from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    address = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(max_length=20, choices=[('user', 'User'), ('admin', 'Admin')], default='user')
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

# class BlacklistedToken(models.Model):
#     token = models.CharField(max_length=500, unique=True)
#     blacklisted_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.token