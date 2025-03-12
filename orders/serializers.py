from rest_framework import serializers
from .models import Produit, Panier, PanierProduit, Commande, CommandeProduit

class ProduitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produit
        fields = '__all__'

class PanierProduitSerializer(serializers.ModelSerializer):
    produit = ProduitSerializer()

    class Meta:
        model = PanierProduit
        fields = ['produit', 'quantite']

class PanierSerializer(serializers.ModelSerializer):
    produits = PanierProduitSerializer(source='panierproduit_set', many=True)

    class Meta:
        model = Panier
        fields = ['utilisateur', 'produits']

class CommandeProduitSerializer(serializers.ModelSerializer):
    produit = ProduitSerializer()

    class Meta:
        model = CommandeProduit
        fields = ['produit', 'quantite']

class CommandeSerializer(serializers.ModelSerializer):
    produits = CommandeProduitSerializer(source='commandeproduit_set', many=True)

    class Meta:
        model = Commande
        fields = ['utilisateur', 'date_commande', 'statut', 'produits']
