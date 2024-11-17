from django.shortcuts import render
from .forms import SignupForm, SignInForm
from django.shortcuts import redirect
from django.contrib.auth import login, logout


def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            print("user:", user)
            login(request, user)
            return redirect("post:posts")

    else:
        form = SignupForm()

    return render(request, "users/signup.html", {"form": form})


def signin_view(request):
    if request.method == "POST":
        form = SignInForm(data=request.POST)
        # print("Form errors:", form.errors)
        if form.is_valid():
            login(request, form.get_user())
            print("User logged in:", request.user)
            return redirect("post:posts")

    else:
        form = SignInForm()

    return render(request, "users/signin.html", {"form": form})


def signout_view(request):
    logout(request)
    return redirect("/")
