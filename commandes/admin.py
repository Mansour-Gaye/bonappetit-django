from django.contrib import admin
from .models import Commande, LigneCommande

class LigneCommandeInline(admin.TabularInline):
    model = LigneCommande
    extra = 1
    fields = ('menu', 'quantite')

@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    inlines = [LigneCommandeInline]
    # Affiche TOUS les champs existants
    list_display = ('id', 'client', 'date_commande', 'etat')  
    # Active le tri par date
    list_display_links = ('id', 'date_commande')  
    # Filtres pratiques
    list_filter = ('date_commande', 'etat')  
    # Ordonner par date récente par défaut
    ordering = ('-date_commande',)  

@admin.register(LigneCommande)
class LigneCommandeAdmin(admin.ModelAdmin):
    list_display = ('id', 'commande', 'date_commande', 'menu', 'quantite')  # Ajout ici
    list_select_related = ('commande',)  # Optimisation SQL