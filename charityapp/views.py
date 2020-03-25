from django.shortcuts import render
from django.views import View


class LandingPageView(View):
    def get(self, request):
        return render(request, "pages/index.html")


class AddDonationView(View):
    def get(self, request):
        return render(request, "forms/form.html")


class LoginView(View):
    def get(self, request):
        return render(request, "forms/login.html")


class RegisterView(View):
    def get(self, request):
        return render(request, "forms/register.html")

