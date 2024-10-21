from django import forms
from .models import Category, Discount, Product


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        labels = {
            'name': 'نام دسته‌بندی',
        }


class DiscountForm(forms.ModelForm):
    class Meta:
        model = Discount
        fields = ['product', 'discount_type', 'value']
        labels = {
            'product': 'محصول',
            'discount_type': 'نوع تخفیف',
            'value': 'مقدار تخفیف',
        }

    discount_type = forms.ChoiceField(choices=Discount.DISCOUNT_TYPES, label='نوع تخفیف')


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'image']
        labels = {
            'name': 'نام محصول',
            'description': 'توضیحات محصول',
            'price': 'قیمت',
            'category': 'دسته‌بندی',
            'image': 'تصویر محصول',
        }











    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="انتخاب دسته‌بندی", label=' دسته‌بندی')

    def save(self, commit=True):
        product = super().save(commit)
        
        if commit:
            product.save()  
        return product
