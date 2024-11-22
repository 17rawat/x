from django.urls import path
from . import views


app_name = "users"

urlpatterns = [
    path("signin", views.signin_view, name="signin"),
    path("signup", views.signup_view, name="signup"),
    path("signout", views.signout_view, name="signout"),
    path("profile", views.profile_view, name="profile"),
    path("edit-profile", views.edit_profile_view, name="edit_profile"),
    path("delete-profile", views.delete_profile_view, name="delete_profile"),
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
    path("profile/<str:username>", views.profile_view, name="profile"),
]
