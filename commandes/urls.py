from django.urls import path
from . import views

app_name = 'commandes'

urlpatterns = [
    # Client accessible URLs (example, might need review based on full app scope)
    path('creer/', views.creer_commande, name='creer_commande'),
    path('mes-commandes/', views.liste_commandes, name='liste_commandes_client'), # Renamed for clarity
    path('modifier/<int:pk>/', views.modifier_commande, name='modifier_commande_client'), # Renamed for clarity

    # Gestionnaire URLs
    path('gestionnaire/toutes/', views.list_all_commandes_view, name='list_all_commandes'),
    path('gestionnaire/update_status/<int:commande_id>/', views.update_commande_status_view, name='update_commande_status'),
]