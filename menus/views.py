# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from comptes.decorators import gestionnaire_required, client_required
from .models import Menu, Categorie
from .forms import MenuForm, CategorieForm
import logging

logger = logging.getLogger(__name__)

def detail_menu(request, id_menu):
    menu = get_object_or_404(Menu, id_menu=id_menu)
    
    # Récupérer les menus précédent et suivant
    all_menus = Menu.objects.filter(disponible=True).order_by('id_menu')
    menu_index = list(all_menus).index(menu)
    
    previous_menu = None
    next_menu = None
    
    if menu_index > 0:
        previous_menu = all_menus[menu_index - 1]
    if menu_index < len(all_menus) - 1:
        next_menu = all_menus[menu_index + 1]
    
    # Récupérer les menus liés (même catégorie, excluant le menu actuel)
    related_menus = Menu.objects.filter(
        categorie=menu.categorie,
        disponible=True
    ).exclude(id_menu=menu.id_menu).order_by('?')[:4]
    
    context = {
        'menu': menu,
        'previous_menu': previous_menu,
        'next_menu': next_menu,
        'related_menus': related_menus
    }
    return render(request, 'menus/detail_menu_restaurantly.html', context)

@login_required(login_url='comptes:login')
def ajouter_au_panier(request, id_menu):
    menu = get_object_or_404(Menu, id_menu=id_menu)
    # Ici, vous pouvez ajouter la logique pour ajouter au panier
    # Pour l'instant, on redirige vers la page du menu avec un message
    messages.success(request, f'Le menu "{menu.nom}" a été ajouté à votre panier.')
    return redirect('menus:menu')

# Vue publique pour lister les menus
def liste_menus(request):
    # Log tous les menus avant le filtre
    all_menus = Menu.objects.all()
    logger.info(f"Nombre total de menus: {all_menus.count()}")
    for menu in all_menus:
        logger.info(f"Menu {menu.id_menu}: {menu.nom} - Disponible: {menu.disponible}")
    
    menus = Menu.objects.filter(disponible=True).select_related('categorie')
    logger.info(f"Nombre de menus disponibles: {menus.count()}")
    
    categories = Categorie.objects.all().order_by('ordre_affichage')
    logger.info(f"Nombre de catégories: {categories.count()}")
    
    # Filtrage par catégorie
    categorie_id = request.GET.get('categorie')
    categorie_active = None
    if categorie_id:
        try:
            categorie_active = Categorie.objects.get(id_categorie=categorie_id)
            menus = menus.filter(categorie=categorie_active)
            logger.info(f"Filtrage par catégorie {categorie_id}: {menus.count()} menus")
        except Categorie.DoesNotExist:
            logger.warning(f"Catégorie {categorie_id} non trouvée")
            pass
    
    # Pagination avec un nombre plus élevé de menus par page
    paginator = Paginator(menus, 50)  # Augmenté de 12 à 50 menus par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'menus': page_obj,
        'categories': categories,
        'categorie_active': categorie_active,
    }
    return render(request, 'menus/liste_menus_restaurantly.html', context)

# Vues gestionnaire
@login_required
@gestionnaire_required
def gestion_menus(request):
    menus = Menu.objects.all().select_related('categorie').order_by('-date_creation')
    categories = Categorie.objects.all().order_by('ordre_affichage')
    
    # Recherche
    search = request.GET.get('search')
    if search:
        menus = menus.filter(
            Q(nom__icontains=search) |
            Q(description__icontains=search)
        )
    
    # Filtrage par catégorie
    categorie_id = request.GET.get('categorie')
    if categorie_id:
        menus = menus.filter(categorie_id=categorie_id)
    
    # Pagination
    paginator = Paginator(menus, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'search': search,
        'categorie_selectionnee': int(categorie_id) if categorie_id else None,
    }
    return render(request, 'menus/gestion_menus.html', context)

