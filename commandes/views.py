from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db import transaction
from .models import Commande, LigneCommande
from menus.models import Menu, Categorie
from comptes.models import Notification
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from django.utils import timezone
from django.db.models import Sum
from django.template.loader import render_to_string
import json
from django.views.decorators.http import require_POST
from comptes.decorators import client_required

def is_gestionnaire_check(user):
    return user.is_authenticated and user.is_gestionnaire

@login_required
@user_passes_test(is_gestionnaire_check, login_url='comptes:login')
def list_all_commandes_view(request):
    commandes = Commande.objects.all().select_related('client').order_by('-date_commande')
    etat = request.GET.get('etat')
    client = request.GET.get('client')
    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')
    if etat:
        commandes = commandes.filter(etat=etat)
    if client:
        commandes = commandes.filter(client__username__icontains=client)
    if date_min:
        commandes = commandes.filter(date_commande__date__gte=date_min)
    if date_max:
        commandes = commandes.filter(date_commande__date__lte=date_max)
    return render(request, 'commandes/gestionnaire/list_commandes.html', {
        'commandes': commandes,
        'etat': etat,
        'client': client,
        'date_min': date_min,
        'date_max': date_max,
        'ETAT_CHOICES': Commande.ETAT_CHOICES
    })

@login_required
@user_passes_test(is_gestionnaire_check, login_url='comptes:login')
def update_commande_status_view(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)
    if request.method == 'POST':
        new_status = request.POST.get('etat')
        old_status = commande.get_etat_display()
        if new_status in [choice[0] for choice in Commande.ETAT_CHOICES]:
            commande.etat = new_status
            commande.save()

            # Create notification for the client
            client_user = commande.client
            message_text = f"Le statut de votre commande #{commande.id} a été mis à jour de '{old_status}' à '{commande.get_etat_display()}'."
            Notification.objects.create(user=client_user, message=message_text)

            messages.success(request, f"Le statut de la commande #{commande.id} a été mis à jour et le client notifié.")
            return redirect('commandes:list_all_commandes')
        else:
            messages.error(request, "Statut invalide.")
    return redirect('commandes:list_all_commandes')

@client_required
@login_required
def liste_commandes(request):
    commandes = Commande.objects.filter(
        client=request.user,
        etat__in=['EN_ATTENTE', 'EN_PREPARATION']
    ).prefetch_related('lignes').order_by('-date_commande')
    return render(request, 'commandes/liste_commandes.html', {'commandes': commandes})

@client_required
@login_required
def passer_commande(request):
    if request.method == 'POST':
        menu_id = request.POST.get('menu_id')
        quantite = int(request.POST.get('quantite', 1))
        
        try:
            menu = Menu.objects.get(id_menu=menu_id)
            
            # Récupérer ou créer la commande en attente
            commande, created = Commande.objects.get_or_create(
                client=request.user,
                etat='EN_ATTENTE',
                defaults={'date_commande': timezone.now()}
            )
            
            # Vérifier si le menu est déjà dans la commande
            ligne_commande, created = LigneCommande.objects.get_or_create(
                commande=commande,
                menu=menu,
                defaults={'quantite': quantite}
            )
            
            if not created:
                ligne_commande.quantite += quantite
                ligne_commande.save()
            
            # Calculer le nouveau total du panier
            total_items = LigneCommande.objects.filter(
                commande__client=request.user,
                commande__etat='EN_ATTENTE'
            ).aggregate(total=Sum('quantite'))['total'] or 0
            
            return JsonResponse({
                'success': True,
                'message': f'{menu.nom} ajouté au panier avec succès!',
                'cart_count': total_items
            })
            
        except Menu.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Menu non trouvé.'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Une erreur est survenue: {str(e)}'
            })
    
    # GET request - afficher le formulaire
    menus = Menu.objects.all()
    return render(request, 'menus/menu.html', {'menus': menus})

@client_required
@login_required
def modifier_commande(request, pk):
    commande = get_object_or_404(Commande, pk=pk, client=request.user)
    messages.info(request, "La modification de commande n'est pas encore implémentée ou est restreinte.")
    return render(request, 'commandes/modifier_commande.html', {'commande': commande})

