from django.urls import path
from . import views

app_name = 'menus'

urlpatterns = [
    path('', views.menu, name='menu'),
    path('<int:id_menu>/', views.detail_menu, name='detail_menu'),
    path('<int:id_menu>/ajouter/', views.ajouter_au_panier, name='ajouter_au_panier'),
]

