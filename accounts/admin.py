from django.contrib import admin

from django.contrib import admin
from .models import User, SellerProfile, Address


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_type', 'phone_number')
    search_fields = ('username', 'email', 'phone_number')
    list_filter = ('user_type',)


@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'shop_name')
    search_fields = ('user__username', 'shop_name')
    list_filter = ('gender',)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'state', 'city', 'country')
    search_fields = ('user__username', 'city')
    list_filter = ('country',)
