from django import template

register = template.Library()

@register.filter
def filter_by_categorie(menus, categorie):
    """Filtre les menus par catégorie"""
    return [menu for menu in menus if menu.categorie == categorie] 