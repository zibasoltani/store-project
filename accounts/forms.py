from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, SellerProfile, Address
from django.contrib.auth.forms import PasswordChangeForm


class CustomerRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']
        labels = {
            'username': 'نام کاربری',
            'email': 'ایمیل',
            'phone_number': 'شماره تلفن',
            'password1': 'رمز عبور',
            'password2': 'تأیید رمز عبور',
        }


class SellerRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'phone_number']
        labels = {
            'username': 'نام کاربری',
            'password': 'رمز عبور',
            'email': 'ایمیل',
            'phone_number': 'شماره تلفن',
        }


class SellerProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)

    class Meta:
        model = SellerProfile
        fields = ['first_name', 'last_name', 'shop_name', 'shop_address']
        labels = {
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'shop_name': 'نام فروشگاه',
            'shop_address': 'آدرس فروشگاه',
        }


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['line_1', 'line_2', 'city', 'state', 'postal_code', 'country']
        labels = {
            'line_1': 'خیابان',
            'line_2': ' آدرس دقیق',
            'city': 'شهر',
            'state': 'استان',
            'postal_code': 'کد پستی',
            'country': 'کشور',
        }


class PasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='رمز عبور قبلی',
        widget=forms.PasswordInput,
        strip=False,
        help_text=None,
    )
    new_password1 = forms.CharField(
        label='رمز عبور جدید',
        widget=forms.PasswordInput,
        strip=False,
        help_text='حداقل 8 کاراکتر، شامل اعداد و حروف باشد.',
    )
    new_password2 = forms.CharField(
        label='تکرار رمز عبور جدید',
        widget=forms.PasswordInput,
        strip=False,
        help_text='لطفا رمز عبور جدید را دوباره وارد کنید.',
    )


class EditUserProfileForm(forms.ModelForm):
    email = forms.EmailField(required=True, label="ایمیل")  # اضافه کردن فیلد ایمیل

    class Meta:
        model = SellerProfile
        fields = ['first_name', 'last_name', 'gender', 'shop_name', 'shop_address',
                  'email']  # اضافه کردن ایمیل به فیلدها
        labels = {
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'gender': 'جنسیت',
            'shop_name': 'نام فروشگاه',
            'shop_address': 'آدرس فروشگاه',
            'email': 'ایمیل',  # لیبل فارسی برای ایمیل
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['email'].initial = user.email  # تنظیم ایمیل اولیه از مدل User
