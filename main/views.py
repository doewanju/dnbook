from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import auth
from .models import Normalprofile, Bossprofile
from bookmap.models import BookStore
# Create your views here.


def home(request):
    return render(request,'home.html')

def mypage(request):
    return render(request,'mypage.html')

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

"""def find(request):
    if request.method == 'GET':
        storename = request.GET["storename"]
        return storename"""