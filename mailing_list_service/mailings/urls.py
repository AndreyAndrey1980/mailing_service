from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.views.decorators.cache import cache_page

app_name = "mailings"
urlpatterns = [
    path("", cache_page(0)(views.index), name="index"),
    path("mailings", views.MailingListView.as_view(), name='mailings_list'),
    path("mailings/<int:pk>/", views.MailingDetailView.as_view(), name='mailings_detail'),
    path("mailings/<int:pk>/delete", views.MailingDeleteView.as_view(), name="mailings_delete"),
    path("mailings/create", views.MailingCreateView.as_view(), name="mailings_create"),
    path("mailings/<int:pk>/update", views.MailingUpdateView.as_view(), name="mailings_update"),

    path("clients", views.ClientListView.as_view(), name='clients_list'),
    path("clients/<int:pk>", views.ClientDetailView.as_view(), name='clients_detail'),
    path("clients/<int:pk>/delete", views.ClientDeleteView.as_view(), name="clients_delete"),
    path("clients/create", views.ClientCreateView.as_view(), name="clients_create"),
    path("clients/<int:pk>/update", views.ClientUpdateView.as_view(), name="clients_update"),

    path("messages", views.MessageListView.as_view(), name='messages_list'),
    path("messages/<int:pk>", views.MessageDetailView.as_view(), name='messages_detail'),
    path("messages/<int:pk>/delete", views.MessageDeleteView.as_view(), name="messages_delete"),
    path("messages/create", views.MessageCreateView.as_view(), name="messages_create"),
    path("messages/<int:pk>/update", views.MessageUpdateView.as_view(), name="messages_update"),

    path("mailings/<int:pk>/start", views.start_mailing, name="mailings_start"),
    path("mailings/<int:pk>/stop", views.stop_mailing, name="mailings_stop")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
