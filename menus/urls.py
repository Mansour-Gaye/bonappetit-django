from django.urls import path
from . import views

app_name = 'menus'

urlpatterns = [
    # URLs publiques
    path('', views.liste_menus, name='menu'),
    path('detail/<int:id_menu>/', views.detail_menu, name='detail_menu'),
    path('ajouter-au-panier/<int:id_menu>/', views.ajouter_au_panier, name='ajouter_au_panier'),
    
    # URLs gestionnaire - Menus
    path('gestion/', views.gestion_menus, name='gestion_menus'),
    path('ajouter/', views.ajouter_menu, name='ajouter_menu'),
    path('modifier/<int:menu_id>/', views.modifier_menu, name='modifier_menu'),
    path('supprimer/<int:menu_id>/', views.supprimer_menu, name='supprimer_menu'),
    path('toggle/<int:menu_id>/', views.toggle_disponibilite, name='toggle_disponibilite'),
    
    # URLs gestionnaire - Catégories
    path('categories/', views.gestion_categories, name='gestion_categories'),
    path('categories/ajouter/', views.ajouter_categorie, name='ajouter_categorie'),
    path('categories/modifier/<int:categorie_id>/', views.modifier_categorie, name='modifier_categorie'),
    path('categories/supprimer/<int:categorie_id>/', views.supprimer_categorie, name='supprimer_categorie'),
]

