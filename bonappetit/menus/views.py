from django.shortcuts import render, get_object_or_404
from .models import Menu, Categorie

# Create your views here.
def menu(request):
    menus = Menu.objects.all().select_related('categorie').order_by('categorie__ordre_affichage', 'nom')
    categories = Categorie.objects.all().order_by('ordre_affichage')
    
    context = {
        'menus': menus,
        'categories': categories
    }
    return render(request, 'menus/menu.html', context)

def detail_menu(request, id_menu):
    menu = get_object_or_404(Menu, id_menu=id_menu)
    context = {
        'menu': menu
    }
    return render(request, 'menus/detail_menu.html', context)
