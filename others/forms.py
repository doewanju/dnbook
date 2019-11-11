from django import forms
from .models import Comment, Culture
from django.utils.dates import MONTHS
'''
MONTHS = {
    1:_('jan'), 2:_('feb'), 3:_('mar'), 4:_('apr'),
    5:_('may'), 6:_('jun'), 7:_('jul'), 8:_('aug'),
    9:_('sep'), 10:_('oct'), 11:_('nov'), 12:_('dec')
}'''

class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder':' 댓글 내용을 입력해주세요.'}), label='')
    
    class Meta:
        model = Comment
        fields = ['content']

class CultureForm(forms.ModelForm):
    start_time = forms.DateField(widget=forms.SelectDateWidget(months=MONTHS))
    finish_time = forms.DateField(widget=forms.SelectDateWidget(months=MONTHS))

    class Meta:
        model = Culture
        fields = ['title', 'picture', 'start_time', 'finish_time', 'content', 'group']

