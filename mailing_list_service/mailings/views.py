from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from blogs.models import Blog
from .models import Client, Mailing, MailingTry, Message
import random
from django.views.generic import DetailView, ListView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.conf import settings
from django.core.cache import cache
from .forms import MailingForm, ClientForm, DeleteForm, MessageForm
from django.core.exceptions import PermissionDenied
from .scheduled import start_mailing as schedule_start_mailing, stop_mailing as schedule_stop_mailing


@login_required(login_url="/users/login")
def start_mailing(request, pk):
    mailing = Mailing.objects.get(pk=pk)
    if request.user.email != mailing.owner:
        raise PermissionDenied
    schedule_start_mailing(mailing)
    mailing.status = Mailing.Status.STARTED
    mailing.save()
    return redirect("mailings:mailings_list")


@login_required(login_url="/users/login")
def stop_mailing(request, pk):
    mailing = Mailing.objects.get(pk=pk)
    if request.user.email != mailing.owner and not request.user.groups.filter(name="manager").exists():
        raise PermissionDenied
    schedule_stop_mailing(mailing)
    mailing.status = Mailing.Status.FINISHED
    mailing.save()
    return redirect("mailings:mailings_list")


@login_required(login_url="/users/login")
def index(request):
    blogs_list = None
    if settings.CACHE_ENABLED:
        # Проверяем включенность кеша
        key = 'blogs'  # Создаем ключ для хранения
        blogs_list = cache.get(key)  # Пытаемся получить данные
        if blogs_list is None:
            # Если данные не были получены из кеша, то выбираем из БД и записываем в кеш
            blogs_list = list(Blog.objects.all())
            random.shuffle(blogs_list)
            blogs_list = blogs_list[:3]
            cache.set(key, blogs_list, 60)
    else:
        # Если кеш не был подключен, то просто обращаемся к БД
        blogs_list = list(Blog.objects.all())
        random.shuffle(blogs_list)
        blogs_list = blogs_list[:3]

    clients = Client.objects.filter(owner=request.user.email)

    mailings = Mailing.objects.filter(owner=request.user.email)

    active_mailings = Mailing.objects.filter(owner=request.user.email, status=Mailing.Status.STARTED.value)

    return render(request, "mailings/index.html",
                  {"blogs": blogs_list,
                   "client_count": len(clients),
                   "mailing_count": len(mailings),
                   "active_mailing_count": len(active_mailings)})


class MailingListView(LoginRequiredMixin, ListView):
    login_url = '/users/login'
    model = Mailing

    def get_queryset(self):
        if self.request.user.groups.filter(name="manager").exists():
            return self.model.objects.all()
        else:
            return self.model.objects.filter(owner=self.request.user.email)


class MailingDetailView(LoginRequiredMixin, DetailView):
    login_url = '/users/login'
    model = Mailing

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner == self.request.user.email:
            return self.object
        else:
            raise PermissionDenied

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["logs"] = MailingTry.objects.filter(mailing=context['object'])
        print(context)
        return context


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    login_url = '/users/login'
    redirect_field_name = 'redirect_to'
    model = Mailing
    success_url = reverse_lazy('mailings:mailings_list')

    def get_form_class(self):
        user = self.request.user
        if user.email == self.object.owner:
            return DeleteForm
        else:
            raise PermissionDenied


class MailingCreateView(LoginRequiredMixin, CreateView):
    login_url = '/users/login'
    redirect_field_name = 'redirect_to'
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailings:mailings_list')

    def form_valid(self, form):
        if form.is_valid():
            mailing = form.save()
            mailing.owner = self.request.user.email
            mailing.save()

        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/users/login'
    redirect_field_name = 'redirect_to'
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailings:mailings_list')

    def get_form_class(self):
        user = self.request.user
        if user.email == self.object.owner:
            return MailingForm
        else:
            raise PermissionDenied


class ClientListView(LoginRequiredMixin, ListView):
    login_url = '/users/login'
    model = Client

    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user.email)


class ClientDetailView(LoginRequiredMixin, DetailView):
    login_url = '/users/login'
    model = Client

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner == self.request.user.email:
            return self.object
        else:
            raise PermissionDenied


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    login_url = '/users/login'
    redirect_field_name = 'redirect_to'
    model = Client
    success_url = reverse_lazy('mailings:clients_list')

    def get_form_class(self):
        user = self.request.user
        if user.email == self.object.owner:
            return DeleteForm
        else:
            raise PermissionDenied


class ClientCreateView(LoginRequiredMixin, CreateView):
    login_url = '/users/login'
    redirect_field_name = 'redirect_to'
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailings:clients_list')

    def form_valid(self, form):
        if form.is_valid():
            client = form.save()
            client.owner = self.request.user.email
            client.save()

        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/users/login'
    redirect_field_name = 'redirect_to'
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailings:clients_list')

    def get_form_class(self):
        user = self.request.user
        if user.email == self.object.owner:
            return ClientForm
        else:
            raise PermissionDenied


class MessageListView(LoginRequiredMixin, ListView):
    login_url = '/users/login'
    model = Message

    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user.email)


class MessageDetailView(LoginRequiredMixin, DetailView):
    login_url = '/users/login'
    model = Message

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner == self.request.user.email:
            return self.object
        else:
            raise PermissionDenied


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    login_url = '/users/login'
    redirect_field_name = 'redirect_to'
    model = Message
    success_url = reverse_lazy('mailings:messages_list')

    def get_form_class(self):
        user = self.request.user
        if user.email == self.object.owner:
            return DeleteForm
        else:
            raise PermissionDenied


class MessageCreateView(LoginRequiredMixin, CreateView):
    login_url = '/users/login'
    redirect_field_name = 'redirect_to'
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailings:messages_list')

    def form_valid(self, form):
        if form.is_valid():
            message = form.save()
            message.owner = self.request.user.email
            message.save()

        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/users/login'
    redirect_field_name = 'redirect_to'
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailings:messages_list')

    def get_form_class(self):
        user = self.request.user
        if user.email == self.object.owner:
            return MessageForm
        else:
            raise PermissionDenied


class TryingListView(LoginRequiredMixin, ListView):
    login_url = '/users/login'
    model = MailingTry

    def get_queryset(self):
        if self.request.user.groups.filter(name="manager").exists():
            return self.model.objects.all()
        else:
            return self.model.objects.filter(mailing__owner=self.request.user.email)
