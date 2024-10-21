# main/models.py
from django.db import models
from accounts.models import User
from vendors.models import Product
from jalali_date_new.model_fields import JalaliDateTimeModelField
from django_jalali.db import models as jmodels


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(null=True, blank=True) 
    comment = models.TextField()
    created_at =  jmodels.jDateTimeField(auto_now_add=True)  #datetime in jalali #datetime 

    class Meta:
        unique_together = ['product', 'user']


