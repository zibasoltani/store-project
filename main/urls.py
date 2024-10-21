from django.urls import path
from .views import home, product_detail, seller_detail, category_products

urlpatterns = [
    path('', home, name='home'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('seller/<int:id>/', seller_detail, name='seller_detail'),  # URL برای نمایش جزئیات فروشگاه
    path('category/<int:category_id>/', category_products, name='category_products'),
]