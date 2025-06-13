import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bonappetit.settings')
django.setup()

from django.core import serializers
from menus.models import Categorie, Menu
from commandes.models import Commande, LigneCommande

# Export des catégories
categories = serializers.serialize('json', Categorie.objects.all(), ensure_ascii=False, indent=2)
with open('categories.json', 'w', encoding='utf-8') as f:
    f.write(categories)

# Export des menus
menus = serializers.serialize('json', Menu.objects.all(), ensure_ascii=False, indent=2)
with open('menus.json', 'w', encoding='utf-8') as f:
    f.write(menus)

# Export des commandes
commandes = serializers.serialize('json', Commande.objects.all(), ensure_ascii=False, indent=2)
with open('commandes.json', 'w', encoding='utf-8') as f:
    f.write(commandes)

# Export des lignes de commande
lignes = serializers.serialize('json', LigneCommande.objects.all(), ensure_ascii=False, indent=2)
with open('lignes_commande.json', 'w', encoding='utf-8') as f:
    f.write(lignes)

print("Export JSON terminé avec succès!") 