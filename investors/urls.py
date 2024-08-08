from django.urls import path
from . import views

urlpatterns = [path("sugest/", views.sugest, name="sugest")]
