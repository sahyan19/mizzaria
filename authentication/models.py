from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.crypto import get_random_string

class CustomUser(AbstractUser):
    address = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(max_length=20, choices=[('user', 'User'), ('admin', 'Admin')], default='user')
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    activation_token = models.CharField(max_length=64, blank=True, null=True)  # Ajout du token d'activation

    def generate_activation_token(self):
        self.activation_token = get_random_string(32)
        self.save()

    def __str__(self):
        return self.username
