from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, UpdateView

from charityapp.forms import RegisterForm, LoginForm, UpdateUserForm, ConfirmUserPasswordForm, ChangeUserPassword
from charityapp.models import Donation, Institution


class LandingPageView(View):
    """Landing Page for charity app"""

    def get(self, request):

        """Simple counting for index view"""
        donation = Donation.objects.all()
        donation_quantity = sum([inst.quantity for inst in donation])
        institution = Institution.objects.count()

        """Pagination for foundations"""
        foundations_list = Institution.objects.filter(type="Fundacja").order_by("id")
        foundations_pagi = Paginator(foundations_list, 5)
        foundations_page = request.GET.get("page")
        foundations = foundations_pagi.get_page(foundations_page)

        """Pagination for organizations"""
        organizations = Institution.objects.filter(type="Organizacja pozarządowa").order_by("id")
        organizations_pag = Paginator(organizations, 5)

        """Pagination for local charity"""
        locals = Institution.objects.filter(type="Zbiórka lokalna").order_by("id")
        locals_pag = Paginator(locals, 5)

        ctx = {
            "donation_quantity": donation_quantity,
            "institution": institution,
            "foundations": foundations,
            "organizations": organizations,
            "locals": locals,
        }
        return render(request, "pages/index.html", ctx)


class AddDonationView(View):
    def get(self, request):
        return render(request, "forms/form.html")


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "forms/login.html", {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("landing-page")
            else:
                return redirect("register")
        else:
            return render(request, "forms/login.html", {"form": form})


class ConfirmUserPasswordView(View):
    def get(self, request):
        form = ConfirmUserPasswordForm(user=request.user)
        return render(request, "forms/user-confirm-password.html", {"form": form})

    def post(self, request):
        form = ConfirmUserPasswordForm(request.POST, user=request.user)
        if form.is_valid():
            return redirect('update')
        else:
            return render(request, "forms/user-confirm-password.html", {"form": form})


class UpdateUserView(View):

    def get(self, request):
        user = request.user
        form1 = UpdateUserForm(initial={
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        })
        form2 = ChangeUserPassword(user=request.user)
        ctx = {"form1": form1, "form2": form2}
        return render(request, "forms/user-settings.html", ctx)

    def post(self, request):
        form1 = UpdateUserForm(request.POST)
        form2 = ChangeUserPassword(request.POST, user=request.user)
        user = request.user
        if 'user-data' in request.POST:
            if form1.is_valid():
                first_name = form1.cleaned_data['first_name']
                last_name = form1.cleaned_data['last_name']
                email = form1.cleaned_data['email']
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.save()
        elif 'user-password' in request.POST:
            if form2.is_valid():
                new_password = form2.cleaned_data['password_new']
                user.set_password(new_password)
                user.save()
        return redirect("landing-page")


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("landing-page")


class RegisterView(View):

    def get(self, request):
        form = RegisterForm()
        return render(request, "forms/register.html", {"form": form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                username=email,
            )
            return redirect("login")
        else:
            return render(request, "forms/register.html", {"form": form})

