from django.urls import path
from .views import AddProductView, product_list, ProductUpdateView, seller_dashboard, manage_sellers, manage_products, reports, category_list, category_create, category_update, category_delete, delete_product, discount_list, discount_create, discount_update, discount_delete
from .views import order_list, vendor_products_with_reviews

urlpatterns = [
    path('manage_sellers/', manage_sellers, name='manage_sellers'),
    path('manage_products/', manage_products, name='manage_products'),
    path('reports/', reports, name='reports'),
    path('products/', product_list, name='product_list'),
    path('product/edit/<int:pk>/', ProductUpdateView.as_view(), name='edit_product'),
    path('delete-product/<int:product_id>/', delete_product, name='delete_product'),
    path('dashboard/', seller_dashboard, name='seller_dashboard'),
    path('add_product/', AddProductView.as_view(), name='add_product'),
    path('category/', category_list, name='category_list'),
    path('category/new/', category_create, name='category_create'),
    path('category/<int:pk>/edit/', category_update, name='category_update'),
    path('category/<int:pk>/delete/', category_delete, name='category_delete'),

    path('discount/', discount_list, name='discount_list'),
    path('discount/new/', discount_create, name='discount_create'),
    path('discount/<int:pk>/edit/', discount_update, name='discount_update'),
    path('discount/<int:pk>/delete/', discount_delete, name='discount_delete'),
    path('orders/', order_list, name='vendor_orders'),
    path('vendor-reviewes', vendor_products_with_reviews, name='vendor_products_with_reviews'),

]