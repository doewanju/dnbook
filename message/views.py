from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Message
from django.contrib.auth.models import User
from .forms import MessageForm
from bookmap.models import BookStore

# Create your views here.

def sendMessage(request, user_id):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            username = request.POST['recipient']
            message.recipient = User.objects.get(username=username)
            message.content = form.cleaned_data.get("content")
            message.save()
            return redirect('listMessage')
        else:
            return HttpResponse("해당하는 아이디가 존재하지 않습니다. 다시 확인해주세요.")
    else:
        recipient = get_object_or_404(User, pk=user_id)
        form = MessageForm()
        return render(request, 'sendMessage.html', {'form':form, 'recipient':recipient})

def listMessage(request):
    receivedList = Message.objects.filter(recipient=request.user)
    sentList = Message.objects.filter(sender=request.user)
    return render(request, 'listMessage.html', {'rlist':receivedList, 'slist':sentList})

def viewMessage(request, message_id):
    if not request.user.is_authenticated:
        return redirect('login')
    messages = get_object_or_404(Message, pk=message_id)
    messages.isRead = True
    messages.save()
    return render(request, 'viewMessage.html', {'message':messages})