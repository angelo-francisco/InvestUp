from django.urls import path
from . import views


urlpatterns = [
    path("login/", views._login, name="login"),
    path("signup/", views._signup, name="signup"),
    path("logout/", views._logout, name="logout"),
    path("profile/<username>/", views.profile, name="profile"),
    path("reset/", views.reset_password, name="reset_password"),
    path(
        "reseting/<uidb64>/<token>/", views.reseting_password, name="reseting_password"
    ),
]
