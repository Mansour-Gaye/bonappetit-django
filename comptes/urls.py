from django.urls import path
from . import views

app_name = 'comptes'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    # path('profile/', views.profile, name='profile'), # Consider removing if mon_compte replaces it
    path('home/', views.home, name='home'), # This will be reviewed later

    # New URLs
    path('mon_compte/', views.mon_compte_view, name='mon_compte'),
    path('gestionnaire/dashboard/', views.gestionnaire_dashboard_view, name='gestionnaire_dashboard'),
]
