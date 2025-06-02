from django.urls import path
from . import views

urlpatterns = [
    path('menu/', views.menu, name='menu'),
    path('menu/<int:id_menu>/', views.detail_menu, name='detail_menu'),
]

