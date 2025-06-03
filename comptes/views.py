from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.contrib import messages

def home(request):
    # This view might need to be adjusted or point to a different template
    # For now, assume 'comptes/home.html' is a generic landing page after login/registration
    return render(request, 'comptes/home.html')

@login_required
def profile(request):
    return render(request, 'comptes/profile.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Inscription réussie. Vous êtes maintenant connecté.")
            return redirect('comptes:home')
        else:
            # It's good practice to pass the form with errors back to the template
            messages.error(request, "Erreur d'inscription. Veuillez corriger les erreurs ci-dessous.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'comptes/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Bienvenue {username} !")
                # Default redirect is to settings.LOGIN_REDIRECT_URL, or use explicit redirect
                return redirect('comptes:home')
            else:
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
        else:
            # Form is invalid (e.g., fields missing)
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect. Veuillez vérifier les champs.")
    else:
        form = AuthenticationForm()
    return render(request, 'comptes/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.info(request, "Vous avez été déconnecté.")
    return redirect('comptes:home') # Or login page: redirect('comptes:login')