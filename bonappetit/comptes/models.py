from django.db import models
from django.contrib.auth.models import AbstractUser

class Client(AbstractUser):
    telephone = models.CharField(max_length=20, blank=True)
    adresse = models.TextField(blank=True)
    
    def __str__(self):
        return self.username