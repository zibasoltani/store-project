from django.contrib import admin
from .models import Category, Product, Discount


class DiscountInline(admin.TabularInline):
    model = Discount
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'sales_count', 'discount', 'created_at')
    list_filter = ('category', 'seller', 'created_at')
    search_fields = ('name', 'description')
    inlines = [DiscountInline]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'seller')
    search_fields = ('name',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Discount)
