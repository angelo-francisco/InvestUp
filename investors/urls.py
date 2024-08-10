from django.urls import path
from . import views

urlpatterns = [
    path("sugest/", views.sugest, name="sugest"),
    path("see/<slug:slug>/", views.seeCompanyInvestors, name="seeCompanyInvestors"),
    path("proposal/<slug:slug>/", views.newProposalInvestors, name="proposalInvestors"),
    path("sign_contract/<int:id>/", views.sign_contract, name="sign_contract"),
]
