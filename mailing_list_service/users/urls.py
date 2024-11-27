from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import LogoutView

app_name = "users"
urlpatterns = [
    path("register", views.UserRegisterView.as_view(success_url='/mailings_service'), name="users_register"),
    path("login", views.UserLoginView.as_view(success_url='/mailings_service'), name="users_login"),
    path("logout", LogoutView.as_view(), name="users_logout"),
    path("pass_rec", views.ResetPassword.as_view(), name="recovery_password"),

    path("list", views.UserListView.as_view(), name="list"),
    path("<int:pk>/block", views.block_user, name="block"),
    path("<int:pk>/unblock", views.unblock_user, name="unblock"),

    path("email-confirm/<str:token>/", views.email_verification, name="email-confirm")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
