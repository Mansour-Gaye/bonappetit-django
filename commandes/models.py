from django.db import models
from menus.models import Menu
from comptes.models import CustomUser

class Commande(models.Model):
    ETAT_CHOICES = [
        ('EN_ATTENTE', 'En attente'),
        ('EN_PREPARATION', 'En préparation'),
        ('PRETE', 'Prête à retirer'),
        ('ANNULEE', 'Annulée'),
    ]

    # Champ CONFIRMÉ (doit apparaître)
    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_commande = models.DateTimeField(auto_now_add=True, verbose_name="Date de commande")  # <-- Modification clé ici
    etat = models.CharField(max_length=20, choices=ETAT_CHOICES, default='EN_ATTENTE')

    def __str__(self):
        return f"Commande #{self.id} - {self.client.username}"

class LigneCommande(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE, related_name="lignes")
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)

    @property
    def date_commande(self):
        return self.commande.date_commande
    def __str__(self):
        return f"{self.quantite}x {self.menu.nom}"