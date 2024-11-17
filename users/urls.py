from django.urls import path
from . import views


app_name = "users"

urlpatterns = [
    path("signin", views.signin_view, name="signin"),
    path("signup", views.signup_view, name="signup"),
    path("signout", views.signout_view, name="signout"),
]