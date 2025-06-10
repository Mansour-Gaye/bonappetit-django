from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings # Required for ForeignKey to AUTH_USER_MODEL

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True)
    is_client = models.BooleanField(default=True)
    is_gestionnaire = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="customuser_groups_set", # Ensure unique related_name
        related_query_name="user_group",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="customuser_permissions_set", # Ensure unique related_name
        related_query_name="user_permission",
    )

    def __str__(self):
        return self.username

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message[:30]}"

    class Meta:
        ordering = ['-created_at']
