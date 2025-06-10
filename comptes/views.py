from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import CustomUserCreationForm
from django.contrib import messages
from .models import Notification # Notification model might be needed if we add "mark as read" functionality here later

# ... (is_gestionnaire_check, mon_compte_view, gestionnaire_dashboard_view) ...

def home(request):
    if request.user.is_authenticated:
        if request.user.is_gestionnaire:
            return redirect('comptes:gestionnaire_dashboard')
        else:
            return redirect('comptes:mon_compte')
    else:
        # For unauthenticated users, redirect to login page
        return redirect('comptes:login')

@login_required
def profile(request):
    return render(request, 'comptes/profile.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Log the user in directly
            messages.success(request, "Inscription réussie. Vous êtes maintenant connecté.")
            # Role-based redirection
            if user.is_gestionnaire: # This assumes is_gestionnaire could be set at registration
                                     # If not, it will always go to mon_compte for new users
                return redirect('comptes:gestionnaire_dashboard')
            else:
                return redirect('comptes:mon_compte')
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
                if user.is_gestionnaire:
                    return redirect('comptes:gestionnaire_dashboard')
                else:
                    return redirect('comptes:mon_compte')
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
    # Redirect to the login page after logout
    return redirect('comptes:login')

# Add new views for mon_compte and gestionnaire_dashboard

@login_required
def mon_compte_view(request):
    # Fetch unread notifications for the logged-in user
    unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
    # For simplicity, we're not fetching order history yet, as per original plan focus
    context = {
        'unread_notifications': unread_notifications
    }
    return render(request, 'comptes/mon_compte.html', context)

def is_gestionnaire_check(user):
    return user.is_authenticated and user.is_gestionnaire

@login_required
@user_passes_test(is_gestionnaire_check, login_url='comptes:login') # Or a custom access denied page
def gestionnaire_dashboard_view(request):
    # Later, this view will fetch stats
    return render(request, 'comptes/gestionnaire/dashboard.html')