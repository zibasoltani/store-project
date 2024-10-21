# accounts/urls.py

from django.urls import path
from .views import register_customer, register_seller, user_login, otp_login, verify_otp, user_logout, address_create, address_update, address_delete, address_list
from .views import AddressListView, AddressDetailView, change_password, change_password_done, edit_phone, confirm_otp, edit_seller_profile


urlpatterns = [
    path('addresses/', address_list, name='address_list'),
    path('addresses/new/', address_create, name='address_create'),
    path('addresses/<int:pk>/edit/', address_update, name='address_update'),
    path('addresses/<int:pk>/delete/', address_delete, name='address_delete'),
    path('register/customer/', register_customer, name='register_customer'),
    path('register/seller/', register_seller, name='register_seller'),
    path('login/otp/', otp_login, name='otp_login'),  
    path('login/verify-otp/', verify_otp, name='verify_otp'), 
    path('login/', user_login, name='user_login'), #login page
    path('logout/', user_logout, name='logout'),
    path('change-password/', change_password, name='change_password'),
    path('change-password-done/', change_password_done, name='password_change_done'),
    path('edit-phone/', edit_phone, name='edit_phone'),
    path('confirm-otp/', confirm_otp, name='confirm_otp'),
    path('edit-seller-profile/', edit_seller_profile, name='edit_seller_profile'),
]
