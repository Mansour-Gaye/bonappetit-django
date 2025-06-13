from django.core.management.base import BaseCommand
from comptes.models import CustomUser

class Command(BaseCommand):
    help = 'Crée un compte gestionnaire'

    def handle(self, *args, **kwargs):
        username = 'gestionnaire'
        email = 'gestionnaire@bonappetit.com'
        password = 'Gestionnaire123!'
        
        if CustomUser.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f"L'utilisateur {username} existe déjà."))
            return
        
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_gestionnaire=True,
            is_client=False,
            is_staff=True
        )
        
        self.stdout.write(self.style.SUCCESS(f"""
        Gestionnaire créé avec succès !
        Username: {username}
        Password: {password}
        Email: {email}
        """)) 