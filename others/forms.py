from django import forms
from .models import Comment, Culture

class CommentForm(forms.ModelForm):
  content = forms.CharField(widget=forms.Textarea(attrs={'placeholder':' 댓글 내용을 입력해주세요.'}), label='')
    
  class Meta:
        model = Comment
        fields = ['content']

class CultureForm(forms.ModelForm):
    start_time = forms.CharField(widget=forms.TextInput(attrs={'placeholder':' * 2019-01-01 형태로 입력해주세요.'}))
    finish_time = forms.CharField(widget=forms.TextInput(attrs={'placeholder':' * 2019-01-01 형태로 입력해주세요.'}))
    class Meta:
        model = Culture
        fields = ['title', 'picture', 'start_time', 'finish_time', 'content', 'group']