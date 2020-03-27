from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from charityapp.forms import RegisterForm, LoginForm
from charityapp.models import Donation, Institution


class LandingPageView(View):

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

