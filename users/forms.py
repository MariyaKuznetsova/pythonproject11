from django.contrib.auth.forms import UserCreationForm

from newsletter.forms import BootstrapFormMixin
from users.models import User


class UserRegisterForm(BootstrapFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ["email", "password1", "password2"]
