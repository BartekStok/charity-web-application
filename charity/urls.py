"""charity URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from charityapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls, name='admin-panel'),
    path('', LandingPageView.as_view(), name='landing-page'),
    path('add_donation/', AddDonationView.as_view(), name='add-donation'),
    path('confirm_of_donation/', DonationConfirmationView.as_view(), name='confirm-of-donation'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('update/', UpdateUserView.as_view(), name='update'),
    path('confirm_password/', ConfirmUserPasswordView.as_view(), name='confirm-password'),
    path('user_profile/', UserProfileView.as_view(), name='user-profile'),
    path('message/', ContactFormView.as_view(), name='message'),
]
