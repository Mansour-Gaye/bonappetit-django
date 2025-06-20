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
from comptes.views import home # This line might become redundant if home is only accessed via comptes.urls
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'), # Root home page
    path('comptes/', include('comptes.urls')), # Authentication app URLs
    path('menu/', include('menus.urls')),
    path('commandes/', include('commandes.urls')), # Commandes app URLs
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)