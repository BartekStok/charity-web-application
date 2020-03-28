from django.contrib.auth import authenticate, password_validation
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

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = User.objects.get(email=email)
            if not user.check_password(password):
                raise forms.ValidationError("Błędne hasło")
        except Exception:
            return None
        return super(LoginForm, self).clean(*args, **kwargs)


class ConfirmUserPasswordForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}))

    class Meta:
        model = User
        fields = ['password']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(ConfirmUserPasswordForm, self).__init__(*args, **kwargs)


    def clean(self, *args, **kwargs):
        cleaned_data = super(ConfirmUserPasswordForm, self).clean()
        password = cleaned_data.get("password")
        if not self.user.check_password(password):
            raise forms.ValidationError("Błędne hasło")
        return cleaned_data


class UpdateUserForm(ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Imię'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nazwisko'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    # def clean(self, *args, **kwargs):
    #     cleaned_data = super(UpdateUserForm, self).clean()
    #     password = cleaned_data.get("password")
    #     password_confirm = cleaned_data.get("password_confirm")
    #     if password != password_confirm:
    #         raise forms.ValidationError("Hasła nie zgadzają się!")
    #     return cleaned_data


class ChangeUserPassword(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}))
    password_new = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Nowe hasło'}))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Powtórz hasło'}))

    class Meta:
        model = User
        fields = ['password', 'password_new', 'password_confirm']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(ChangeUserPassword, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        cleaned_data = super(ChangeUserPassword, self).clean()
        password = cleaned_data.get("password")
        password_new = cleaned_data.get("password_new")
        password_confirm = cleaned_data.get("password_confirm")
        if not self.user.check_password(password):
            raise forms.ValidationError("Błędne hasło")
        if password_new != password_confirm:
            raise forms.ValidationError("Hasła nie zgadzają się!")
        return cleaned_data


class DonationStatusForm(forms.Form):
    is_taken = forms.BooleanField()