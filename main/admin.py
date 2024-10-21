from django.contrib import admin
from .models import Review


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')  # نمایش فیلدهای مورد نظر در لیست
    list_filter = ('product', 'user', 'rating')  # فیلتر کردن بر اساس فیلدهای مورد نظر
    search_fields = ('user__username', 'product__name', 'comment')  # قابلیت جستجو
    ordering = ('-created_at',)  # ترتیب نمایش بر اساس تاریخ ایجاد
    raw_id_fields = ('user', 'product')  # نمایش به عنوان فیلدهای Raw ID


admin.site.register(Review, ReviewAdmin)
