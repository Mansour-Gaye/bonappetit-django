from django.core.management.base import BaseCommand
from menus.models import Menu, Categorie
from decimal import Decimal
from django.db import transaction

class Command(BaseCommand):
    help = 'Crée les menus du restaurant'

    def handle(self, *args, **kwargs):
        try:
            with transaction.atomic():
                # Création des catégories
                self.stdout.write('Création des catégories...')
                plats, created = Categorie.objects.get_or_create(
                    nom="Plats",
                    defaults={'description': "Nos plats principaux, préparés avec soin"}
                )
                self.stdout.write(f'Catégorie Plats {"créée" if created else "existante"}')
                
                desserts, created = Categorie.objects.get_or_create(
                    nom="Desserts",
                    defaults={'description': "Nos délicieux desserts maison"}
                )
                self.stdout.write(f'Catégorie Desserts {"créée" if created else "existante"}')
                
                boissons, created = Categorie.objects.get_or_create(
                    nom="Boissons",
                    defaults={'description': "Notre sélection de boissons rafraîchissantes"}
                )
                self.stdout.write(f'Catégorie Boissons {"créée" if created else "existante"}')

                # Liste des menus à créer
                menus_data = [
                    # Plats
                    {
                        'nom': 'Burger Bon Appétit',
                        'description': 'Pain brioché, steak haché maison, cheddar fondant, salade croquante, oignons caramélisés et sauce signature.',
                        'prix': Decimal('4500'),
                        'categorie': plats
                    },
                    {
                        'nom': 'Poulet braisé + riz blanc',
                        'description': 'Demi-poulet mariné et grillé, servi avec un riz blanc parfumé et une sauce piquante à la tomate.',
                        'prix': Decimal('4000'),
                        'categorie': plats
                    },
                    {
                        'nom': 'Pasta crémeuses aux champignons',
                        'description': 'Pâtes al dente enrobées d\'une sauce onctueuse à la crème, champignons frais et parmesan.',
                        'prix': Decimal('3800'),
                        'categorie': plats
                    },
                    # Desserts
                    {
                        'nom': 'Fondant au chocolat',
                        'description': 'Un cœur coulant au chocolat noir servi tiède, accompagné d\'une boule de glace vanille.',
                        'prix': Decimal('2500'),
                        'categorie': desserts
                    },
                    {
                        'nom': 'Tarte aux fruits',
                        'description': 'Pâte sablée croustillante garnie de crème pâtissière et de fruits frais de saison.',
                        'prix': Decimal('2000'),
                        'categorie': desserts
                    },
                    {
                        'nom': 'Salade de fruits',
                        'description': 'Un mélange coloré et rafraîchissant de fruits frais découpés, servi bien frais avec une touche de jus d\'orange.',
                        'prix': Decimal('1800'),
                        'categorie': desserts
                    },
                    # Boissons
                    {
                        'nom': 'Jus de bissap / gingembre',
                        'description': 'Boissons traditionnelles fraîches, faites maison, sans conservateurs.',
                        'prix': Decimal('1000'),
                        'categorie': boissons
                    },
                    {
                        'nom': 'Soda',
                        'description': 'Servi bien frais, pour accompagner vos plats avec pétillance. (Coca-Cola, Fanta, Sprite...)',
                        'prix': Decimal('1200'),
                        'categorie': boissons
                    },
                    {
                        'nom': 'Eau minérale',
                        'description': 'Eau fraîche (plate ou gazeuse) pour une pause désaltérante.',
                        'prix': Decimal('800'),
                        'categorie': boissons
                    },
                    {
                        'nom': 'Cocktail sans alcool Bon Appétit',
                        'description': 'Mélange rafraîchissant de fruits tropicaux, servi avec glace pilée et feuilles de menthe.',
                        'prix': Decimal('2000'),
                        'categorie': boissons
                    },
                ]

                # Création des menus
                self.stdout.write('Création des menus...')
                for menu_data in menus_data:
                    menu, created = Menu.objects.get_or_create(
                        nom=menu_data['nom'],
                        defaults={
                            'description': menu_data['description'],
                            'prix': menu_data['prix'],
                            'categorie': menu_data['categorie']
                        }
                    )
                    self.stdout.write(
                        self.style.SUCCESS(f'Menu créé : {menu.nom}') if created
                        else self.style.WARNING(f'Menu existant : {menu.nom}')
                    )

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erreur lors de la création des menus : {str(e)}')) 