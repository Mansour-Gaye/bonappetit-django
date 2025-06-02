from django.shortcuts import render, redirect
from django.contrib import messages # For displaying messages
from .forms import CustomUserCreationForm
# Remove the placeholder HttpResponse if it's still there
# from django.http import HttpResponse

# Existing home view (if any)
def home(request):
    return render(request, 'comptes/home.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('comptes:login') # Redirect to login page in 'comptes' app
    else:
        form = CustomUserCreationForm()
    return render(request, 'comptes/registration.html', {'form': form})