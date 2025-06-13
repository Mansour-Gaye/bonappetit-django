from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Sum, Avg, F, Q
from django.utils import timezone
from datetime import timedelta
from django.core.paginator import Paginator
from .forms import CustomUserCreationForm
from django.contrib import messages
from .models import Notification, CustomUser
from commandes.models import Commande, LigneCommande
from menus.models import Menu
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie

User = get_user_model()

# ... (is_gestionnaire_check, mon_compte_view, gestionnaire_dashboard_view) ...

def is_gestionnaire_check(user):
    return user.is_authenticated and user.is_gestionnaire

def home(request):
    if request.user.is_authenticated:
        if request.user.is_gestionnaire:
            return redirect('comptes:gestionnaire_dashboard')
        else:
            return redirect('comptes:mon_compte')
    else:
        return redirect('comptes:login')

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
            if user.is_gestionnaire:
                return redirect('comptes:gestionnaire_dashboard')
            else:
                return redirect('comptes:mon_compte')
        else:
            messages.error(request, "Erreur d'inscription. Veuillez corriger les erreurs ci-dessous.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'comptes/register.html', {'form': form})

@ensure_csrf_cookie
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
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': True,
                        'redirect': 'comptes:gestionnaire_dashboard' if user.is_gestionnaire else 'comptes:mon_compte'
                    })
                if user.is_gestionnaire:
                    return redirect('comptes:gestionnaire_dashboard')
                else:
                    return redirect('comptes:mon_compte')
            else:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'error': "Nom d'utilisateur ou mot de passe incorrect."
                    }, status=400)
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'error': "Nom d'utilisateur ou mot de passe incorrect. Veuillez vérifier les champs."
                }, status=400)
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect. Veuillez vérifier les champs.")
    else:
        form = AuthenticationForm()
    return render(request, 'comptes/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.info(request, "Vous avez été déconnecté.")
    return redirect('comptes:login')

# Add new views for mon_compte and gestionnaire_dashboard

@login_required
def mon_compte_view(request):
    # Récupérer les notifications non lues
    notifications = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).order_by('-created_at')
    
    # Récupérer l'historique des commandes
    commandes = Commande.objects.filter(
        client=request.user
    ).order_by('-date_commande')
    
    context = {
        'notifications': notifications,
        'commandes': commandes
    }
    return render(request, 'comptes/mon_compte.html', context)

@login_required
@user_passes_test(is_gestionnaire_check, login_url='comptes:login')
def gestionnaire_dashboard(request):
    # Période pour les statistiques (30 derniers jours)
    date_limite = timezone.now() - timedelta(days=30)
    
    # Statistiques des commandes
    commandes_stats = {
        'total': Commande.objects.count(),
        'terminees': Commande.objects.filter(etat='TERMINEE').count(),
        'en_cours': Commande.objects.filter(etat__in=['EN_PREPARATION', 'EN_ATTENTE']).count(),
        'chiffre_affaires': LigneCommande.objects.filter(
            commande__etat='TERMINEE'
        ).aggregate(
            total=Sum(F('menu__prix') * F('quantite'))
        )['total'] or 0
    }
    
    # Statistiques des utilisateurs
    users_stats = {
        'total': User.objects.count(),
        'clients': User.objects.filter(is_client=True).count(),
        'gestionnaires': User.objects.filter(is_gestionnaire=True).count(),
        'nouveaux': User.objects.filter(date_joined__gte=date_limite).count()
    }
    
    # Commandes récentes
    commandes_recentes = Commande.objects.select_related('client').prefetch_related(
        'lignes__menu'
    ).order_by('-date_commande')[:10]
    
    # Créer des notifications pour les nouvelles commandes
    notifications = []
    for commande in commandes_recentes:
        notification = {
            'icon': 'fas fa-shopping-cart',
            'message': f'Nouvelle commande #{commande.id} de {commande.client.username}',
            'created_at': commande.date_commande
        }
        notifications.append(notification)
    
    context = {
        'commandes_stats': commandes_stats,
        'users_stats': users_stats,
        'commandes_recentes': commandes_recentes,
        'notifications': notifications
    }
    
    return render(request, 'comptes/gestionnaire/dashboard.html', context)

@login_required
@user_passes_test(is_gestionnaire_check, login_url='comptes:login')
def gestion_utilisateurs(request):
    # Récupération des paramètres de filtrage
    role = request.GET.get('role', '')
    search = request.GET.get('search', '')
    
    # Base queryset
    users = CustomUser.objects.all()
    
    # Filtrage par rôle
    if role == 'client':
        users = users.filter(is_client=True)
    elif role == 'gestionnaire':
        users = users.filter(is_gestionnaire=True)
    
    # Recherche
    if search:
        users = users.filter(
            Q(username__icontains=search) |
            Q(email__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search)
        )
    
    # Pagination
    paginator = Paginator(users, 10)
    page = request.GET.get('page')
    users = paginator.get_page(page)
    
    context = {
        'users': users,
        'role': role,
        'search': search
    }
    return render(request, 'comptes/gestionnaire/gestion_utilisateurs.html', context)

@login_required
@user_passes_test(is_gestionnaire_check, login_url='comptes:login')
def edit_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        # Logique de modification de l'utilisateur
        pass
    return render(request, 'comptes/gestionnaire/edit_user.html', {'user': user})

@login_required
@user_passes_test(is_gestionnaire_check, login_url='comptes:login')
def promote_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.is_gestionnaire = True
    user.save()
    messages.success(request, f"L'utilisateur {user.username} est maintenant gestionnaire.")
    return redirect('comptes:gestion_utilisateurs')

@login_required
@user_passes_test(is_gestionnaire_check, login_url='comptes:login')
def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        username = user.username
        user.delete()
        messages.success(request, f"L'utilisateur {username} a été supprimé.")
        return redirect('comptes:gestion_utilisateurs')
    return render(request, 'comptes/gestionnaire/delete_user.html', {'user': user})