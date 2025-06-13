import os
import django
import csv

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bonappetit.settings')
django.setup()

from menus.models import Categorie, Menu
from commandes.models import Commande, LigneCommande
from django.contrib.auth.models import User

# Export des catégories
with open('categories_export.csv', 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['id_categorie', 'nom', 'description', 'ordre_affichage'])
    for cat in Categorie.objects.all():
        writer.writerow([cat.id_categorie, cat.nom, cat.description, cat.ordre_affichage])

# Export des menus
with open('menus_export.csv', 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['id_menu', 'nom', 'description', 'prix', 'image', 'categorie_id'])
    for menu in Menu.objects.all():
        writer.writerow([menu.id_menu, menu.nom, menu.description, menu.prix, menu.image, menu.categorie_id])

# Export des commandes
with open('commandes_export.csv', 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['id', 'date_commande', 'etat', 'client_id'])
    for cmd in Commande.objects.all():
        writer.writerow([cmd.id, cmd.date_commande, cmd.etat, cmd.client_id])

# Export des lignes de commande
with open('lignes_commande_export.csv', 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['id', 'quantite', 'commande_id', 'menu_id'])
    for ligne in LigneCommande.objects.all():
        writer.writerow([ligne.id, ligne.quantite, ligne.commande_id, ligne.menu_id])

print("Export terminé avec succès!") 