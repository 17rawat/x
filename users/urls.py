from django.urls import path
from . import views


app_name = "users"

urlpatterns = [
    path("signin", views.signin_view, name="signin"),
    path("signup", views.signup_view, name="signup"),
    path("signout", views.signout_view, name="signout"),
    path("forgot-password", views.forgot_password_view, name="forgot_password"),
    path(
        "reset-password/<uidb64>/<token>/",
        views.reset_password_view,
        name="reset_password",
    ),
    path(
        "password-reset-success",
        views.password_reset_success,
        name="password_reset_success",
    ),
]
