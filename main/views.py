from django.shortcuts import render, redirect
from vendors.models import Product, Category
from accounts.models import SellerProfile
from django.shortcuts import get_object_or_404
from .forms import ReviewForm
from cart.models import Order
from django.db.models import Avg
from vendors.models import Discount


def home(request):
    categories = Category.objects.all()
    sellers = SellerProfile.objects.all()

    search_query = request.GET.get('search', '')
    sort_option = request.GET.get('sort', '')

    # محصولات با رتبه بندی
    products = Product.objects.annotate(average_rating=Avg('reviews__rating'))

    # فیلتر کردن بر اساس پرس و جو و جستجو
    if search_query:
        products = products.filter(name__icontains=search_query)

    # مرتب سازی محصولات
    if sort_option == 'best_selling':
        products = products.order_by('-sales_count')
    elif sort_option == 'highest_rated':
        products = products.order_by('-average_rating')  #با استفاده از میانگین رتبه بندی میشود
    elif sort_option == 'most_expensive':
        products = products.order_by('-price')

    # قیمت نهایی را از قبل محاسبه کنید
    if products:
        for product in products:
            discount = Discount.objects.filter(product=product).first()
            # محاسبه امتیاز متوسط
            average_rating = product.reviews.aggregate(Avg('rating'))['rating__avg'] or 0
            if discount:
                dis_val = discount.value
                dis_type = discount.discount_type

                if dis_val > 0 and dis_type == 'percentage':
                    product.final_price = product.price * (1 - (dis_val / 100))
                elif dis_val > 0 and dis_type == 'fixed':
                    product.final_price = product.price - dis_val
                else:
                    product.final_price = product.price
            else:
                # تخفیف در دسترس نیست
                product.final_price = product.price

        user_type = request.user.user_type if request.user.is_authenticated else None
        return render(request, 'main/home.html', {
            'products': products,
            'categories': categories,
            'sellers': sellers,
            'user_type': user_type,
            'dis_val': dis_val,
            'dis_type': dis_type,
            'average_rating': average_rating,
        })
    else:
        products = None
        dis_val = None
        dis_type = None
        user_type = request.user.user_type if request.user.is_authenticated else None
        return render(request, 'main/home.html', {
            'products': products,
            'categories': categories,
            'sellers': sellers,
            'user_type': user_type,
            'dis_val': dis_val,
            'dis_type': dis_type,
        })


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # محاسبه امتیاز متوسط
    average_rating = product.reviews.aggregate(Avg('rating'))['rating__avg'] or 0

    reviews = product.reviews.all()

    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if request.user.is_authenticated:
            if not product.reviews.filter(user=request.user).exists():
                if form.is_valid():
                    review = form.save(commit=False)
                    review.product = product
                    review.user = request.user

                    # اگر کاربر محصول را خریده باشد، امتیاز را ذخیره می‌کنیم
                    if has_user_purchased_product(request.user, product):
                        review.rating = form.cleaned_data.get('rating')
                    else:
                        review.rating = None

                    review.save()
                    return redirect('product_detail', product_id=product.id)
                else:
                    for field in form.errors:
                        form.add_error(field, form.errors[field])
            else:
                form.add_error(None, "شما قبلاً این محصول را بررسی کرده‌اید.")
        else:
            return redirect('login')
    else:
        form = ReviewForm()

    # Pre-calculate final price

    discount = Discount.objects.filter(product=product).first()
    dis_val = discount.value
    dis_type = discount.discount_type
    if dis_val > 0 and dis_type == 'percentage':
        product.final_price = product.price * (1 - (dis_val / 100))
    elif dis_val > 0 and dis_type == 'fixed':
        product.final_price = product.price - dis_val
    else:
        product.final_price = product.price

    return render(request, 'main/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'form': form,
        'average_rating': average_rating,  # اضافه کردن امتیاز متوسط
        'dis_val': dis_val,
    })


