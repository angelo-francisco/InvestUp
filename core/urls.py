from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.urls import reverse_lazy

from django.conf import settings
from django.conf.urls.static import static


alternativesURLS = [
    path("", RedirectView.as_view(url=reverse_lazy("showCompany"))),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("users.urls")),
    path("company/", include("companies.urls")),
] + alternativesURLS

# FOR MEDIA FILES
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# FOR STATIC FILES
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
