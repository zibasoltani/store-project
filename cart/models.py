from django.db import models
from accounts.models import User
from vendors.models import Product, Discount
from jalali_date_new.model_fields import JalaliDateTimeModelField
from django_jalali.db import models as jmodels


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    updated_at = jmodels.jDateTimeField(auto_now_add=True)

    def calculate_total_price(self):
        return sum(item.get_final_price() * item.quantity for item in self.items.all())

    def total_price(self):
        return self.calculate_total_price()


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=0)

    def get_final_price(self):
        discount = Discount.objects.filter(product=self.product).first()
        if discount:
            if discount.discount_type == 'percentage':
                return self.product.price * (1 - (discount.value / 100))
            elif discount.discount_type == 'fixed':
                return self.product.price - discount.value
        return self.product.price


class Order(models.Model):

    def calculate_total_price(self):
        total = sum(item.price * item.quantity for item in self.items.all())
        return total - self.calculate_total_discount()

    def calculate_total_discount(self):
        return sum(self.calculate_discount(item) for item in self.items.all())

    def calculate_discount(self, item):
        discount = Discount.objects.filter(product=item.product).first()
        if discount:
            if discount.discount_type == 'percentage':
                return item.price * (discount.value / 100) * item.quantity
            elif discount.discount_type == 'fixed':
                return min(discount.value, item.price * item.quantity)
        return 0

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    updated_at = jmodels.jDateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Pending')
    address = models.TextField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=0)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=0)  # قیمت در زمان ثبت سفارش

    def get_final_price(self):
        discount = Discount.objects.filter(product=self.product).first()
        if discount:
            if discount.discount_type == 'percentage':
                return self.product.price * (1 - (discount.value / 100))
            elif discount.discount_type == 'fixed':
                return self.product.price - discount.value
        return self.product.price
