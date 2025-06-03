from django.contrib import admin

from .models import Categorie, Menu
# Register your models here.
@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('nom', 'ordre_affichage')
    search_fields = ('nom',)
    ordering = ('ordre_affichage',)

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('nom', 'categorie', 'prix', 'disponible', 'date_modification')
    list_filter = ('categorie', 'disponible')
    search_fields = ('nom', 'description')
    ordering = ('categorie__ordre_affichage', 'nom')
    list_editable = ('disponible', 'prix')
    readonly_fields = ('date_creation', 'date_modification')
    fieldsets = (
        ('Informations générales', {
            'fields': ('nom', 'description', 'categorie', 'prix')
        }),
        ('Image', {
            'fields': ('image',)
        }),
        ('Statut', {
            'fields': ('disponible',)
        }),
        ('Dates', {
            'fields': ('date_creation', 'date_modification'),
            'classes': ('collapse',)
        }),
    )

