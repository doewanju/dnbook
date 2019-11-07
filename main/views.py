from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.models import User
from django.contrib import auth
from .models import Normalprofile, Bossprofile
from bookmap.models import BookStore, Scrap, Stamp
from others.models import Culture, Comment
from datetime import datetime
from django.contrib.auth.hashers import check_password
import os
from .forms import AddstoreForm
import requests

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
        message = "존재하지 않는 회원이거나 일반회원이 아닙니다."
        return render(request,'popup.html',{'message':message})
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
    message = "스탬프가 성공적으로 저장되었습니다."
    return render(request,'popup.html',{'message':message})

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

def get_stamp_info(request,tf):
    stamp = Stamp.objects.all()
    stamp_month = []
    stamp_ic = []
    stamp_idx = []
    user_img = {}
    user_nick = {}
    user_count = {}
    result = {}
    for s in stamp:
        d = str(s.created_at)
        d=d.split()[0]
        date = datetime.strptime(d, "%Y-%m-%d")
        stamp_month.append(date.month)
        stamp_ic.append([str(s.user), int(s.count)])
        profile = Normalprofile.objects.get(user=s.user)
        try:
            user_img[str(s.user)] = profile.profileimg
        except:
            user_img[str(s.user)] = None
        user_nick[str(s.user)]=profile.nickname
    today = datetime.today().month
    for i,m in enumerate(stamp_month):
        if m == today:
            stamp_idx.append(i)
    if tf == True:
        for i in stamp_idx:
            name = stamp_ic[i][0]
            count = stamp_ic[i][1]
            if name in user_count:
                user_count[name] += count
            else:
                user_count[name] = count
    else:
        for i,s in enumerate(stamp_ic):
            name = s[0]
            count = s[1]
            if name in user_count:
                user_count[name] += count
            else:
                user_count[name] = count
    result = [user_nick, user_count, user_img]
    return result

def ranking(request):
    total = get_stamp_info(request,False)
    month = get_stamp_info(request, True)
    nickname = [total[0], month[0]]
    count = [total[1], month[1]]
    img = [total[2], month[2]]
    res_first = {}
    res_second = {}
    res_third = {}
    key_arr = ['total_nickname', 'month_nickname', 'total_stamp', 'month_stamp', 'total_img', 'month_img']

    for idx,cnt in enumerate(count): #idx가 0이면 전체, 1이면 월별
        first, second, third = [-1, '없음'], [-1, '없음'], [-1, '없음']
        for k,v in cnt.items(): #k는 id, v는 갯수
            if first[0] <= v:
                third = second
                second = first
                first = [v,k]
            elif second[0] <= v:
                third = second
                second = [v,k]
            elif third[0] <= v:
                third = [v, k]
            else:
                pass
        
        if first != [-1, '없음']:
            nick_f = nickname[idx][first[1]]
            img_f = img[idx][first[1]]
        else:
            nick_f = first[1]
            img_f = None

        if second != [-1, '없음']:
            nick_s = nickname[idx][second[1]]
            img_s = img[idx][second[1]]
        else:
            nick_s = second[1]
            img_s = None

        if third != [-1, '없음']:
            nick_t = nickname[idx][third[1]]
            img_t = img[idx][third[1]]
        else:
            nick_t = third[1]
            img_t = None
            
        res_first[key_arr[idx]] = nick_f
        res_first[key_arr[idx + 2]] = first[0]
        res_first[key_arr[idx + 4]] = img_f
        
        res_second[key_arr[idx]] = nick_s
        res_second[key_arr[idx + 2]] = second[0]
        res_second[key_arr[idx + 4]] = img_s

        res_third[key_arr[idx]] = nick_t
        res_third[key_arr[idx + 2]] = third[0]
        res_third[key_arr[idx + 4]] = img_t

    return render(request,'ranking.html', {'first':res_first, 'second':res_second, 'third':res_third})

def info(request):
    return render(request,'info.html')

def del_user(request):
    user = request.user
    try:
        profile = Bossprofile.objects.get(user=user)
    except:
        profile = Normalprofile.objects.get(user=user)
    if profile.profileimg:
        os.remove(profile.profileimg.path)
    user.delete()
    auth.logout(request)
    return render(request,'home.html')

def user_change(request):
    if request.method == "POST":
        user = request.user
        try:
            new_img = request.FILES['img_file']
            try:
                profile = Bossprofile.objects.get(user=user)
            except:
                profile = Normalprofile.objects.get(user=user)
            if profile.profileimg:
                os.remove(profile.profileimg.path)
            profile.profileimg = new_img
            profile.save()
        except:
            pass
        new_pwd = request.POST.get("password1")
        pwd_confirm = request.POST.get("password2")
        if new_pwd == "":
            if (new_img):
                message = "프로필 사진이 성공적으로 변경되었습니다."
                return render(request,'popup.html',{'message':message})
            else:
                return redirect('mypage')
        if new_pwd == pwd_confirm:
            user.set_password(new_pwd)
            user.save()
            auth.login(request, user)
            message = "비밀번호가 성공적으로 변경되었습니다."
            return render(request,'popup.html',{'message':message})
        else:
            message = "비밀번호가 일치하지 않습니다."
            return render(request,'popup.html',{'message':message})

def addstore(request):
    if request.method == 'POST':
        form = AddstoreForm(request.POST)
        if form.is_valid():
            store = form.save(commit=False)
            check = saup_valid(request, store.saup)
            if check == False:
                content="<script type='text/javascript'>alert('존재하지 않는 사업자 등록번호입니다.');history.back();</script>"
                return HttpResponse(content)
            else:
                pass
            store.name=request.POST['name']
            addr = request.POST['addr']
            detail = request.POST['detail']
            if detail.strip() != "":
                store.addr = addr + " " + detail
            store.site=request.POST['site']
            store.openhour = request.POST['openhour']
            open_tf = request.POST['open_tf']
            if open_tf == '영업시간':
                store.openhour_tf = True
            else:
                store.openhour_tf = False
            store.save()
            return redirect('bossbook')
        else:
            content="<script type='text/javascript'>alert('형식에 맞게 입력하세요');history.back();</script>"
            return HttpResponse(content)
    elif request.method == 'GET':
        form = AddstoreForm()
        return render(request, 'addstore.html', {'form': form})

def saup_valid(request, saup):
    saup = saup.replace("-", "")
    headers = {'Authorization': 'Bearer 5MhIQ5Kb69hXPbCj2coo'}
    url='https://business.api.friday24.com/closedown/'+saup
    response = requests.get(url, headers=headers)
    content = str(response.content)
    if '"state":"normal"' in content:
        return True
    else:
        return False