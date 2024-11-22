from django.shortcuts import render
from .forms import (
    SignupForm,
    SignInForm,
    ForgotPasswordForm,
    ResetPasswordForm,
    EditProfileForm,
)
from django.shortcuts import redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .email_content import reset_password_email_content
from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404


def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # print("user:", user)

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


def forgot_password_view(request):
    if request.method == "POST":
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            user = User.objects.filter(email=email).first()
            if user:
                print("User found:", user)
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))

                reset_url = request.build_absolute_uri(
                    f"/users/reset-password/{uid}/{token}"
                )

                email_content = reset_password_email_content(
                    reset_url=reset_url,
                    username=user.username,
                    site_name=settings.SITE_NAME,
                )

                email_message = EmailMessage(
                    subject=email_content["subject"],
                    body=email_content["html_message"],
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[email],
                    reply_to=[settings.SUPPORT_EMAIL],
                )

                email_message.content_subtype = "html"

                # Add custom headers to improve deliverability
                email_message.extra_headers = {
                    "List-Unsubscribe": f"<mailto:unsubscribe@{settings.SITE_DOMAIN}>",
                    "X-Entity-Ref-ID": f"reset-password-{user.id}",
                    "Precedence": "bulk",
                }
                email_message.send(fail_silently=False)

                messages.success(
                    request, "Password reset link has been sent to your email."
                )

                return render(request, "users/forgot_password.html", {"form": form})
            else:
                messages.error(request, "User with this email does not exist.")
                return render(
                    request,
                    "users/forgot_password.html",
                    {"form": form},
                )

    form = ForgotPasswordForm()
    return render(request, "users/forgot_password.html", {"form": form})


def reset_password_view(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)

        if not default_token_generator.check_token(user, token):
            messages.error(
                request,
                "The password reset link has expired or is invalid. Please request a new password reset link.",
            )
            return redirect("users:forgot_password")

        if request.method == "POST":
            form = ResetPasswordForm(request.POST)
            if form.is_valid():
                password1 = form.cleaned_data["password1"]
                password2 = form.cleaned_data["password2"]
                if password1 == password2:
                    user.set_password(password1)
                    user.save()
                    return redirect("users:password_reset_success")
                else:
                    messages.error(
                        request,
                        "The passwords you entered do not match. Please ensure both passwords are identical.",
                    )
            else:
                messages.error(
                    request,
                    "There was an error with the form. Please try again.",
                )
                return redirect("users:reset_password", uidb64=uidb64, token=token)

        else:
            form = ResetPasswordForm()

        return render(
            request,
            "users/reset_password.html",
            {"form": form, "uidb64": uidb64, "token": token},
        )

    except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
        messages.error(
            request,
            "The password reset link has expired or is invalid. Please request a new password reset link.",
        )
        print("Error:", e)
        return redirect("users:forgot_password")


def password_reset_success(request):
    return render(request, "users/password_reset_success.html")


@login_required(login_url="/users/signin")
def profile_view(request, username=None):
    if username:
        profile = get_object_or_404(User, username=username).profile
    else:
        profile = request.user.profile

    return render(request, "users/profile.html", {"profile": profile})


@login_required(login_url="/users/signin")
def edit_profile_view(request):
    if request.method == "POST":
        form = EditProfileForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if form.is_valid():
            form.save()
            return redirect("users:profile")
    else:
        form = EditProfileForm(instance=request.user.profile)

    return render(request, "users/edit_profile.html", {"form": form})


@login_required(login_url="/users/signin")
def delete_profile_view(request):
    user = request.user
    if request.method == "POST":
        logout(request)
        user.delete()
        return redirect("/")

    return render(request, "users/delete_profile.html")
