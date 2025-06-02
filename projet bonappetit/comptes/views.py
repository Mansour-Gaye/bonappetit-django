from django.shortcuts import render, redirect
from django.contrib import messages # For displaying messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from .models import Client
# Remove the placeholder HttpResponse if it's still there
# from django.http import HttpResponse

# Existing home view (if any)
def home(request):
    return render(request, 'comptes/home.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Client.objects.create(user=user) # Create Client profile
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('comptes:login') # Redirect to login page in 'comptes' app
    else:
        form = CustomUserCreationForm()
    return render(request, 'comptes/registration.html', {'form': form})

@login_required
def profile(request):
    # The Client object is accessed via user.client due to the OneToOneField relationship
    # No need to explicitly fetch Client if related_name is default 'client' or not set,
    # or if primary_key=True on the OneToOneField makes it accessible directly.
    # For clarity, we can try to fetch it, or rely on the template to access user.client.
    # Let's pass the user and allow template to access user.client for simplicity here.
    return render(request, 'comptes/profile.html', {'user_profile': request.user})