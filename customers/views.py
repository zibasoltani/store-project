from django.shortcuts import render, redirect
from .models import CustomerProfile
from cart.models import Order
from main.models import Review
from .forms import ProfileEditForm, UserEditForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from vendors.models import Product


@login_required
def edit_profile(request):
    user = request.user
    profile, created = CustomerProfile.objects.get_or_create(user=user)  # بوجود آوردن پروفایل در صورت وجود نداشتن
    profile_edit_form = ProfileEditForm(instance=profile)
    user_edit_form = UserEditForm(instance=user)

    if request.method == 'POST':
        profile_edit_form = ProfileEditForm(request.POST, instance=profile)
        user_edit_form = UserEditForm(request.POST, instance=user)

        if profile_edit_form.is_valid() and user_edit_form.is_valid():
            profile_edit_form.save()
            user_edit_form.save()  # فقط اطلاعات دیگر را ذخیره کن

            messages.success(request, 'پروفایل با موفقیت ویرایش شد.')
            return redirect('edit_profile')  # مسیر به صفحه ویرایش پروفایل

    context = {
        'profile_edit_form': profile_edit_form,
        'user_edit_form': user_edit_form,
        'phone_number': user.phone_number  # برای نمایش شماره تلفن
    }
    return render(request, 'customers/edit_profile.html', context)


@login_required
def review_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        rating = request.POST['rating']
        comment = request.POST['comment']
        Review.objects.create(user=request.user, product=product, rating=rating, comment=comment)
        return redirect('user_reviews')  # یا صفحه مورد نظر دیگری
    return render(request, 'customers/review_form.html', {'product': product})


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'customers/order_history.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'customers/order_detail.html', {'order': order})


@login_required
def customer_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'customers/dashboard.html', {})


@login_required
def user_reviews(request):
    # گرفتن بررسی‌های کاربر
    user_reviews = Review.objects.filter(user=request.user).select_related('product')

    # گرفتن سفارشات کاربر
    orders = Order.objects.filter(user=request.user)

    #  لیستی از محصولات خریداری‌شده رو به ما میدهد
    purchased_products = Product.objects.filter(orderitem__order__in=orders).distinct()

    # ایجاد یک مجموعه از شناسه‌های محصولاتی که کاربر نظراتی برای آنها ثبت کرده است
    reviewed_product_ids = set(user_reviews.values_list('product_id', flat=True))

    # تولید لیستی از محصولاتی که کاربر نظری روی آنها ثبت نکرده است
    products_without_reviews = purchased_products.exclude(id__in=reviewed_product_ids)

    context = {
        'reviews': user_reviews,
        'products_without_reviews': products_without_reviews
    }

    return render(request, 'customers/user_reviews.html', context)
