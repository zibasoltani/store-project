from django.test import TestCase
from accounts.models import User, SellerProfile

class UserModelTestCase(TestCase):
    def setUp(self):
        # یک کاربر ایجاد کنید
        self.user = User.objects.create(
            username='testuser',
            email='testuser@example.com',
            password='password123',
            user_type=1  #مشتری
        )

    def test_user_creation(self):
        # بررسی کنید که آیا کاربر با موفقیت ایجاد شده است
        self.assertIsNotNone(self.user)
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'testuser@example.com')
        self.assertEqual(self.user.user_type, 1)

    def test_user_update(self):
        # کاربر را به روز کنید
        self.user.phone_number = '09123456789'
        self.user.save()

        # بررسی کنید که آیا کاربر با موفقیت به روز شده است
        self.assertEqual(self.user.phone_number, '09123456789')

class SellerProfileModelTestCase(TestCase):
    def setUp(self):
        # یک کاربر ایجاد کنید
        self.user = User.objects.create(
            username='testuser',
            email='testuser@example.com',
            password='password123',
            user_type=2  # فروشنده
        )

        # نمایه فروشنده ایجاد کنید
        self.seller_profile = SellerProfile.objects.create(
            user=self.user,
            first_name='John',
            last_name='Doe',
            gender=1,  # مرد
            shop_name='My Shop',
            shop_address='Tehran, Iran'
        )

    def test_seller_profile_creation(self):
        # بررسی کنید که آیا نمایه فروشنده با موفقیت ایجاد شده است
        self.assertIsNotNone(self.seller_profile)
        self.assertEqual(self.seller_profile.user, self.user)
        self.assertEqual(self.seller_profile.first_name, 'John')
        self.assertEqual(self.seller_profile.last_name, 'Doe')
        self.assertEqual(self.seller_profile.gender, 1)
        self.assertEqual(self.seller_profile.shop_name, 'My Shop')
        self.assertEqual(self.seller_profile.shop_address, 'Tehran, Iran')

    def test_seller_profile_update(self):
        # نمایه فروشنده را به روز کنید
        self.seller_profile.shop_name = 'My New Shop'
        self.seller_profile.save()

        # بررسی کنید که آیا نمایه فروشنده با موفقیت به روز شده است
        self.assertEqual(self.seller_profile.shop_name, 'My New Shop')

