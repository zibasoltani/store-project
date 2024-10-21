from django.contrib import admin
from .models import CustomerProfile


class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'gender')
    search_fields = ('first_name', 'last_name', 'user__username')  # جستجو بر اساس نام، نام خانوادگی و نام کاربری
    list_filter = ('gender',)  # فیلتر کردن بر اساس جنسیت
    ordering = ('last_name', 'first_name')  # ترتیب مرتب‌سازی بر اساس نام خانوادگی و نام
    fieldsets = (
        (None, {
            'fields': ('user', 'first_name', 'last_name', 'gender')
        }),
    )


admin.site.register(CustomerProfile, CustomerProfileAdmin)
