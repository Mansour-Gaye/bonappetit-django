from django.urls import path
from . import views

app_name = 'comptes'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('mon-compte/', views.mon_compte_view, name='mon_compte'),
    
    # URLs pour les gestionnaires
    path('gestionnaire/dashboard/', views.gestionnaire_dashboard, name='gestionnaire_dashboard'),
    path('gestionnaire/utilisateurs/', views.gestion_utilisateurs, name='gestion_utilisateurs'),
    path('gestionnaire/utilisateurs/<int:user_id>/edit/', views.edit_user, name='edit_user'),
    path('gestionnaire/utilisateurs/<int:user_id>/promote/', views.promote_user, name='promote_user'),
    path('gestionnaire/utilisateurs/<int:user_id>/delete/', views.delete_user, name='delete_user'),
]
