from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db import transaction
from .models import Commande, LigneCommande
from menus.models import Menu, Categorie
from comptes.models import Notification, CustomUser
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
            # Notifications client (persistantes)
            client = commande.client
            notif_msg = None
            notif_type = 'commande'
            notif_icon = 'fas fa-bell'
            if new_status == 'EN_PREPARATION':
                notif_msg = f"Votre commande #{commande.id} est en cours de préparation."
                notif_icon = 'fas fa-hourglass-half'
            elif new_status == 'PRETE':
                notif_msg = f"Votre commande #{commande.id} est prête à être retirée !"
                notif_icon = 'fas fa-check-circle'
            elif new_status == 'RETIREE':
                notif_msg = f"Merci d'avoir retiré votre commande #{commande.id}."
                notif_icon = 'fas fa-box-open'
            elif new_status == 'ANNULEE':
                notif_msg = f"Votre commande #{commande.id} a été annulée."
                notif_icon = 'fas fa-times-circle'
            elif new_status == 'CONFIRMEE':
                notif_msg = f"Votre commande #{commande.id} a été confirmée."
                notif_icon = 'fas fa-clipboard-check'
            if notif_msg:
                Notification.create_notification(user=client, message=notif_msg, type_notification=notif_type, icon=notif_icon)
            # Notifications gestionnaire (persistantes)
            if new_status == 'EN_ATTENTE':
                for gestionnaire in CustomUser.objects.filter(is_gestionnaire=True):
                    Notification.create_notification(user=gestionnaire, message=f"Nouvelle commande #{commande.id} reçue de {commande.client.username}.", type_notification='commande', icon='fas fa-shopping-cart')
            elif new_status == 'ANNULEE':
                for gestionnaire in CustomUser.objects.filter(is_gestionnaire=True):
                    Notification.create_notification(user=gestionnaire, message=f"La commande #{commande.id} a été annulée par {commande.client.username}.", type_notification='commande', icon='fas fa-times-circle')
            # Feedback immédiat (messages Django)
            if notif_msg:
                messages.info(request, notif_msg)
            return redirect('commandes:list_all_commandes')
        else:
            messages.error(request, "Statut invalide.")
    return redirect('commandes:list_all_commandes')

@client_required
@login_required
def liste_commandes(request):
    commandes = Commande.objects.filter(
        client=request.user,
        etat__in=['EN_ATTENTE', 'EN_PREPARATION', 'PRETE']
    ).prefetch_related('lignes').order_by('-date_commande')
    return render(request, 'commandes/liste_commandes.html', {'commandes': commandes})

@client_required
@login_required
def historique_commandes(request):
    commandes = Commande.objects.filter(
        client=request.user,
        etat__in=['RETIREE', 'ANNULEE']
    ).prefetch_related('lignes').order_by('-date_commande')
    return render(request, 'commandes/historique_commandes.html', {'commandes': commandes})

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

def ajouter_au_panier(request, menu_id):
    if request.method == 'POST':
        panier = request.session.get('panier', {})
        try:
            quantite = int(request.POST.get('quantite', 1))
            if quantite <= 0:
                quantite = 1
        except (ValueError, TypeError):
            quantite = 1
        menu_id = str(menu_id)
        panier[menu_id] = panier.get(menu_id, 0) + quantite
        request.session['panier'] = panier
        cart_count = sum(panier.values())
        return JsonResponse({'status': 'success', 'message': 'Article ajouté!', 'cart_count': cart_count})
    return JsonResponse({'status': 'error', 'message': 'Requête invalide'}, status=400)

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
        commande = Commande.objects.create(
            client=request.user,
            date_commande=timezone.now(),
            etat='EN_ATTENTE',
            montant_total=0
        )
        montant_total = 0
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
        commande.montant_total = montant_total
        commande.save()
        del request.session['panier']
        messages.success(request, "Votre commande a été enregistrée avec succès.")
        # Notifier tous les gestionnaires d'une nouvelle commande
        for gestionnaire in CustomUser.objects.filter(is_gestionnaire=True):
            Notification.create_notification(user=gestionnaire, message=f"Nouvelle commande #{commande.id} reçue de {request.user.username}.", type_notification='commande', icon='fas fa-shopping-cart')
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

@login_required(login_url='comptes:login')
def detail_commande(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)
    if not request.user.is_staff and commande.client != request.user:
        messages.error(request, "Vous n'êtes pas autorisé à voir cette commande.")
        return redirect('commandes:liste_commandes')
    lignes = LigneCommande.objects.filter(commande=commande).select_related('menu')
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
@login_required(login_url='comptes:login')
def annuler_commande(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)
    if commande.client != request.user:
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
    # Notification client (persistante)
    Notification.create_notification(user=request.user, message=f"Votre commande #{commande.id} a été annulée.", type_notification='commande', icon='fas fa-times-circle')
    # Notification gestionnaire (persistante)
    for gestionnaire in CustomUser.objects.filter(is_gestionnaire=True):
        Notification.create_notification(user=gestionnaire, message=f"La commande #{commande.id} a été annulée par {request.user.username}.", type_notification='commande', icon='fas fa-times-circle')
    messages.success(request, f"Votre commande #{commande.id} a été annulée.")
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': f"Commande #{commande.id} annulée."})
    return redirect('commandes:detail_commande', commande_id=commande.id)

@login_required(login_url='comptes:login')
def confirmer_commande(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)
    if not request.user.is_staff and commande.client != request.user:
        messages.error(request, "Vous n'êtes pas autorisé à confirmer cette commande.")
        return redirect('commandes:liste_commandes')
    if commande.etat != 'EN_ATTENTE':
        messages.error(request, "Cette commande ne peut plus être confirmée.")
        return redirect('commandes:detail_commande', commande_id=commande.id)
    commande.etat = 'CONFIRMEE'
    commande.save()
    messages.success(request, "Votre commande a bien été confirmée. Elle sera traitée dans les plus brefs délais.")
    return redirect('commandes:detail_commande', commande_id=commande.id)

def get_cart_count(request):
    panier = request.session.get('panier', {})
    count = sum(panier.values())
    return JsonResponse({'count': count})

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
    
    return render(request, 'commandes/partials/cart_modal_content.html', {
        'items': items,
        'total': total
    })

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

def update_cart_item(request, menu_id):
    panier = request.session.get('panier', {})
    menu_id = str(menu_id)
    
    try:
        data = json.loads(request.body)
        action = data.get('action')

        if action == 'increase':
            panier[menu_id] = panier.get(menu_id, 0) + 1
        elif action == 'decrease':
            panier[menu_id] = panier.get(menu_id, 0) - 1
            if panier[menu_id] <= 0:
                del panier[menu_id]
        
        request.session['panier'] = panier
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

def remove_cart_item(request, menu_id):
    panier = request.session.get('panier', {})
    menu_id = str(menu_id)
    
    if menu_id in panier:
        del panier[menu_id]
        request.session['panier'] = panier
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Article non trouvé'}, status=404)
