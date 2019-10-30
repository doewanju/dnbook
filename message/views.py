from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Message
from django.contrib.auth.models import User
from .forms import MessageForm
from bookmap.models import BookStore
from django.db.models import Q
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
    messages = Message.objects.filter(Q(recipient=request.user) | Q(sender=request.user)).order_by('-sentAt')
    testlist = []
    for who in messages:
        if who.recipient == request.user:
            if who.sender not in testlist:
                testlist.append(who.sender)
        else:
            if who.recipient not in testlist:
                testlist.append(who.recipient)

    test2 = []   
    for i in testlist:
        q = Q()
        q.add(Q(recipient=request.user) & Q(sender=i), q.OR)
        q.add(Q(recipient=i) & Q(sender=request.user), q.OR)
        x = Message.objects.filter(q).order_by('-sentAt')[0]
        test2.append(x)

    
    

    receivedList = Message.objects.filter(recipient=request.user) #나한테 보낸 쪽지
    
    #testlist = []
    #for who in receivedList:
    #    testlist.append(Message.objects.filter(recipient=request.user, sender=who).order_by('-sentAt')[0])

    sentList = Message.objects.filter(sender=request.user) #내가 보낸 쪽지
    return render(request, 'listMessage.html', {'test':test2, 'rlist':receivedList, 'slist':sentList, 'messages':messages})

def viewMessage(request, message_id):
    if not request.user.is_authenticated:
        return redirect('login')
    messages = get_object_or_404(Message, pk=message_id)
    if messages.sender != request.user:
        messages.isRead = True
    messages.save()
    return render(request, 'viewMessage.html', {'message':messages})

def chat(request, user_id):
    friend = get_object_or_404(User, pk=user_id)
    q = Q()
    q.add(Q(recipient=request.user) & Q(sender=friend), q.OR)
    q.add(Q(recipient=friend) & Q(sender=request.user), q.OR)
    messages = Message.objects.filter(q).order_by('sentAt')

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = get_object_or_404(User, pk=user_id)
            message.content = form.cleaned_data.get("content")
            message.save()
            form = MessageForm
            return render(request, 'chat.html', {'form':form, 'messages':messages})
        else:
            return HttpResponse("해당하는 아이디가 존재하지 않습니다. 다시 확인해주세요.")
    else:
        form = MessageForm()
        return render(request, 'chat.html', {'form':form, 'messages':messages})