def seller_detail(request, id):
    # ابتدا اطلاعات فروشنده و دسته‌بندی‌ها را دریافت کنید
    seller = SellerProfile.objects.get(id=id)
    categories = Category.objects.filter(seller_id=id)

    # تعریف جستجو
    search_query = request.GET.get('search', '')
    sort_option = request.GET.get('sort', '')

    # در ابتدا تمام محصولات فروشنده را دریافت کنید
    products = Product.objects.filter(seller_id=id).annotate(average_rating=Avg('reviews__rating'))

    # اگر کوئری جستجو موجود باشد، محصولات را فیلتر کنید
    if search_query:
        products = products.filter(name__icontains=search_query)

    # مرتب‌سازی محصولات بر اساس گزینه انتخاب شده
    if sort_option == 'best_selling':
        products = products.order_by('-sales_count')
    elif sort_option == 'highest_rated':
        products = products.order_by('-average_rating')  # استفاده از میانگین امتیاز محاسبه شده
    elif sort_option == 'most_expensive':
        products = products.order_by('-price')
    elif sort_option == 'cheapest':
        products = products.order_by('price')

    if products:
        # قیمت نهایی را از قبل محاسبه میکنیم
        for product in products:
            discount = Discount.objects.filter(product=product).first()
            # محاسبه امتیاز متوسط
            average_rating = product.reviews.aggregate(Avg('rating'))['rating__avg'] or 0
            dis_val = discount.value
            dis_type = discount.discount_type
            if dis_val > 0 and dis_type == 'percentage':
                product.final_price = product.price * (1 - (dis_val / 100))
            elif dis_val > 0 and dis_type == 'fixed':
                product.final_price = product.price - dis_val
            else:
                product.final_price = product.price

        user_type = request.user.user_type if request.user.is_authenticated else None
        return render(request, 'main/seller_detail.html', {
            'products': products,
            'categories': categories,
            'seller': seller,
            'user_type': user_type,
            'dis_val': dis_val,
            'dis_type': dis_type,
            'average_rating': average_rating,
        })
    else:
        products = None
        dis_val = None
        dis_type = None

        user_type = request.user.user_type if request.user.is_authenticated else None

        return render(request, 'main/seller_detail.html', {
            'products': products,
            'categories': categories,
            'seller': seller,
            'user_type': user_type,
            'dis_val': dis_val,
            'dis_type': dis_type,
        })


def category_products(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)  #دسته بندی را یک فیلد خارجی در محصول فرض میکنیم

    # تعریف جستجو
    search_query = request.GET.get('search', '')
    sort_option = request.GET.get('sort', '')

    # اگر کوئری جستجو موجود باشد، محصولات را فیلتر کنید
    if search_query:
        products = products.filter(name__icontains=search_query)

    # مرتب‌سازی محصولات بر اساس گزینه انتخاب شده
    if sort_option == 'best_selling':
        products = products.order_by('-sales_count')
    elif sort_option == 'highest_rated':
        products = products.order_by('-average_rating')  # استفاده از میانگین امتیاز محاسبه شده
    elif sort_option == 'most_expensive':
        products = products.order_by('-price')
    elif sort_option == 'cheapest':
        products = products.order_by('price')

    if products:
        # قیمت نهایی را از قبل محاسبه میشود
        for product in products:
            discount = Discount.objects.filter(product=product).first()
            # محاسبه امتیاز متوسط
            average_rating = product.reviews.aggregate(Avg('rating'))['rating__avg'] or 0
            if discount:  # بررسی می‌کنیم که آیا تخفیفی وجود دارد یا خیر
                dis_val = discount.value
                dis_type = discount.discount_type
                if dis_val > 0 and dis_type == 'percentage':
                    product.final_price = product.price * (1 - (dis_val / 100))
                elif dis_val > 0 and dis_type == 'fixed':
                    product.final_price = product.price - dis_val
                else:
                    product.final_price = product.price

            else:
                dis_val = 0  # یا هر مقدار پیش‌فرضی که می‌خواهید
                dis_type = None  # یا هر مقدار پیش‌فرضی که می‌خواهید
                product.final_price = product.price  # اگر تخفیف وجود نداشته باشد، قیمت نهایی برابر با قیمت اصلی خواهد بود

        user_type = request.user.user_type if request.user.is_authenticated else None
        return render(request, 'main/seller_detail.html', {
            'products': products,
            'category': category,
            'user_type': user_type,
            'dis_val': dis_val,
            'dis_type': dis_type,
            'average_rating': average_rating,
        })
    else:
        products = None
        dis_val = None
        dis_type = None

        user_type = request.user.user_type if request.user.is_authenticated else None
        return render(request, 'main/seller_detail.html', {
            'products': products,
            'category': category,
            'user_type': user_type,
            'dis_val': dis_val,
            'dis_type': dis_type,
        })


def has_user_purchased_product(user, product):
    if user.is_authenticated:
        # بررسی اینکه آیا کاربر ، محصول را در سفارشاتش خریداری کرده است یا خیر
        orders = Order.objects.filter(user=user)
        for order in orders:
            if order.items.filter(product=product).exists():
                return True
    return False