def calcul_total(panier):
    total = 0
    for menu_id, quantite in panier.items():
        menu = Menu.objects.get(id_menu=menu_id)
        total += menu.prix * quantite
    return total

def calcul_sous_total(menu_id, panier):
    quantite = panier.get(str(menu_id), 0)
    if quantite == 0:
        return 0
    menu = Menu.objects.get(id_menu=menu_id)
    return menu.prix * quantite

@client_required
@login_required
def voir_panier(request):
    panier = request.session.get('panier', {})
    items = []
    total = 0
    
    for menu_id, quantite in panier.items():
        try:
            menu = Menu.objects.get(id_menu=menu_id)
            sous_total = menu.prix * quantite
            items.append({
                'menu': menu,
                'quantite': quantite,
                'sous_total': sous_total
            })
            total += sous_total
        except Menu.DoesNotExist:
            continue
    
    return render(request, 'commandes/panier.html', {
        'items': items,
        'total': total
    })

@login_required
def ajouter_au_panier(request, menu_id):
    if request.method == 'POST':
        panier = request.session.get('panier', {})
        try:
            data = json.loads(request.body)
            quantite = data.get('quantite', 0)
        except Exception:
            quantite = 0
            
        menu_id = str(menu_id)
        if menu_id in panier:
            panier[menu_id] += quantite
            if panier[menu_id] <= 0:
                del panier[menu_id]
        else:
            if quantite > 0:
                panier[menu_id] = quantite
                
        request.session['panier'] = panier
        request.session.modified = True  # Important pour s'assurer que la session est sauvegardée
        
        total = calcul_total(panier)
        sous_total = calcul_sous_total(menu_id, panier)
        
        return JsonResponse({
            'success': True,
            'quantite': panier.get(menu_id, 0),
            'sous_total': sous_total,
            'total': total
        })
    return JsonResponse({'success': False, 'message': 'Méthode non autorisée.'})

@client_required
@login_required
def supprimer_du_panier(request, menu_id):
    if request.method == 'POST':
        panier = request.session.get('panier', {})
        menu_id = str(menu_id)
        if menu_id in panier:
            del panier[menu_id]
            request.session['panier'] = panier
            total = calcul_total(panier)
            return JsonResponse({
                'success': True,
                'total': total
            })
        return JsonResponse({'success': False, 'message': "L'article n'était pas dans le panier."})
    return JsonResponse({'success': False, 'message': 'Méthode non autorisée.'})

@client_required
@require_POST
@login_required
def vider_panier(request):
    if 'panier' in request.session:
        request.session['panier'] = {}
        request.session.modified = True
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'message': 'Le panier était déjà vide.'})

@client_required
@login_required
def nouvelle_commande(request):
    panier = request.session.get('panier', {})
    if not panier:
        messages.error(request, "Votre panier est vide.")
        return redirect('commandes:liste_commandes')
    
    if request.method == 'POST':
        # Créer la commande
        commande = Commande.objects.create(
            client=request.user,
            date_commande=timezone.now(),
            etat='EN_ATTENTE',
            montant_total=0  # Sera mis à jour après l'ajout des lignes
        )
        
        montant_total = 0
        
        # Ajouter les lignes de commande
        for menu_id, quantite in panier.items():
            menu = get_object_or_404(Menu, id_menu=menu_id)
            sous_total = menu.prix * quantite
            montant_total += sous_total
            
            LigneCommande.objects.create(
                commande=commande,
                menu=menu,
                quantite=quantite,
                prix_unitaire=menu.prix
            )
        
        # Mettre à jour le montant total de la commande
        commande.montant_total = montant_total
        commande.save()
        
        # Vider le panier
        del request.session['panier']
        
        messages.success(request, "Votre commande a été enregistrée avec succès.")
        return redirect('commandes:liste_commandes')
    
    # Préparer les données pour l'affichage
    items = []
    total = 0
    
    for menu_id, quantite in panier.items():
        menu = get_object_or_404(Menu, id_menu=menu_id)
        sous_total = menu.prix * quantite
        items.append({
            'menu': menu,
            'quantite': quantite,
            'sous_total': sous_total
        })
        total += sous_total
    
    return render(request, 'commandes/nouvelle_commande.html', {
        'items': items,
        'total': total
    })

