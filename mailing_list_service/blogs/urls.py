from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.views.decorators.cache import cache_page


app_name = "blogs"
urlpatterns = [
    path("blog/<int:pk>/", cache_page(60)(views.BlogDetailView.as_view()), name='detail'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
