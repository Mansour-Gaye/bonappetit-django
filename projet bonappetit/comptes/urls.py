from django.urls import path
from django.contrib.auth import views as auth_views
from . import views # We'll create a placeholder registration view
from .views import profile # Import the profile view

app_name = 'comptes'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='comptes/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'), # Redirect to home after logout
    # Placeholder for registration view, assuming a view named 'register' will be created
    path('register/', views.register, name='register'),
    path('profile/', profile, name='profile'),
]
