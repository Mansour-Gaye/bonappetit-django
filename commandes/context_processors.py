from .models import Commande

def cart_item_count(request):
    """
    Rend le nombre d'articles dans le panier disponible pour tous les templates.
    Le panier est stocké dans la session.
    """
    panier = request.session.get('panier', {})
    count = sum(panier.values())
    return {'cart_item_count': count}