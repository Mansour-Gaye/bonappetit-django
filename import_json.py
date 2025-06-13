import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bonappetit.settings')
django.setup()

from django.core import serializers
from django.db import transaction
from menus.models import Categorie, Menu
from commandes.models import Commande, LigneCommande

def import_data():
    try:
        with transaction.atomic():
            # Vider les tables existantes
            LigneCommande.objects.all().delete()
            Commande.objects.all().delete()
            Menu.objects.all().delete()
            Categorie.objects.all().delete()

            # Import des catégories
            with open('categories.json', 'r', encoding='utf-8') as f:
                for obj in serializers.deserialize('json', f.read()):
                    obj.save()

            # Import des menus
            with open('menus.json', 'r', encoding='utf-8') as f:
                for obj in serializers.deserialize('json', f.read()):
                    obj.save()

            # Import des commandes
            with open('commandes.json', 'r', encoding='utf-8') as f:
                for obj in serializers.deserialize('json', f.read()):
                    obj.save()

            # Import des lignes de commande
            with open('lignes_commande.json', 'r', encoding='utf-8') as f:
                for obj in serializers.deserialize('json', f.read()):
                    obj.save()

        print("Import terminé avec succès!")
    except Exception as e:
        print(f"Erreur lors de l'import : {str(e)}")

if __name__ == '__main__':
    import_data() 