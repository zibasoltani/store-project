from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment']  # فقط فیلد نظر را نگه می‌داریم.

    rating = forms.ChoiceField(
        required=False,  
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')],
        label='امتیاز',
        widget=forms.RadioSelect(attrs={'class': 'rating'})
    )