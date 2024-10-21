from django import forms
from .models import User, CustomerProfile


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = ['first_name', 'last_name', 'gender']  # فیلدهای ویرایش شونده
        

class UserEditForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ['email', 'username']
