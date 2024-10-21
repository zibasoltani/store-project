from rest_framework import viewsets, views
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import Cart, CartItem
from .serializers import CartSerializer
from django.shortcuts import get_object_or_404
from vendors.models import Product, Discount
from django.shortcuts import render, redirect
from accounts.models import Address
from .models import Order, OrderItem
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth.decorators import login_required
from django.contrib import messages


class CartManager:
    @staticmethod
    def get_or_create_cart(request):
        cart_id = request.session.get('cart_id')

        # برای کاربران احراز هویت شده
        if request.user.is_authenticated:
            # بررسی سبد خرید موجود برای کاربر
            cart = Cart.objects.filter(user=request.user).first()

            # اگر سبد خریدی وجود دارد و شناسه آن در سشن موجود است
            if not cart and cart_id:
                # سبد خرید با شناسه موجود در سشن را به کاربر منتسب کنید
                cart = get_object_or_404(Cart, id=cart_id)
                cart.user = request.user
                cart.save()  # ذخیره تغییرات در پایگاه داده

            # اگر سبد خریدی برای کاربر وجود ندارد، یکی جدید بسازید.
            if not cart:
                cart = Cart.objects.create(user=request.user)

            # اطمینان از اینکه شناسه سبد خرید در نشست ذخیره شده باشد
            request.session['cart_id'] = cart.id
        else:
            # برای کاربران غیر احراز هویت شده
            if cart_id:
                cart = get_object_or_404(Cart, id=cart_id)
            else:
                cart = Cart.objects.create()  # یک سبد خرید بدون کاربر ایجاد کنید
                request.session['cart_id'] = cart.id

        return cart

    @staticmethod
    def associate_cart_with_user(cart, user):
        if user.is_authenticated and cart.user is None:
            cart.user = user
            cart.save()


class AddToCartView(viewsets.ViewSet):
    @action(detail=False, methods=['post'], url_path='add/(?P<product_id>[^/.]+)')
    def add(self, request, product_id=None):
        product = get_object_or_404(Product, id=product_id)
        cart = CartManager.get_or_create_cart(request)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'price': product.get_final_price()}  # قیمت نهایی با احتساب تخفیف
        )

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        CartManager.associate_cart_with_user(cart, request.user)

        return Response({'message': 'به سبد خرید اضافه شد', 'cart_item_id': cart_item.id},
                        status=status.HTTP_201_CREATED)


class ViewCartView(views.APIView):
    def get(self, request):
        cart = CartManager.get_or_create_cart(request)
        serializer = CartSerializer(cart)
        return Response(serializer.data)


class RemoveFromCartView(viewsets.ViewSet):
    @action(detail=False, methods=['post'], url_path='remove/')
    def remove(self, request):
        product_id = request.data.get('product_id')  # استخراج product_id از داده‌های دریافتی
        cart = CartManager.get_or_create_cart(request)
        cart_item = get_object_or_404(CartItem, cart=cart, product__id=product_id)
        cart_item.delete()
        return Response({'message': 'Item removed from cart'}, status=status.HTTP_204_NO_CONTENT)


class UpdateCartView(viewsets.ViewSet):
    @action(detail=False, methods=['post'], url_path='update/(?P<product_id>[^/.]+)')
    def update(self, request, product_id=None):
        quantity = request.data.get('quantity')

        try:
            quantity = int(quantity)
        except (ValueError, TypeError):
            return Response({'error': 'Invalid quantity'}, status=status.HTTP_400_BAD_REQUEST)

        if quantity <= 0:
            return Response({'error': 'Invalid quantity'}, status=status.HTTP_400_BAD_REQUEST)

        cart = CartManager.get_or_create_cart(request)

        try:
            cart_item = CartItem.objects.get(cart=cart, product__id=product_id)
        except CartItem.DoesNotExist:
            return Response({'error': 'Cart item does not exist for this product in your cart.'},
                            status=status.HTTP_404_NOT_FOUND)

        cart_item.quantity = quantity
        cart_item.save()

        return Response({'message': 'Item quantity updated'}, status=status.HTTP_200_OK)


@login_required(login_url='/accounts/login/?next=/checkout/')
def checkout(request):
    # سبد خرید کاربر فعلی را دریافت کنیم
    cart = Cart.objects.filter(user=request.user).first()
    if not cart:
        messages.error(request, "سبد خرید شما خالی است.")
        return redirect('cart_view')

    # قیمت کل سبد را با تخفیف محاسبه میکنیم
    total = sum(item.get_final_price() * item.quantity for item in cart.items.all())

    # آدرس های کاربر را دریافت میکنیم
    addresses = request.user.addresses.all()

    if request.method == 'POST':
        selected_address_id = request.POST.get('address')
        address = Address.objects.get(id=selected_address_id, user=request.user)

        # سفارش را با مجموع_مبلغ ایجاد میکنیم
        order = Order.objects.create(user=request.user, address=address.full_address, total_amount=total)

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.get_final_price()  # استفاده از قیمت نهایی با احتساب تخفیف
            )

            # به روز رسانی تعداد فروش
            item.product.sales_count += item.quantity
            item.product.save()

        # سبد خرید را پاک کنید
        cart.items.all().delete()
        messages.success(request, "سفارش شما با موفقیت ثبت شد.")
        return redirect('order_confirmation', order.id)

    return render(request, 'cart/checkout.html', {'total': total, 'addresses': addresses})


class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart = CartManager.get_or_create_cart(request)
        address_id = request.data.get('address_id')

        address = get_object_or_404(Address, id=address_id, user=request.user)

        # خالی بودن سبد خرید را بررسی میشود
        if not cart.items.exists():
            return Response({'error': 'سبد خرید خالی است.'}, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(
            user=request.user,
            address=address.full_address,
            total_amount=cart.total_price()
        )

        for item in cart.items.all():
            # هنگام ایجاد OrderItem قیمت را درج میشود
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, price=item.price)

        # سبد خرید را پاک میشود
        cart.items.all().delete()

        return Response({'message': 'سفارش شما با موفقیت ثبت شد'}, status=status.HTTP_201_CREATED)


def order_confirmation(request, order_id):
    # Assuming you retrieve order items or similar data
    order_items = OrderItem.objects.filter(order_id=order_id)
    order = get_object_or_404(Order, id=order_id)
    total_sum = sum(item.price for item in order_items)
    return render(request, 'cart/order_confirmation.html', {'order': order, 'total_sum': total_sum})


def cart_view(request):
    cart = CartManager.get_or_create_cart(request)
    addresses = Address.objects.filter(user=request.user) if request.user.is_authenticated else []
    return render(request, 'cart/cart.html',
                  {'cart': cart, 'addresses': addresses, 'user_authenticated': request.user.is_authenticated})


class APIRootView(APIView):
    def get(self, request, format=None):
        api_urls = {
            'Add to Cart': '/cart/add/<product_id>/',
            'Remove from Cart': '/cart/remove/',
            'Update Cart': '/cart/update/<product_id>/',
            'View Cart': '/cart/view/',
            'Checkout': '/checkout/',
            'Order Confirmation': '/order/confirmation/<order_id>/',
            'Checkout API': '/checkoutapi/',
        }
        return Response(api_urls, status=status.HTTP_200_OK)
