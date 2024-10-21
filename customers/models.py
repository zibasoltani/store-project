from django.db import models
from accounts.models import User


class CustomerProfile(models.Model):
    GENDER_TYPE_CHOICES = (
        (1, 'مرد'),
        (2, 'زن'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.PositiveSmallIntegerField(choices=GENDER_TYPE_CHOICES, null=True, blank=True)
