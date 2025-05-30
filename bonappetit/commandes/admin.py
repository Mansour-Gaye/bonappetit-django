from django.contrib import admin
from .models import Commande, LigneCommande, HistoriqueCommande

class LigneCommandeInline(admin.TabularInline):
    model = LigneCommande
    extra = 1

class HistoriqueCommandeInline(admin.TabularInline):
    model = HistoriqueCommande
    extra = 0
    readonly_fields = ('date_changement',)

@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = ('numero_commande', 'client', 'date_commande', 'montant_total', 'etat')
    list_filter = ('etat', 'date_commande')
    search_fields = ('numero_commande', 'client__username')
    inlines = [LigneCommandeInline, HistoriqueCommandeInline]
    actions = ['marquer_comme_prete']

    def marquer_comme_prete(self, request, queryset):
        queryset.update(etat='pret')
    marquer_comme_prete.short_description = "Marquer les commandes sélectionnées comme prêtes"