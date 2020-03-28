from django.contrib.admin import ModelAdmin
from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Institution(models.Model):
    INSTITUTION_TYPES = (
        ("Fundacja", "Fundacja"),
        ("Organizacja pozarządowa", "Organizacja pozarządowa"),
        ("Zbiórka lokalna", "Zbiórka lokalna"),
    )
    name = models.CharField(max_length=128)
    description = models.TextField()
    type = models.CharField(choices=INSTITUTION_TYPES, default="Fundacja", max_length=128)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name


class Donation(models.Model):
    quantity = models.IntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=256)
    phone_number = models.IntegerField()
    city = models.CharField(max_length=128)
    zip_code = models.CharField(max_length=128)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField()
    user = models.ForeignKey(User, null=True, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} dla {self.institution}"


def quantity(obj):
    if obj.quantity == 1:
        return f"{obj.quantity} worek"
    elif 1 < obj.quantity < 5:
        return f"{obj.quantity} worki"
    elif obj.quantity >= 5:
        return f"{obj.quantity} worków"
class DonationAdmin(ModelAdmin):
    list_display = ('institution', 'user', quantity, 'city')

