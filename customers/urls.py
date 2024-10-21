from django.urls import path
from .views import customer_dashboard, order_detail
from .views import review_product, order_history, edit_profile, user_reviews


urlpatterns = [
    path('edit-profile/', edit_profile, name='edit_profile'),
    path('review/<int:product_id>/', review_product, name='review_product'),
    path('order-history/', order_history, name='order_history'),
    path('order/<int:order_id>/', order_detail, name='order_detail'),
    path('dashboard/', customer_dashboard, name='customer_dashboard'),
    path('my-reviews/', user_reviews, name='user_reviews'),
]