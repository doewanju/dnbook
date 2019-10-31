from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib import auth
from .models import Normalprofile, Bossprofile
from bookmap.models import BookStore, Scrap, Stamp
from others.models import Culture, Comment
from datetime import datetime
from django.contrib.auth.hashers import check_password

# Create your views here.


def home(request):
    return render(request,'home.html')

def mypage(request):
    user = request.user
    if user.is_superuser:
        return render(request, 'home.html')
    else:
        try:
            profile = Bossprofile.objects.get(user=request.user)
            store = BookStore.objects.get(boss=request.user)
            store_name = store.name
            mystamp = None
            level = None
            next_level = None
            more = None
            cultures = Culture.objects.filter(store=store)
        except Bossprofile.DoesNotExist:
            profile = Normalprofile.objects.get(user=request.user)
            store_name = None
            cultures = None
            mystamp = profile.stampcount()
            level = profile.level
            if level==3:
                next_level = None
            else:
                next_level = level + 1
            more = level*10-mystamp
    scraps = Scrap.objects.filter(user=request.user)
    comments = Comment.objects.filter(user=request.user)
    return render(request,'mypage.html', {
                        'scraps':scraps, 
                        'stamp':mystamp,
                        'level':level,
                        'next':next_level,
                        'more':more,
                        'cultures':cultures,
                        'comments':comments,
                        'user':user,
                        'profile':profile, 
                        'store_name':store_name,
                        'comments':comments,
                        })

def stamppush(request):
    userid = request.GET['userid']
    try:
        user = User.objects.get(username=userid)
        profile = Normalprofile.objects.get(user=user)
    except:
        url = "http://127.0.0.1:8000/"+"main/mypage/"
        msg = '<script type="text/javascript">alert("존재하지 않는 회원이거나 일반회원이 아닙니다."); location.href="abc";</script>'
        msg2 = msg.replace('abc',url)
        return HttpResponse(msg2)
    count = request.GET['count']
    store = BookStore.objects.get(boss=request.user)
    stamp = Stamp(user=user, store=store, count=count)
    stamp.save()
    s_count = profile.stampcount()
    if s_count >= 20 :
        level = 3
    elif s_count >= 10 :
        level = 2
    else:
        level = 1
    profile.level = level
    profile.save()
    url = "http://127.0.0.1:8000/"+"main/mypage/"
    msg = '<script type="text/javascript">alert("스탬프가 성공적으로 저장되었습니다."); location.href="abc";</script>'
    msg2 = msg.replace('abc',url)
    return HttpResponse(msg2)

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
                storename = request.POST['storename'].strip()
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

def get_nc(request,tf):
    stamp = Stamp.objects.all()
    stamp_month=[]
    stamp_nc=[]
    stamp_idx=[]
    result={}
    for s in stamp:
        d = str(s.created_at)
        d=d.split()[0]
        date = datetime.strptime(d, "%Y-%m-%d")
        stamp_month.append(date.month)
        profile = Normalprofile.objects.get(user=s.user)
        stamp_nc.append([str(profile.nickname),int(s.count)])
    today = datetime.today().month
    for i,m in enumerate(stamp_month):
        if m == today:
            stamp_idx.append(i)
    if tf == True:
        for i in stamp_idx:
            name = stamp_nc[i][0]
            count = stamp_nc[i][1]
            if name in result:
                result[name] += count
            else:
                result[name] = count
    else:
        for s in stamp_nc:
            name = s[0]
            count = s[1]
            if name in result:
                result[name] += count
            else:
                result[name] = count
    return result

def ranking(request):
    total = get_nc(request,False)
    month = get_nc(request,True)
    total_n=[]
    total_c=[]
    month_n=[]
    month_c=[]
    rank=[total, month]
    name=[total_n, month_n]
    count=[total_c, month_c]
    res_first={}
    res_second={}
    res_third={}
    key_arr=['total_nickname','month_nickname','total_stamp','month_stamp']

    for idx,r in enumerate(rank):
        for i in r.keys():
            name[idx].append(i)
            count[idx].append(r.get(i))

    for idx,cnt in enumerate(count):
        first, second, third = [-1,'없음'], [-1,'없음'], [-1,'없음']
        for i,c in enumerate(cnt):
            if first[0] <= c:
                third = second
                second = first
                first = [c,name[idx][i]]
            elif second[0] <= c:
                third = second
                second = [c,name[idx][i]]
            elif third[0] <= c:
                third = [c,name[idx][i]]
        res_first[key_arr[idx]]=first[1]
        res_first[key_arr[idx+2]]=first[0]
        res_second[key_arr[idx]]=second[1]
        res_second[key_arr[idx+2]]=second[0]
        res_third[key_arr[idx]]=third[1]
        res_third[key_arr[idx+2]]=third[0]
    return render(request,'ranking.html', {'first':res_first, 'second':res_second, 'third':res_third})

def info(request):
    return render(request,'info.html')

def del_user(request):
    request.user.delete()
    auth.logout(request)
    return render(request,'home.html')

def change_pwd(request):
    if request.method == "POST":
        user = request.user
        new_pwd = request.POST.get("password1")
        pwd_confirm = request.POST.get("password2")
        if new_pwd == "":
            return redirect('mypage')
        if new_pwd == pwd_confirm:
            user.set_password(new_pwd)
            user.save()
            auth.login(request,user)
            url = "http://127.0.0.1:8000/"+"main/mypage/"
            msg = '<script type="text/javascript">alert("비밀번호가 성공적으로 변경되었습니다."); location.href="abc";</script>'
            msg2 = msg.replace('abc',url)
            return HttpResponse(msg2)
        else:
            url = "http://127.0.0.1:8000/"+"main/mypage/"
            msg = '<script type="text/javascript">alert("비밀번호가 일치하지 않습니다."); location.href="abc";</script>'
            msg2 = msg.replace('abc',url)
            return HttpResponse(msg2)