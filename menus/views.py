# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Menu, Categorie

# Create your views here.
def menu(request):
    categories = Categorie.objects.all().order_by('ordre_affichage')
    categorie_id = request.GET.get('categorie')
    categorie_active = None
    
    if categorie_id:
        menus = Menu.objects.filter(categorie__id_categorie=categorie_id).select_related('categorie').order_by('nom')
        categorie_active = get_object_or_404(Categorie, id_categorie=categorie_id)
    else:
        menus = Menu.objects.all().select_related('categorie').order_by('categorie__ordre_affichage', 'nom')
    
    context = {
        'menus': menus,
        'categories': categories,
        'categorie_active': categorie_active
    }
    return render(request, 'menus/menu.html', context)

def detail_menu(request, id_menu):
    menu = get_object_or_404(Menu, id_menu=id_menu)
    context = {
        'menu': menu
    }
    return render(request, 'menus/detail_menu.html', context)

@login_required(login_url='comptes:login')
def ajouter_au_panier(request, id_menu):
    menu = get_object_or_404(Menu, id_menu=id_menu)
    # Ici, vous pouvez ajouter la logique pour ajouter au panier
    # Pour l'instant, on redirige vers la page du menu avec un message
    messages.success(request, f'Le menu "{menu.nom}" a été ajouté à votre panier.')
    return redirect('menus:menu')
