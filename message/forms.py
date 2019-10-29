from django import forms
from .models import Message
from django.forms import ModelChoiceField
from django.contrib.auth.models import User

class MessageForm(forms.ModelForm):
    recipient = ModelChoiceField(queryset=User.objects.all())

    class Meta:
        model = Message
        fields = ['recipient', 'content']

        widgets = {
            'recipient':forms.TextInput(),
            'content':forms.Textarea(
                attrs = {
                    'class':'form-control',
                    'placeholder':'쪽지를 작성해주세요.',
                }
            )
        }