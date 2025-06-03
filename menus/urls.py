from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu, name='menu'),
    path('<int:id_menu>/', views.detail_menu, name='detail_menu'),
]

