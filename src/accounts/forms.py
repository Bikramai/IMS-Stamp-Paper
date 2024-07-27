from django.forms import ModelForm, ValidationError
from src.accounts.models import User
from django.contrib.auth.forms import AuthenticationForm


class CustomLoginForm(AuthenticationForm):
    def confirm_login_allowed(self, user):

        if not user.is_active:
            raise ValidationError(f"Hi {user.username}! Your account is inactive and you are not allowed to sign in.")

        if not user.is_superuser:
            if not user.treasury:
                raise ValidationError(f"Hi {user.username}! No treasury has been assigned to you. Please contact your administrator.")

        return super().confirm_login_allowed(user)


class UserProfileForm(ModelForm):

    class Meta:
        model = User
        fields = [
            'profile_image', 'first_name', 'last_name',
            'phone_number', 'cnic'
        ]
