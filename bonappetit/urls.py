"""
URL configuration for bonappetit project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from comptes.views import mark_all_notifications_read

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('comptes.urls')),  # Include comptes URLs at root level
    path('menu/', include('menus.urls')),
    path('commandes/', include('commandes.urls')),  # Commandes app URLs
    path('notifications/mark_all_read/', mark_all_notifications_read, name='mark_all_notifications_read'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)