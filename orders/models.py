from django.db import models
from django.conf import settings  

class Produit(models.Model):
    nom = models.CharField(max_length=255)
    image = models.URLField(blank=True, null=True)
    localisation = models.CharField(max_length=255)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    taille = models.CharField(max_length=10, choices=[('pm', 'Petite'), ('gm', 'Grande')])

    def __str__(self):
        return self.nom

class Panier(models.Model):
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    session_key = models.CharField(max_length=40, blank=True, null=True)  # Ajout pour panier anonyme
    produits = models.ManyToManyField(Produit, through='PanierProduit')

    def __str__(self):
        return f"Panier de {self.utilisateur if self.utilisateur else 'Utilisateur anonyme'}"

class PanierProduit(models.Model):
    panier = models.ForeignKey(Panier, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)
    date_ajout = models.DateTimeField(auto_now_add=True)

class Commande(models.Model):
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    produits = models.ManyToManyField(Produit, through='CommandeProduit')
    date_commande = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=10, choices=[('en cours', 'En cours'), ('livré', 'Livré')], default='en cours')

    def __str__(self):
        return f"Commande {self.id} - {self.utilisateur if self.utilisateur else 'Utilisateur anonyme'}"

class CommandeProduit(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()
