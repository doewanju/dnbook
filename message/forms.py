from django import forms
from .models import Message
from django.forms import ModelChoiceField
from django.contrib.auth.models import User

class MessageForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea, label='')

    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content':forms.Textarea(
                attrs = {
                    'class':'form-control',
                    'placeholder':'보낼 내용을 입력해주세요.',
                }
            )
        }