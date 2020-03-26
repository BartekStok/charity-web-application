from django.contrib.auth.models import User
from django.forms import ModelForm, Form
from django import forms
from charityapp.models import Category, Institution, Donation


class RegisterForm(ModelForm, Form):
    password = forms.CharField(widget=forms.PasswordInput())
    password_confirm = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']


    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        email = cleaned_data.get("email")
        if password != password_confirm:
            raise forms.ValidationError("Hasło niepoprawne!")
        try:
            user = User.objects.get(email=email)
            if user.email ==email:
                raise forms.ValidationError("Podany email już istneiej")
        except User.DoesNotExist:
            return None


class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']