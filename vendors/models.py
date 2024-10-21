from django.db import models
from django_jalali.db import models as jmodels


class Category(models.Model):
    name = models.CharField(max_length=100)
    seller = models.ForeignKey('accounts.SellerProfile', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=0)
    sales_count = models.PositiveIntegerField(default=0)
    discount = models.DecimalField(max_digits=10, default=0, decimal_places=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    seller = models.ForeignKey('accounts.SellerProfile', on_delete=models.CASCADE)
    created_at = jmodels.jDateTimeField(auto_now_add=True)  # datetime in jalali #datetime
    updated_at = jmodels.jDateTimeField(auto_now_add=True)  # datetime in jalali
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)  # فیلد جدید برای تصویر

    def get_final_price(self):
        discount = Discount.objects.filter(product=self).first()
        if discount:
            if discount.discount_type == 'percentage':
                return self.price * (1 - (discount.value / 100))
            elif discount.discount_type == 'fixed':
                return self.price - discount.value
        return self.price

    def __str__(self):
        return self.name


class Discount(models.Model):
    DISCOUNT_TYPES = [
        ('fixed', 'ثابت'),
        ('percentage', 'درصدی'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='discounts')
    seller = models.ForeignKey('accounts.SellerProfile', on_delete=models.CASCADE)
    discount_type = models.CharField(max_length=50, choices=DISCOUNT_TYPES)  # نوع تخفیف
    value = models.DecimalField(max_digits=10, decimal_places=0)  # مقدار تخفیف
