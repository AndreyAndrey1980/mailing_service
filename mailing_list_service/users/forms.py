from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.core.exceptions import ObjectDoesNotExist


def check_email_exist(email):
    try:
        User.objects.get(email=email)
        return True
    except ObjectDoesNotExist:
        return False


def check_token_empty(email):
    try:
        user = User.objects.get(email=email)
        if user.token:
            return False
        else:
            return True
    except ObjectDoesNotExist:
        return False


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def clean_email(self):
        cleaned_data = self.cleaned_data.get('email')
        print("проверяем почту и токен")
        print(check_token_empty(cleaned_data))
        if check_email_exist(cleaned_data) and check_token_empty(cleaned_data):
            print("nут ошибка")
            raise forms.ValidationError('Ошибка такая почта уже используется')

        return cleaned_data


class EmailForm(forms.Form):
    email = forms.CharField()
