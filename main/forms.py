from django import forms
from bookmap.models import BookStore

class AddstoreForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '책방 이름'}), label='책방이름')
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '전화 번호(하이픈(-) 포함)'}), label='전화번호')
    site = forms.URLField(widget=forms.URLInput(attrs={'placeholder': '홈페이지 주소'}), label='홈페이지')
    insta = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '인스타그램 ID'}), label='인스타그램')
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': '이메일'}), label='이메일주소')
    openhour = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '영업 시간'}), label='영업시간')
    saup = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '사업자 등록번호(하이픈(-) 포함)'}), label='사업자등록번호')

    class Meta:
        model = BookStore
        fields = ['name', 'phone_number', 'site', 'img', 'insta', 'email', 'openhour', 'saup']