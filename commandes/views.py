from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Commande
from comptes.models import Notification # Import Notification model
# Assuming you might need a form to change status later, but for now direct change.
# from .forms import CommandeStatusForm

def is_gestionnaire_check(user):
    return user.is_authenticated and user.is_gestionnaire

@login_required
@user_passes_test(is_gestionnaire_check, login_url='comptes:login')
def list_all_commandes_view(request):
    commandes = Commande.objects.all().order_by('-date_commande')
    return render(request, 'commandes/gestionnaire/list_commandes.html', {'commandes': commandes})

@login_required
@user_passes_test(is_gestionnaire_check, login_url='comptes:login')
def update_commande_status_view(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)
    if request.method == 'POST':
        new_status = request.POST.get('etat')
        old_status = commande.get_etat_display() # Get display name of old status
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

# Placeholder for client's view of their own commandes (already in original urls.py)
# Ensure it's login_required but not gestionnaire restricted
@login_required
def liste_commandes(request): # Renamed from file to avoid conflict
    commandes = Commande.objects.filter(client=request.user).order_by('-date_commande')
    return render(request, 'commandes/liste_commandes.html', {'commandes': commandes})

# Placeholder for creer_commande (already in original urls.py)
@login_required
def creer_commande(request):
    # Logic for creating a command
    # For now, just a placeholder render
    messages.info(request, "La création de commande n'est pas encore implémentée.")
    return render(request, 'commandes/creer_commande.html')


# Placeholder for modifier_commande (already in original urls.py)
# This should be for clients modifying their *pending* orders, or removed if not applicable
@login_required
def modifier_commande(request, pk):
    commande = get_object_or_404(Commande, pk=pk, client=request.user)
    # Add logic for modifying commande if allowed
    messages.info(request, "La modification de commande n'est pas encore implémentée ou est restreinte.")
    return render(request, 'commandes/modifier_commande.html', {'commande': commande})
