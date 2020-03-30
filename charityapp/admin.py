from django.contrib import admin
from charityapp.models import *
# Register your models here.

admin.site.register(Category)
admin.site.register(Institution, InstitutionAdmin)
admin.site.register(Donation, DonationAdmin)
