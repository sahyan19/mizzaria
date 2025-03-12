from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.conf import settings
from .models import Produit, Panier, PanierProduit, Commande, CommandeProduit
from .serializers import ProduitSerializer, PanierSerializer, CommandeSerializer

class PanierViewSet(viewsets.ViewSet):
    def get_panier(self, request):
        """ Récupère ou crée un panier, même pour un utilisateur non connecté """
        if request.user.is_authenticated:
            panier, _ = Panier.objects.get_or_create(utilisateur=request.user)
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
            panier, _ = Panier.objects.get_or_create(session_key=request.session.session_key, utilisateur=None)
        return panier

    @action(detail=False, methods=['post'])
    def add_pizza_to_card(self, request):
        data = request.data
        panier = self.get_panier(request)

        produit, _ = Produit.objects.get_or_create(
            nom=data['nom'], localisation=data['localisation'],
            image=data.get('image', ''), prix=data['prix'], taille=data['taille']
        )

        panier_produit, created = PanierProduit.objects.get_or_create(
            panier=panier, produit=produit
        )
        panier_produit.quantite = data['quantite']
        panier_produit.save()

        return Response({"status": True}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def delete_pizza_from_card(self, request):
        data = request.data
        panier = self.get_panier(request)

        produit = Produit.objects.filter(
            nom=data['nom'], localisation=data['localisation'], prix=data['prix'], taille=data['taille']
        ).first()

        if produit:
            PanierProduit.objects.filter(panier=panier, produit=produit).delete()

        return Response({"status": True})

    @action(detail=False, methods=['post'])
    @action(detail=False, methods=['post'])
    def update_pizza_from_card(self, request):
        data = request.data
        panier = self.get_panier(request)

        produit = Produit.objects.filter(
            nom=data['nom'], localisation=data['localisation'], prix=data['prix'], taille=data['taille']
        ).first()

        if produit:
            panier_produit = PanierProduit.objects.filter(panier=panier, produit=produit).first()
            if panier_produit:
                if data['quantite'] == 0:
                    # Supprimer le produit si la quantité est mise à 0
                    panier_produit.delete()
                    return Response({"status": True, "message": "Produit supprimé du panier"}, status=status.HTTP_200_OK)
                
                panier_produit.quantite = data['quantite']
                panier_produit.save()
                return Response({"status": True, "message": "Quantité mise à jour"}, status=status.HTTP_200_OK)

        return Response({"status": False, "message": "Produit non trouvé"}, status=status.HTTP_404_NOT_FOUND)


    @action(detail=False, methods=['get'])
    def read_card(self, request):
        panier = self.get_panier(request)
        serializer = PanierSerializer(panier)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def order(self, request):
        panier = self.get_panier(request)
        if panier:
            utilisateur = request.user if request.user.is_authenticated else None
            commande = Commande.objects.create(utilisateur=utilisateur)

            for panier_produit in PanierProduit.objects.filter(panier=panier):
                CommandeProduit.objects.create(
                    commande=commande, produit=panier_produit.produit, quantite=panier_produit.quantite
                )
            
            PanierProduit.objects.filter(panier=panier).delete()

        return Response({"status": True})

    @action(detail=False, methods=['get'])
    def order_history(self, request):
        """
        Récupère l'historique des commandes :
        - Si l'utilisateur est connecté, retourne son historique.
        - Si `all` est passé en paramètre, retourne toutes les commandes.
        """
        show_all = request.query_params.get('all', None) == 'true'

        if show_all:
            commandes = Commande.objects.all()
        elif request.user.is_authenticated:
            commandes = Commande.objects.filter(utilisateur=request.user)
        else:
            return Response({"status": False, "message": "Connectez-vous pour voir votre historique."}, status=status.HTTP_403_FORBIDDEN)

        # Construction de la réponse avec les noms des utilisateurs
        historique = []
        for commande in commandes:
            produits = [
                {"nom": cp.produit.nom, "quantite": cp.quantite}
                for cp in CommandeProduit.objects.filter(commande=commande)
            ]
            historique.append({
                "id_commande": commande.id,
                "utilisateur": commande.utilisateur.username if commande.utilisateur else "Utilisateur anonyme",
                "date_commande": commande.date_commande.strftime("%Y-%m-%d %H:%M"),
                "statut": commande.statut,
                "produits": produits
            })

        return Response(historique, status=status.HTTP_200_OK)
