from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Client, Notification

# Inline pour le modèle Client
class ClientInline(admin.StackedInline):
    model = Client
    can_delete = False  # Empêche la suppression du profil Client depuis l'admin User
    verbose_name_plural = 'Profil Client'
    fk_name = 'user' # Spécifier la clé étrangère si ce n'est pas évident pour Django

# Personnalisation de l'admin pour User pour inclure Client
class CustomUserAdmin(UserAdmin):
    inlines = (ClientInline, )
    # Ajout des champs de Client dans list_display
    # Assurez-vous que les champs de UserAdmin par défaut que vous voulez garder sont là
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff',
                    'get_is_client', 'get_is_gestionnaire')
    list_select_related = ('client', ) # Optimisation pour récupérer le client en même temps

    def get_is_client(self, instance):
        # Gère le cas où le profil client n'existe pas encore (bien que la vue register le crée)
        try:
            return instance.client.is_client
        except Client.DoesNotExist:
            return False
    get_is_client.short_description = 'Client'
    get_is_client.boolean = True # Affiche une icône True/False

    def get_is_gestionnaire(self, instance):
        try:
            return instance.client.is_gestionnaire
        except Client.DoesNotExist:
            return False
    get_is_gestionnaire.short_description = 'Gestionnaire'
    get_is_gestionnaire.boolean = True

    # S'assurer que les inlines ne s'affichent pas lors de la création d'un nouvel utilisateur
    # (car le profil Client est lié à un User existant)
    def get_inline_instances(self, request, obj=None):
        if not obj: # Si c'est un nouvel objet (création)
            return list()
        return super().get_inline_instances(request, obj)

# Désenregistrer le User admin par défaut
admin.site.unregister(User)
# Réenregistrer User avec le CustomUserAdmin
admin.site.register(User, CustomUserAdmin)

# Enregistrer Notification (si toujours nécessaire)
admin.site.register(Notification)

# Ne plus enregistrer Client séparément si vous l'avez fait avant
# admin.site.register(Client)
