from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        # Fields to include on the registration form:
        # Default UserCreationForm fields are username and password fields.
        # Add 'email' as it's commonly required.
        # 'phone' is also a custom field in CustomUser.
        # 'is_client' and 'is_gestionnaire' have defaults, usually not set by user at registration
        # unless specific logic is intended for that.
        fields = UserCreationForm.Meta.fields + ('email', 'phone',)
