from django.contrib.auth.models import User
from django.forms import ModelForm, Form
from django import forms
from charityapp.models import Category, Institution, Donation


class RegisterForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Imię'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nazwisko'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Powtórz hasło'}))


    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        email = cleaned_data.get("email")
        if password != password_confirm:
            raise forms.ValidationError("Hasła nie zgadzają się!")
        try:
            user = User.objects.get(email=email)
            if user.email == email:
                raise forms.ValidationError("Podany email już istnieje w bazie danych")
        except User.DoesNotExist:
            return None
        return cleaned_data

class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']
        widgets = {
            'password': forms.PasswordInput(attrs={'placeholder': 'Hasło'}),
            'email': forms.TextInput(attrs={'placeholder': 'Email'})
        }