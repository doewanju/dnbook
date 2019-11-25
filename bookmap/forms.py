from django import forms
from .models import Review, BookStore

class ReviewForm(forms.ModelForm):
    #content = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'후기를 입력하세요'}), label='')
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder':' 후기를 입력해주세요.'}), label='')

    class Meta:
        model = Review
        fields = ['content']

class StoreEditForm(forms.ModelForm):
    class Meta:
        model = BookStore
        fields = ['addr', 'phone_number', 'site', 'img', 'insta', 'email', 'openhour']
