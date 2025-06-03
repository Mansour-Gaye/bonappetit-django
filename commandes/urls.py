from django.urls import path
from . import views

urlpatterns = [
    path('creer/', views.creer_commande, name='creer_commande'),
    path('mes-commandes/', views.liste_commandes, name='liste_commandes'),
    path('modifier/<int:pk>/', views.modifier_commande, name='modifier_commande'),
]