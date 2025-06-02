from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    is_client = models.BooleanField(default=True)
    is_gestionnaire = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Client Profile"

class Notification(models.Model):
    recipient = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    read_status = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.recipient} at {self.timestamp}"
