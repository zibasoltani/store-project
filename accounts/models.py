from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'Customer'),
        (2, 'Seller'),
        (3, 'Employee'),
    )
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES)
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    groups = models.ManyToManyField('auth.Group', related_name='custom_user_set', blank=True)

    user_permissions = models.ManyToManyField('auth.Permission', related_name='custom_user_permissions_set', blank=True)


class SellerProfile(models.Model):
    GENDER_TYPE_CHOICES = (
        (1, 'مرد'),
        (2, 'زن'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.PositiveSmallIntegerField(choices=GENDER_TYPE_CHOICES, blank=True, null=True)
    shop_name = models.CharField(max_length=255)
    shop_address = models.TextField()


# accounts/models.py

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    line_1 = models.CharField(max_length=255)
    line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.line_1}, {self.city}, {self.country}"

    @property
    def full_address(self):
        return f"{self.line_1}, {self.city}, {self.state}, {self.postal_code}, {self.country}"
