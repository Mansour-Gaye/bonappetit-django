from django.urls import path
from . import views
# Import LogoutView for class-based logout, or use the custom user_logout function view
from django.contrib.auth.views import LogoutView

app_name = 'comptes' # This is good practice for namespacing

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    # Using the custom user_logout view:
    path('logout/', views.user_logout, name='logout'),
    # Alternatively, using Django's built-in LogoutView:
    # path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('home/', views.home, name='home'), # Assuming 'home' is also part of 'comptes' app
]
