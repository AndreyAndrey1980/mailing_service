from django.views.generic import CreateView, ListView
from django.contrib.auth.views import LoginView
from .models import User
from django.views.generic.edit import FormView
from .forms import RegisterForm, EmailForm
from django.conf import settings
from django.core.mail import send_mail
import string
import random
import secrets
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist


class UserRegisterView(CreateView):
    # Создаем обычный контроллер на создание сущности
    model = User
    form_class = RegisterForm

    def form_valid(self, form):
        if form.is_valid():
            email = form.cleaned_data.get('email')
            print(f"почта {email}")
            try:
                user = User.objects.get(email=email)
                if not user.token:
                    print("удаляем неактивир пользователя")
                    user.delete()
            except ObjectDoesNotExist:
                pass
            token = secrets.token_hex(16)
            new_user = form.save()
            new_user.is_active = False
            new_user.token = token
            new_user.save()
            host = self.request.get_host()
            url = f'http://{host}/users/email-confirm/{token}/'
            send_mail('Подтверждение почты',
                      f'Подтвердите почту и перейдите по ссылке {url}, если это не вы, то не переходите по ссылке',
                      settings.EMAIL_HOST_USER, [new_user.email])

        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.token = None
    user.save()
    send_mail('Регистрация', 'Регистрация прошла успешно',
              settings.EMAIL_HOST_USER, [user.email])
    return redirect("mailings:index")


class UserLoginView(LoginView):
    template_name = "users/login.html"


class ResetPassword(FormView):
    form_class = EmailForm
    template_name = "users/password_reset.html"
    success_url = "/mailings_service"

    def form_valid(self, form):
        if form.is_valid():
            print(type(form))
            print(form)
            email = form.cleaned_data["email"]
            user = User.objects.get(email=email)
            password = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
            user.set_password(password)
            user.save(update_fields=['password'])
            send_mail('Сброс пароля', f'ваш новый пароль {password}',
                      settings.EMAIL_HOST_USER, [user.email])

        return super().form_valid(form)


class UserListView(LoginRequiredMixin, ListView):
    login_url = '/users/login'
    model = User

    def get_queryset(self):
        if self.request.user.groups.filter(name="manager").exists():
            return self.model.objects.all()
        else:
            raise PermissionDenied


@login_required(login_url="/users/login")
def block_user(request, pk):
    user = User.objects.get(pk=pk)
    if not request.user.groups.filter(name="manager").exists():
        raise PermissionDenied
    user.is_active = False
    user.save()
    return redirect("users:list")


@login_required(login_url="/users/login")
def unblock_user(request, pk):
    user = User.objects.get(pk=pk)
    if not request.user.groups.filter(name="manager").exists():
        raise PermissionDenied
    user.is_active = True
    user.save()
    return redirect("users:list")
