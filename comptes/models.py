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
    TYPE_CHOICES = [
        ('commande', 'Commande'),
        ('systeme', 'Système'),
        ('promo', 'Promotion'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    type_notification = models.CharField(max_length=20, choices=TYPE_CHOICES, default='systeme')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    link = models.CharField(max_length=255, blank=True, null=True)  # Pour rediriger vers une page spécifique
    icon = models.CharField(max_length=50, default='fas fa-bell')  # Classe FontAwesome pour l'icône

    def __str__(self):
        return f"Notification pour {self.user.username}: {self.message[:30]}"

    class Meta:
        ordering = ['-created_at']
        
    @classmethod
    def create_notification(cls, user, message, type_notification='systeme', link=None, icon=None):
        """Méthode utilitaire pour créer une notification"""
        return cls.objects.create(
            user=user,
            message=message,
            type_notification=type_notification,
            link=link,
            icon=icon or cls._meta.get_field('icon').default
        )
