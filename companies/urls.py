from django.urls import path
from . import views


urlpatterns = [
    path("", views.showCompany, name="showCompany"),
    path("new/", views.addCompany, name="addCompany"),
    path("<slug:slug>/", views.seeCompany, name="seeCompany"),
    path("remove/<slug:slug>/", views.removeDocument, name="removeDocument"),
    path("metric/new/<slug:slug>/", views.addMetric, name="addMetric"),
]
