from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.db import IntegrityError


class SignupForm(UserCreationForm):
    first_name = forms.CharField(label="First name")
    last_name = forms.CharField(label="Last name")

    def save(self, commit=True):
        """
        On save of the form, update the associated user profile with first and
        last names.
        """
        user = super(SignupForm, self).save(commit=False)
        profile = user.revolvuserprofile
        profile.first_name = self.cleaned_data["first_name"]
        profile.last_name = self.cleaned_data["last_name"]
        profile.save()
        if commit:
            user.save()
        return user

    def ensure_authenticated_user(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password2')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            return user
        raise IntegrityError(
            "User model could not be saved during signup process."
        )
