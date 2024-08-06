from django.urls import path
from . import views


urlpatterns = [path("new/", views.addCompany, name="addCompany")]
