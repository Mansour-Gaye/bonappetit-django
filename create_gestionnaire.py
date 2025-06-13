import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bonappetit.settings')
django.setup()

from comptes.models import CustomUser

def create_gestionnaire():
    username = 'gestionnaire'
    email = 'gestionnaire@bonappetit.com'
    password = 'Gestionnaire123!'
    
    # Vérifier si l'utilisateur existe déjà
    if CustomUser.objects.filter(username=username).exists():
        print(f"L'utilisateur {username} existe déjà.")
        return
    
    # Créer le gestionnaire
    user = CustomUser.objects.create_user(
        username=username,
        email=email,
        password=password,
        is_gestionnaire=True,
        is_client=False,
        is_staff=True
    )
    
    print(f"""
    Gestionnaire créé avec succès !
    Username: {username}
    Password: {password}
    Email: {email}
    """)

if __name__ == '__main__':
    create_gestionnaire() 