@login_required
@gestionnaire_required
def ajouter_menu(request):
    if request.method == 'POST':
        form = MenuForm(request.POST, request.FILES)
        if form.is_valid():
            menu = form.save()
            messages.success(request, f'Le menu "{menu.nom}" a été créé avec succès!')
            return redirect('menus:gestion_menus')
    else:
        form = MenuForm()
    
    return render(request, 'menus/ajouter_menu.html', {'form': form})

@login_required
@gestionnaire_required
def modifier_menu(request, menu_id):
    menu = get_object_or_404(Menu, id_menu=menu_id)
    
    if request.method == 'POST':
        form = MenuForm(request.POST, request.FILES, instance=menu)
        if form.is_valid():
            menu = form.save()
            messages.success(request, f'Le menu "{menu.nom}" a été modifié avec succès!')
            return redirect('menus:gestion_menus')
    else:
        form = MenuForm(instance=menu)
    
    return render(request, 'menus/modifier_menu.html', {'form': form, 'menu': menu})

@login_required
@gestionnaire_required
def supprimer_menu(request, menu_id):
    menu = get_object_or_404(Menu, id_menu=menu_id)
    
    if request.method == 'POST':
        nom_menu = menu.nom
        menu.delete()
        messages.success(request, f'Le menu "{nom_menu}" a été supprimé avec succès!')
        return redirect('menus:gestion_menus')
    
    return render(request, 'menus/supprimer_menu.html', {'menu': menu})

@login_required
@gestionnaire_required
def toggle_disponibilite(request, menu_id):
    menu = get_object_or_404(Menu, id_menu=menu_id)
    menu.disponible = not menu.disponible
    menu.save()
    
    statut = "disponible" if menu.disponible else "indisponible"
    messages.success(request, f'Le menu "{menu.nom}" est maintenant {statut}.')
    return redirect('menus:gestion_menus')

# Vues pour les catégories
@login_required
@gestionnaire_required
def gestion_categories(request):
    categories = Categorie.objects.all().order_by('ordre_affichage')
    return render(request, 'menus/gestion_categories.html', {'categories': categories})

@login_required
@gestionnaire_required
def ajouter_categorie(request):
    if request.method == 'POST':
        form = CategorieForm(request.POST)
        if form.is_valid():
            categorie = form.save()
            messages.success(request, f'La catégorie "{categorie.nom}" a été créée avec succès!')
            return redirect('menus:gestion_categories')
    else:
        form = CategorieForm()
    
    return render(request, 'menus/ajouter_categorie.html', {'form': form})

@login_required
@gestionnaire_required
def modifier_categorie(request, categorie_id):
    categorie = get_object_or_404(Categorie, id_categorie=categorie_id)
    
    if request.method == 'POST':
        form = CategorieForm(request.POST, instance=categorie)
        if form.is_valid():
            categorie = form.save()
            messages.success(request, f'La catégorie "{categorie.nom}" a été modifiée avec succès!')
            return redirect('menus:gestion_categories')
    else:
        form = CategorieForm(instance=categorie)
    
    return render(request, 'menus/modifier_categorie.html', {'form': form, 'categorie': categorie})

@login_required
@gestionnaire_required
def supprimer_categorie(request, categorie_id):
    categorie = get_object_or_404(Categorie, id_categorie=categorie_id)
    
    # Vérifier s'il y a des menus dans cette catégorie
    if Menu.objects.filter(categorie=categorie).exists():
        messages.error(request, f'Impossible de supprimer la catégorie "{categorie.nom}" car elle contient des menus.')
        return redirect('menus:gestion_categories')
    
    if request.method == 'POST':
        nom_categorie = categorie.nom
        categorie.delete()
        messages.success(request, f'La catégorie "{nom_categorie}" a été supprimée avec succès!')
        return redirect('menus:gestion_categories')
    
    return render(request, 'menus/supprimer_categorie.html', {'categorie': categorie})
