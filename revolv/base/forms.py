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
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user

    def ensure_authenticated_user(self):
        """
        Return the User model related to this valid form, or raise an
        IntegrityError if it does not exist (because it should).
        """
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password2')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            return user
        raise IntegrityError(
            "User model could not be saved during signup process."
        )
