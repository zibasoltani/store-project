# cart/urls.py

from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import AddToCartView, ViewCartView, RemoveFromCartView, UpdateCartView, cart_view, CheckoutView, checkout, order_confirmation

from .views import APIRootView




# Router configuration
router = DefaultRouter()
router.register(r'cart', ViewCartView, basename='view_cart')

urlpatterns = [
    path('', APIRootView.as_view(), name='api_root'),  # API root endpoint
    path('cart/add/<int:product_id>/', AddToCartView.as_view({'post': 'add'}), name='add_to_cart'),
    path('cart/remove/', RemoveFromCartView.as_view({'post': 'remove'}), name='remove_from_cart'),
    path('cart/update/<int:product_id>/', UpdateCartView.as_view({'post': 'update'}), name='update_cart'),
    path('cart/view/', cart_view, name="cart_view"),
    path('checkout/', checkout, name='checkout'),
    path('order/confirmation/<int:order_id>/', order_confirmation, name='order_confirmation'),
]

urlpatterns += [
    path('cart/', ViewCartView.as_view(), name='view-cart'),
    path('checkoutapi/', CheckoutView.as_view(), name='checkoutapi'),
]
