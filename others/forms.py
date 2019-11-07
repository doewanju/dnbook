from django import forms
from .models import Comment, Culture

class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder':' 댓글을 입력해주세요.'}), label='')

    class Meta:
        model = Comment
        fields = ['content']

class CultureForm(forms.ModelForm):
    class Meta:
        model = Culture
        fields = ['title', 'picture', 'start_time', 'finish_time', 'content', 'group']