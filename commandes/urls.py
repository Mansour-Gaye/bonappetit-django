from django.urls import path
from . import views

app_name = 'commandes'

urlpatterns = [
    # Client accessible URLs (example, might need review based on full app scope)
    path('passer-commande/', views.passer_commande, name='passer_commande'),
    path('mes-commandes/', views.liste_commandes, name='liste_commandes_client'), # Renamed for clarity
    path('modifier/<int:pk>/', views.modifier_commande, name='modifier_commande_client'), # Renamed for clarity

    # Gestionnaire URLs
    path('gestionnaire/toutes/', views.list_all_commandes_view, name='list_all_commandes'),
    path('gestionnaire/update_status/<int:commande_id>/', views.update_commande_status_view, name='update_commande_status'),

    path('', views.liste_commandes, name='liste_commandes'),
    path('historique/', views.historique_commandes, name='historique_commandes'),
    path('nouvelle/', views.nouvelle_commande, name='nouvelle_commande'),
    path('detail/<int:commande_id>/', views.detail_commande, name='detail_commande'),
    path('annuler/<int:commande_id>/', views.annuler_commande, name='annuler_commande'),
    path('confirmer/<int:commande_id>/', views.confirmer_commande, name='confirmer_commande'),
    path('panier/', views.voir_panier, name='voir_panier'),
    path('panier/ajouter/<int:menu_id>/', views.ajouter_au_panier, name='ajouter_au_panier'),
    path('panier/supprimer/<int:menu_id>/', views.supprimer_du_panier, name='supprimer_du_panier'),
    path('panier/vider/', views.vider_panier, name='vider_panier'),
    path('panier/count/', views.get_cart_count, name='get_cart_count'),
    path('panier/modal/', views.cart_modal_content, name='cart_modal_content'),
]