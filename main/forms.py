from django import forms
from bookmap.models import BookStore

class AddstoreForm(forms.ModelForm):
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '  전화 번호(000-0000-0000)'}), label='')
    saup = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '  사업자 등록번호(000-00-00000)'}), label='')

    class Meta:
        model = BookStore
        fields = ['phone_number','saup']