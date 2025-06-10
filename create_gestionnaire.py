import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bonappetit.settings')
django.setup()

from comptes.models import CustomUser

def create_gestionnaire():
    username = 'gestionnaire1'
    email = 'gestionnaire1@test.com'
    password = 'gestionnaire123'
    
    if not CustomUser.objects.filter(username=username).exists():
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_gestionnaire=True,
            is_client=False
        )
        print(f"Gestionnaire créé avec succès : {username}")
    else:
        print(f"L'utilisateur {username} existe déjà")

if __name__ == '__main__':
    create_gestionnaire() 