@login_required
def detail_commande(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)
    
    # Vérifier si l'utilisateur est autorisé à voir cette commande
    if not request.user.is_staff and commande.client != request.user:
        messages.error(request, "Vous n'êtes pas autorisé à voir cette commande.")
        return redirect('commandes:liste_commandes')
    
    # Récupérer les lignes de commande
    lignes = LigneCommande.objects.filter(commande=commande).select_related('menu')
    
    # Préparer les données pour l'affichage
    items = []
    for ligne in lignes:
        items.append({
            'menu': ligne.menu,
            'quantite': ligne.quantite,
            'prix_unitaire': ligne.prix_unitaire,
            'sous_total': ligne.quantite * ligne.prix_unitaire
        })
    
    return render(request, 'commandes/detail_commande.html', {
        'commande': commande,
        'items': items,
        'total': commande.montant_total
    })

@require_POST
@login_required
def annuler_commande(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)
    if commande.client != request.user and not request.user.is_staff:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': "Non autorisé."}, status=403)
        messages.error(request, "Vous n'êtes pas autorisé à annuler cette commande.")
        return redirect('commandes:liste_commandes')
    if commande.etat != 'EN_ATTENTE':
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': "Cette commande ne peut plus être annulée."}, status=400)
        messages.error(request, "Cette commande ne peut plus être annulée.")
        return redirect('commandes:detail_commande', commande_id=commande.id)
    commande.etat = 'ANNULEE'
    commande.save()
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': "Commande annulée."})
    messages.success(request, "La commande a été annulée avec succès.")
    return redirect('commandes:detail_commande', commande_id=commande.id)

@login_required
def confirmer_commande(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)
    
    # Vérifier si l'utilisateur est autorisé à confirmer cette commande
    if not request.user.is_staff and commande.client != request.user:
        messages.error(request, "Vous n'êtes pas autorisé à confirmer cette commande.")
        return redirect('commandes:liste_commandes')
    
    # Vérifier si la commande peut être confirmée
    if commande.etat != 'EN_ATTENTE':
        messages.error(request, "Cette commande ne peut plus être confirmée.")
        return redirect('commandes:detail_commande', commande_id=commande.id)
    
    # Confirmer la commande
    commande.etat = 'CONFIRMEE'
    commande.save()
    
    messages.success(request, "La commande a été confirmée avec succès.")
    return redirect('commandes:detail_commande', commande_id=commande.id)

@login_required
def get_cart_count(request):
    panier = request.session.get('panier', {})
    count = sum(panier.values())
    return JsonResponse({'count': count})

@client_required
@login_required
def cart_modal_content(request):
    panier = request.session.get('panier', {})
    items = []
    total = 0
    
    for menu_id, quantite in panier.items():
        try:
            menu = Menu.objects.get(id_menu=menu_id)
            sous_total = menu.prix * quantite
            items.append({
                'menu': menu,
                'quantite': quantite,
                'sous_total': sous_total
            })
            total += sous_total
        except Menu.DoesNotExist:
            continue
    
    return render(request, 'commandes/cart_modal_content.html', {
        'items': items,
        'total': total
    })

@client_required
@login_required
def modal_panier_partial(request):
    panier = request.session.get('panier', {})
    items = []
    total = 0
    from menus.models import Menu
    for id_menu, quantite in panier.items():
        try:
            menu = Menu.objects.get(id_menu=id_menu)
            sous_total = menu.prix * quantite
            items.append({'menu': menu, 'quantite': quantite, 'sous_total': sous_total})
            total += sous_total
        except Menu.DoesNotExist:
            continue
    return render(request, 'commandes/partials/cart_modal.html', {
        'items': items,
        'total': total
    })
