from django.db import models

# Create your models here.
class Categorie(models.Model):
    id_categorie = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=50, unique=True, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    ordre_affichage = models.IntegerField(default=0)

    def __str__(self):
        return self.nom
    
class Menu(models.Model):
    id_menu = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=200)
    description = models.TextField()
    prix = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='menus/', null=True, blank=True)
    disponible = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)

    def __str__(self):
        return self.nom


