from django import forms
from .models import Message
from django.forms import ModelChoiceField
from django.contrib.auth.models import User

class MessageForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder':' 보낼 내용을 입력해주세요.'}), label='')


    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content':forms.Textarea(
                attrs = {
                    'auto_id' : False,
                    'class':'form-control',
                }  
            )
        }
