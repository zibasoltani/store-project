from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, Discount
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CategoryForm, DiscountForm, ProductForm
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from accounts.models import SellerProfile
from django.views.generic import ListView
from cart.models import Order


def category_list(request):
    categories = Category.objects.filter(seller=request.user.sellerprofile)
    return render(request, 'vendors/category_list.html', {'categories': categories})


def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.seller = request.user.sellerprofile  # هر دسته‌بندی برای فروشنده مشخصی باشد
            category.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'vendors/category_form.html', {'form': form})


def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk,
                                 seller=request.user.sellerprofile)  # استعلام دسته‌بندی مربوط به فروشنده
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'vendors/category_form.html', {'form': form})


def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk,
                                 seller=request.user.sellerprofile)  # استعلام دسته‌بندی مربوط به فروشنده
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'vendors/category_confirm_delete.html', {'category': category})


# CRUD for discount


def discount_list(request):
    discounts = Discount.objects.filter(seller=request.user.sellerprofile)
    return render(request, 'vendors/discount_list.html', {'discounts': discounts})


def discount_create(request):
    if request.method == 'POST':
        form = DiscountForm(request.POST)
        if form.is_valid():
            discount = form.save(commit=False)
            discount.seller = request.user.sellerprofile  # تخصیص به فروشنده
            discount.save()
            messages.success(request, 'تخفیف با موفقیت ایجاد شد.')
            return redirect('discount_list')
    else:
        form = DiscountForm()
    return render(request, 'vendors/discount_form.html', {'form': form})


def discount_update(request, pk):
    discount = get_object_or_404(Discount, pk=pk, seller=request.user.sellerprofile)
    if request.method == 'POST':
        form = DiscountForm(request.POST, instance=discount)
        if form.is_valid():
            form.save()
            messages.success(request, 'تخفیف با موفقیت ویرایش شد.')
            return redirect('discount_list')
    else:
        form = DiscountForm(instance=discount)
    return render(request, 'vendors/discount_form.html', {'form': form})


def discount_delete(request, pk):
    discount = get_object_or_404(Discount, pk=pk, seller=request.user.sellerprofile)
    if request.method == 'POST':
        discount.delete()
        messages.success(request, 'تخفیف با موفقیت حذف شد.')
        return redirect('discount_list')  # تغییر به لیست تخفیف‌ها
    return render(request, 'vendors/discount_confirm_delete.html', {'discount': discount})


@login_required
def seller_dashboard(request):
    try:
        seller_profile = request.user.sellerprofile
    except SellerProfile.DoesNotExist:
        seller_profile = None  #می توانید ایجاد نمایه جدید یا تغییر مسیر را تنظیم کنید

    context = {
        'seller_profile': seller_profile,
    }
    return render(request, 'vendors/dashboard.html', context)


class AddProductView(FormView):
    template_name = 'vendors/add_product.html'
    form_class = ProductForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        product = form.save(commit=False)
        product.seller = self.request.user.sellerprofile  # Seller را تنظیم کن
        product.save()  # ذخیره محصول

        messages.success(self.request, 'محصول با موفقیت اضافه شد')
        return redirect('product_list')

    def form_invalid(self, form):
        messages.error(self.request, 'مشکلی در ارسال اطلاعات وجود دارد.')
        return self.render_to_response(self.get_context_data(form=form))


class ProductUpdateView(SuccessMessageMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'vendors/edit_product.html'
    success_message = "محصول با موفقیت ویرایش شد"
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        # در صورتی که نیاز به انجام کاری خاص بعد از اعتبارسنجی فرم دارید اینجا اضافه کنید
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = self.object  # به محصول جاری دسترسی پیدا کنید
        return context


@login_required
def product_list(request):
    products = Product.objects.filter(seller=request.user.sellerprofile)
    return render(request, 'vendors/product_list.html', {'products': products})


@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        product.delete()
        messages.success(request, 'محصول با موفقیت حذف شد.')
        return redirect('product_list')  # فرض می‌کنیم که نام آدرس مربوط به لیست محصولات 'product_list' است.

    return render(request, 'vendors/confirm_delete.html', {'product': product})


@login_required
def order_list(request):
    # 1. دریافت فروشنده کاربر فعلی
    seller_profile = request.user.sellerprofile

    # 2. فیلتر کردن سفارشات بر اساس فروشنده
    orders = Order.objects.filter(items__product__seller=seller_profile).distinct()

    # 3. ارسال داده‌ها به قالب
    context = {
        'orders': orders
    }
    return render(request, 'vendors/vendor_orders.html', context)


def vendor_products_with_reviews(request):
    # دریافت محصولات مرتبط با فروشنده
    seller_profile = request.user.sellerprofile
    products = Product.objects.filter(seller_id=seller_profile).prefetch_related('reviews')

    context = {
        'products': products,
    }

    return render(request, 'vendors/vendor_products_with_reviews.html', context)




















def manage_sellers(request):
    # Logic to manage sellers
    pass


def manage_products(request):
    # Logic to manage products
    pass


def reports(request):
    # Logic to generate reports
    pass
