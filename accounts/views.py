from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import SellerRegistrationForm, SellerProfileForm, CustomerRegistrationForm, AddressForm, PasswordChangeForm, \
    EditUserProfileForm
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from django.contrib import messages
from kavenegar import *  # kaveh negar sms service
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Address, SellerProfile
from .serializers import AddressSerializer
from rest_framework import status
from cart.views import CartManager
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

User = get_user_model()

API_KEY = '774F533338376574547369663350346C6843776350796231717268324F5041342F4973747941336C2F44303D'  # api_key for kaveh negar


def send_sms(receptor, token):
    try:
        api = KavenegarAPI(API_KEY)
        params = {
            'receptor': receptor,
            'template': 'این قسمت رو باید توی پنل سایت کاوه نگار ایجاد و نام تمپلت رو اینجا بنویسید:',
            'token': token,
            'type': 'sms',  # sms
        }
        response = api.verify_lookup(params)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)


def user_login(request):
    next_url = request.GET.get('next', '') or request.POST.get('next', '')  # GET و POST را بررسی کنید

    if request.method == 'POST':
        identifier = request.POST.get('identifier')
        password = request.POST.get('password')

        # احراز هویت کاربر
        try:
            user = User.objects.get(email=identifier)
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                # سبد خرید را با کاربر مرتبط کنید
                cart = CartManager.get_or_create_cart(request)
                CartManager.associate_cart_with_user(cart, user)

                if next_url:
                    return redirect(next_url)
                return redirect('home')
            else:
                return render(request, 'accounts/login.html',
                              {'next': next_url, 'error_message': "جزئیات ورود اشتباه است."})
        except User.DoesNotExist:
            return render(request, 'accounts/login.html', {'next': next_url, 'error_message': "کاربر یافت نشد."})

    return render(request, 'accounts/login.html', {'next': next_url})


def otp_login(request):
    if request.method == 'POST':
        identifier = request.POST.get('identifier')

        # بررسی وجود شماره تلفن
        user = User.objects.filter(phone_number=identifier).first()
        if user:
            # ارسال OTP
            otp = get_random_string(length=6, allowed_chars='0123456789')
            user.otp = otp
            user.save()
            send_sms(identifier, otp)

            return JsonResponse({'message': 'کد OTP به شماره شما ارسال شد.'}, status=200)
        else:
            return JsonResponse({'error': 'کاربر یافت نشد.'}, status=404)

    return render(request, 'accounts/otp_login.html')


def verify_otp(request):
    if request.method == 'POST':
        entered_phone_number = request.POST['phone_number']
        entered_otp = request.POST['otp']
        user = User.objects.filter(phone_number=entered_phone_number).first()

        if user and user.otp == entered_otp:
            login(request, user)
            user.otp = ''  # جهت پاک کردن OTP بعد از ورود موفق
            user.save()
            return JsonResponse({'message': 'ورود موفق.'})
        else:
            return JsonResponse({'error': 'کد وارد شده نامعتبر است.'}, status=400)

    return render(request, 'accounts/verify_otp.html')


def register_customer(request):
    if request.method == 'POST':
        user_form = CustomerRegistrationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password1'])
            user.user_type = 1  # مشتری
            user.save()
            login(request, user)
            return redirect('home')
    else:
        user_form = CustomerRegistrationForm()

    return render(request, 'accounts/register_customer.html', {'user_form': user_form})


def register_seller(request):
    if request.method == 'POST':
        user_form = SellerRegistrationForm(request.POST)
        profile_form = SellerProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.user_type = 2  # فروشنده
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            login(request, user)
            return redirect('seller_dashboard')

    else:
        user_form = SellerRegistrationForm()
        profile_form = SellerProfileForm()

    return render(request, 'accounts/register_seller.html', {'user_form': user_form, 'profile_form': profile_form})


class AddressListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # اختصاص کاربر جاری به آدرس
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddressDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


@login_required
def address_list(request):
    addresses = Address.objects.filter(user=request.user)
    return render(request, 'accounts/address_list.html', {'addresses': addresses})


