from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].error_messages = {
            "unique": "This username is already taken",
        }
        self.fields["password1"].error_messages = {
            "password_too_short": "Password must be at least 8 characters",
        }
        self.fields["password2"].error_messages = {
            "password_mismatch": "The two password fields do not match",
        }

        self.fields["password1"].label = "Password"
        self.fields["password2"].label = "Confirm Password"

        for field in self.fields.values():
            field.widget.attrs["class"] = (
                "appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email


class SignInForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.error_messages = {
            "invalid_login": "Please enter the correct username and password.",
        }

        for field in self.fields.values():
            field.widget.attrs["class"] = (
                "appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            )


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm",
                "placeholder": "Email",
            }
        ),
    )


class ResetPasswordForm(forms.Form):
    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
                "placeholder": "New Password",
            }
        ),
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
                "placeholder": "Confirm New Password",
            }
        ),
    )


class EditProfileForm(forms.ModelForm):
    bio = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 3,
            }  # Controls the height of the textarea
        ),
    )

    class Meta:
        model = Profile
        fields = ["full_name", "bio", "avatar"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs["class"] = (
                "appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            )
