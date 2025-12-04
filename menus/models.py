from django.db import models
from django.utils.text import slugify

# Create your models here.
class Categorie(models.Model):
    id_categorie = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    ordre_affichage = models.PositiveIntegerField(default=0, help_text="Ordre d'affichage de la catégorie")

    def get_slug(self):
        return slugify(self.nom)

    class Meta:
        ordering = ['ordre_affichage', 'nom']

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


