from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Message
from django.contrib.auth.models import User
from .forms import MessageForm
from bookmap.models import BookStore
from main.models import Normalprofile, Bossprofile
from django.db.models import Q


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

    return render(request, 'listMessage.html', {'test':test2})


def chat(request, user_id):
    friend = get_object_or_404(User, pk=user_id)
    if friend.is_superuser:
        return render(request, 'home.html')
    try:
        other = Bossprofile.objects.get(user = friend)
    except Bossprofile.DoesNotExist:
        other = Normalprofile.objects.get(user = friend)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = get_object_or_404(User, pk=user_id)
            message.content = form.cleaned_data.get("content")
            message.save()
            form = MessageForm

            q = Q()
            q.add(Q(recipient=request.user) & Q(sender=friend), q.OR)
            q.add(Q(recipient=friend) & Q(sender=request.user), q.OR)
            messages = Message.objects.filter(q).order_by('sentAt')

            for i in messages:
                if i.recipient == request.user:
                    i.isRead = True
                    i.save()
            return render(request, 'chat.html', {'form':form, 'messages':messages, 'other':other})
        else:
            return HttpResponse("해당하는 아이디가 존재하지 않습니다. 다시 확인해주세요.")
    else:
        q = Q()
        q.add(Q(recipient=request.user) & Q(sender=friend), q.OR)
        q.add(Q(recipient=friend) & Q(sender=request.user), q.OR)
        messages = Message.objects.filter(q).order_by('sentAt')

        for i in messages:
            if i.recipient == request.user:
                i.isRead = True
                i.save()

        form = MessageForm()
        return render(request, 'chat.html', {'form':form, 'messages':messages, 'other':other})