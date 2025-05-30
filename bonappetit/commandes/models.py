from django.db import models

class Commande(models.Model):
    ETAT_CHOICES = [
        ('attente', 'En attente'),
        ('preparation', 'En préparation'),
        ('pret', 'Prête à retirer'),
        ('retiree', 'Retirée'),
        ('annulee', 'Annulée'),
    ]
    
    # Utilisation de références sous forme de chaînes
    client = models.ForeignKey('comptes.Client', on_delete=models.CASCADE)
    numero_commande = models.CharField(max_length=20, unique=True)
    date_commande = models.DateTimeField(auto_now_add=True)
    montant_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    etat = models.CharField(max_length=20, choices=ETAT_CHOICES, default='attente')
    date_preparation = models.DateTimeField(null=True, blank=True)
    
    # Relation avec Menu via chaîne
    menus = models.ManyToManyField('menus.Menu', through='LigneCommande')
    
    def __str__(self):
        return f"Commande #{self.numero_commande}"

class LigneCommande(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE)
    menu = models.ForeignKey('menus.Menu', on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.quantite}x {self.menu.nom}"

class HistoriqueCommande(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE)
    ancien_etat = models.CharField(max_length=20)
    nouvel_etat = models.CharField(max_length=20)
    date_changement = models.DateTimeField(auto_now_add=True)
    commentaire = models.TextField(blank=True)
    
    def __str__(self):
        return f"Changement {self.ancien_etat} → {self.nouvel_etat}"