@login_required
def address_create(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect('address_list')
    else:
        form = AddressForm()
    return render(request, 'accounts/address_form.html', {'form': form})


@login_required
def address_update(request, pk):
    address = get_object_or_404(Address, pk=pk, user=request.user)
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect('address_list')
    else:
        form = AddressForm(instance=address)
    return render(request, 'accounts/address_form.html', {'form': form})


@login_required
def address_delete(request, pk):
    address = get_object_or_404(Address, pk=pk, user=request.user)
    if request.method == 'POST':
        address.delete()
        return redirect('address_list')
    return render(request, 'accounts/address_confirm_delete.html', {'address': address})


@login_required
def change_password(request):
    user = request.user  # استفاده از کاربر جاری
    user_type = user.user_type  # دریافت نوع کاربر

    # انتخاب قالب بر اساس نوع کاربر
    if user_type == 1:  # مشتری
        base_template = 'customers/base.html'
    elif user_type == 2:  # فروشنده
        base_template = 'vendors/base.html'

    if request.method == 'POST':
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # به‌روز رسانی نشست با رمز عبور جدید
            return redirect('password_change_done')
    else:
        form = PasswordChangeForm(user)

    return render(request, 'accounts/change_password.html', {
        'form': form,
        'base_template': base_template  # ارسال نام قالب به صفحه
    })


@login_required
def change_password_done(request):
    user = request.user  # استفاده از کاربر جاری
    user_type = user.user_type  # دریافت نوع کاربر

    # انتخاب قالب بر اساس نوع کاربر
    if user_type == 1:  # Customer
        base_template = 'customers/base.html'
    elif user_type == 2:  # Seller
        base_template = 'vendors/base.html'

    messages.success(request, 'رمز عبور شما با موفقیت تغییر یافت.')
    return render(request, 'accounts/change_password_done.html', {'base_template': base_template})


@login_required
def edit_phone(request):
    user = request.user  # استفاده از کاربر جاری
    user_type = user.user_type  # دریافت نوع کاربر

    # انتخاب قالب بر اساس نوع کاربر
    if user_type == 1:  # Customer
        base_template = 'customers/base.html'
    elif user_type == 2:  # Seller
        base_template = 'vendors/base.html'
    if request.method == 'POST':
        new_phone_number = request.POST.get('new_phone_number')

        # ارسال OTP
        otp = get_random_string(length=6, allowed_chars='0123456789')
        request.user.otp = otp  # ذخیره OTP برای کاربر
        request.user.save()

        send_sms(new_phone_number, f"کد تایید برای تغییر شماره تلفن: {otp}")

        return JsonResponse({'message': 'کد تایید به شماره جدید شما ارسال شد.'}, status=200)

    return render(request, 'accounts/edit_phone.html', {'base_template': base_template})


@login_required
def confirm_otp(request):
    if request.method == 'POST':
        otp_entered = request.POST.get('otp')
        new_phone_number = request.POST.get('new_phone_number')

        if request.user.otp == otp_entered:
            request.user.phone_number = new_phone_number
            request.user.otp = None  # حذف OTP بعد از تایید
            request.user.save()
            return JsonResponse({'message': 'شماره تلفن شما با موفقیت تغییر کرد.'}, status=200)
        else:
            return JsonResponse({'error': 'کد تایید معتبر نیست.'}, status=400)

    return JsonResponse({'error': 'درخواست نامعتبر است.'}, status=400)


def edit_seller_profile(request):
    profile = get_object_or_404(SellerProfile, user=request.user)

    if request.method == 'POST':
        form = EditUserProfileForm(request.POST, user=request.user, instance=profile)
        if form.is_valid():
            # به‌روز کردن مشخصات کاربر
            profile = form.save(commit=False)
            user = request.user
            user.email = form.cleaned_data['email']  # ذخیره ایمیل جدید
            user.save()
            profile.save()  # ذخیره مشخصات فروشنده
            return redirect('seller_dashboard')
    else:
        form = EditUserProfileForm(instance=profile, user=request.user)

    return render(request, 'accounts/edit_seller_profile.html', {'form': form})


# خروج
def user_logout(request):
    logout(request)
    return redirect('home')
