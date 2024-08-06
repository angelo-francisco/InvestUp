from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.urls import reverse_lazy


alternativesURLS = [
    path("", RedirectView.as_view(url=reverse_lazy("addCompany"))),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("users.urls")),
    path("company/", include("companies.urls")),
] + alternativesURLS
