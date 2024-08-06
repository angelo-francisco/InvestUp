from django.urls import path
from . import views


urlpatterns = [
    path("", views.showCompany, name="showCompany"),
    path("new/", views.addCompany, name="addCompany"),
    path("<slug:slug>/", views.seeCompany, name="seeCompany"),
]
