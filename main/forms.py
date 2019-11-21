from django import forms
from bookmap.models import BookStore

class AddstoreForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '  책방 이름'}), label='')
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '  전화 번호(하이픈(-) 포함)'}), label='')
    site = forms.URLField(widget=forms.URLInput(attrs={'placeholder': '  홈페이지 주소'}), label='')
    insta = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '  인스타그램 ID'}), label='')
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': '  이메일'}), label='')
    openhour = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '  영업 시간'}), label='')
    saup = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '  사업자 등록번호(하이픈(-) 포함)'}), label='')

    class Meta:
        model = BookStore
        fields = ['name', 'phone_number', 'site', 'img', 'insta', 'email', 'openhour', 'saup']