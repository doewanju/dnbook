from django import forms
from .models import Message
from django.forms import ModelChoiceField
from django.contrib.auth.models import User

class MessageForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = ['content']

        widgets = {
            'content':forms.Textarea(
                attrs = {
                    'class':'form-control',
                    'placeholder':'쪽지를 작성해주세요.',
                }
            )
        }