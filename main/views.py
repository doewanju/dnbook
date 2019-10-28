from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import auth
from .models import Normalprofile, Bossprofile
from bookmap.models import BookStore, Scrap, Stamp
from others.models import Culture, Comment

# Create your views here.


def home(request):
    return render(request,'home.html')

def mypage(request):
    user = request.user
    if user.is_superuser:
        return render(request, 'home.html', {'error': 'superuser는 mypage가 없습니다!'})
    else:
        try:
            profile = Bossprofile.objects.get(user=request.user)
            store_name = BookStore.objects.get(boss=request.user).name
        except Bossprofile.DoesNotExist:
            profile = Normalprofile.objects.get(user=request.user)
            store_name = ""
    scraps = Scrap.objects.filter(user=request.user)
    mystamp = profile.stampcount
    # store = BookStore.objects.get(boss=request.user)
    # cultures = Culture.objects.filter(store=store)
    comments = Comment.objects.filter(user=request.user)
    return render(request,'mypage.html', {
                        'scraps':scraps, 
                        'stamp':mystamp, 
                        'user':user, 
                        'profile':profile, 
                        'store_name':store_name,
                        # 'cultures':cultures,
                        'comments':comments,
                        })

def stamppush(request):
    #if request.method == 'GET':
    userid = request.GET['userid']
    user = User.objects.get(username=userid)
    count = request.GET['count']
    store = BookStore.objects.get(boss=request.user)
    stamp = Stamp(user=user, store=store, count=count)
    stamp.save()
    return redirect('mypage')

def signup(request):
    return render(request,'signup.html')

def normal(request):
   if request.method == 'POST':
       # User has info and wants an account now! 즉 [signup!]버튼을 눌렀을 때 일어나는 일
       if request.POST['password1'] == request.POST['password2']:
           try:
               user = User.objects.get(username=request.POST['username'])
               return render(request, 'normal.html', {'error': 'Username has already been taken'})
           except User.DoesNotExist:
               user = User.objects.create_user(
                   username=request.POST['username'], 
                   password=request.POST['password1'])
               nickname=request.POST['nickname']
               email=request.POST['email']
               normalprofile = Normalprofile(user=user, nickname=nickname, email=email)
               normalprofile.save()
               auth.login(request, user)
               return redirect('home')
       else:
           return render(request, 'normal.html', {'error': 'Passwords must match'})
   else:
       # User wants to enter info --> 유저가 정보를 입력하고 있는 중임.
       return render(request, 'normal.html')

def boss(request):
   if request.method == 'POST':
       # User has info and wants an account now! 즉 [signup!]버튼을 눌렀을 때 일어나는 일
       if request.POST['password1'] == request.POST['password2']:
           try:
               user = User.objects.get(username=request.POST['username'])
               return render(request, 'boss.html', {'error': 'Username has already been taken'})
           except User.DoesNotExist:
                user = User.objects.create_user(
                   username=request.POST['username'], 
                   password=request.POST['password1'])
                #storename = request.POST["storename"]
                nickname=request.POST['nickname']
                email=request.POST['email']
                introduce=request.POST['introduce']
                bossprofile = Bossprofile(user=user, nickname=nickname, email=email, introduce=introduce)
                bossprofile.save()
                #선택한 책방 이름에 맞는 책방모델에 >>>책방모델.add(bossprofile), >>>책방모델.save()
                storename = request.POST['storename']
                bookstore = BookStore.objects.get(name=storename)
                bookstore.boss=User.objects.get(username=user)
                bookstore.save()
                auth.login(request, user)
                return redirect('home')
       else:
           return render(request, 'boss.html', {'error': 'Passwords must match'})
   elif request.method == 'GET':
       bsname = request.GET.get("bsname", False)
       return render(request, 'boss.html', {"bsname":bsname})
   else:
       # User wants to enter info --> 유저가 정보를 입력하고 있는 중임.
        return render(request, 'boss.html')

def login(request):
   if request.method == 'POST': #로그인 버튼을 눌렀을 때
       username = request.POST['username']
       password = request.POST['password']
       user = auth.authenticate(request, username=username, password=password)
       if user is not None: #사용자 정보를 알맞게 입력한 경우
           auth.login(request, user)
           return redirect('home')
       else: #잘못 입력한경우
           return render(request, 'login.html', {'error' : 'username or password is incorrect.'})
   else:
       return render(request, 'login.html')


def logout(request):
   if request.method == 'POST':
       auth.logout(request)
       return redirect('home')
   return render(request, 'signup.html')

def bossbook(request):
    bookstores = BookStore.objects
    return render(request,'bossbook.html', {'bookstores':bookstores})

def ranking(request):
    users = Normalprofile.objects.all()
    name = []
    stamp = []
    for i in users:
        name.append(i.nickname)
        stamp.append(i.stampcount())
    first, second, third = -1, -1, -1
    for i in stamp:
        if first <= i:
            third = second
            second = first
            first = i
        elif second <= i:
            third = second
            second = i
        elif third <= i:
            third = i
    if third != -1:
        idx = stamp.index(third)
        nick = Normalprofile.objects.filter(nickname=name[idx])[0].nickname
        del name[idx]
        del stamp[idx]
    else:
        nick='없음'
        third=None
    res_third = {'nickname': nick, 'total_stamp': third}

    if second != -1:
        idx = stamp.index(second)
        nick = Normalprofile.objects.filter(nickname=name[idx])[0].nickname
        del name[idx]
        del stamp[idx]
    else:
        nick='없음'
        second=None
    res_second = {'nickname': nick, 'total_stamp':second}
        
    if first != -1:
        idx = stamp.index(first)
        nick = Normalprofile.objects.filter(nickname=name[idx])[0].nickname
    else:
        nick='없음'
    res_first = {'nickname': nick, 'total_stamp':first}
    
    return render(request,'ranking.html', {'first':res_first, 'second':res_second, 'third':res_third})

def info(request):
    return render(request,'info.html')