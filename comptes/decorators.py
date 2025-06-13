from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def gestionnaire_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Vous devez être connecté pour accéder à cette page.")
            return redirect('comptes:login')
        if not request.user.is_gestionnaire:
            messages.error(request, "Vous n'avez pas les droits nécessaires pour accéder à cette page.")
            return redirect('comptes:mon_compte')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# Nouveau décorateur pour restreindre l'accès aux clients uniquement

def client_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Vous devez être connecté pour accéder à cette page.")
            return redirect('comptes:login')
        if getattr(request.user, 'is_gestionnaire', False):
            messages.error(request, "Accès réservé aux clients.")
            return redirect('comptes:gestionnaire_dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped_view 