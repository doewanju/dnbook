from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from django.contrib.auth.models import User
from .models import BookStore, Scrap, Review, Tag, Crawling
from main.models import Bossprofile
from django.core import serializers
from .review import reviewFuc
import simplejson
from .forms import ReviewForm, StoreEditForm
from django.db.models import Avg
import os


# Create your views here.

def bookstore(request):
    bookstores = BookStore.objects
    return render(request,'bookstore.html', {'bookstores' : bookstores})

def detail(request, bookstore_id):
    edit = None
    introduce = None
    store_detail = get_object_or_404(BookStore, pk = bookstore_id)
    scrap = Scrap.objects.filter(store=store_detail)
    rev = Crawling.objects.filter(store=store_detail)
    tot = 0
    reviews = store_detail.review_set.all().order_by('-created_at')
    for i in store_detail.review_set.all():
        tot += i.star
    if store_detail.review_set.all().count():
        star_avg = '%.1f' %(tot/(store_detail.review_set.all().count()))
    else:
        star_avg = 0
    if store_detail.boss:
        boss = store_detail.boss
        introduce = Bossprofile.objects.get(user=boss).introduce
        if request.user.is_authenticated:
            try:
                login_user = Bossprofile.objects.get(user=request.user).user
                if login_user == boss:
                    edit = True
                else:
                    pass
            except:
                pass
        else:
            pass
    else:
        pass
    if request.user.is_authenticated:
        store_scrap = scrap.filter(user=request.user)
        form = ReviewForm()
        return render(request, 'storedetail.html', {'reviews':reviews,'rev' : rev, 'store' : store_detail, 'scrap' : store_scrap, 'form':form, 'star_avg':star_avg, 'introduce':introduce, 'edit':edit,})
    else:
        return render(request, 'storedetail.html', {'reviews':reviews,'rev' : rev, 'store' : store_detail, 'star_avg':star_avg, 'introduce':introduce, 'edit':edit, })
      
def realmap(request):
    bookstores = BookStore.objects.all()
    addr = []
    name = []
    storepk = []
    for a in bookstores:
        addr.append(a.addr)
        name.append(a.name)
        storepk.append(a.bookstore_id)
    addrlist = simplejson.dumps(addr)
    namelist = simplejson.dumps(name)
    pklist = simplejson.dumps(storepk)
    return render(request, 'realmap.html', {
        'bs':bookstores, 
        'bsaddr' : addrlist, 
        'bsname' : namelist,
        'pklist' : pklist})

def themamap(request):
    thema = Tag.objects.all()
    return render(request, 'themamap.html',{'thema':thema})

def themadetail(request, tag_id):
    thema = get_object_or_404(Tag, pk=tag_id)
    stores = BookStore.objects.filter(tag_set=thema)
    addr = []
    name = []
    storepk = []
    for a in stores:
        addr.append(a.addr)
        name.append(a.name)
        storepk.append(a.bookstore_id)
    addrlist = simplejson.dumps(addr)
    namelist = simplejson.dumps(name)
    pklist = simplejson.dumps(storepk)
    content = {'thema':thema,
            'stores':stores,
            'bsaddr':addrlist,
            'bsname':namelist,
            'pklist':pklist}

    return render(request, 'themadetail.html', content)

def scrap(request, bookstore_id):
    store = get_object_or_404(BookStore, pk=bookstore_id)
    scrapped = Scrap.objects.filter(user=request.user, store=store)
    if not scrapped:
        Scrap.objects.create(user=request.user, store=store)
    else:
        scrapped.delete()
    #return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    return redirect('storedetail', bookstore_id=bookstore_id)

def reviewcreate(request, bookstore_id):
    store = get_object_or_404(BookStore, pk=bookstore_id)
    if request.method=='POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            star=request.POST["star"]
            review.star = star
            review.user = request.user
            review.store = store
            review.save()
            return redirect('storedetail', bookstore_id=bookstore_id)
        else:
            redirect('bookstore')
    else:
        return redirect('storedetail', bookstore_id=bookstore_id)

def reviewdelete(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    review.delete()
    return redirect('storedetail', bookstore_id=review.store.pk)

def listsearch(request):
    bookstores = BookStore.objects
    query = request.GET.get('query','')
    if query:
        stype = request.GET['searchtype']
        if stype == 'searchname':
            bookstores = bookstores.filter(name__contains=query)
            return render(request,'bookstore.html', {'bookstores' : bookstores})
        else:
            bookstores = bookstores.filter(addr__contains=query)
            return render(request,'bookstore.html', {'bookstores' : bookstores})

def mapsearch(request):
    bookstores = BookStore.objects.all()
    query = request.GET.get('query','')
    if query:
        stype = request.GET['searchtype']
        if stype == 'searchname':
            bookstores = bookstores.filter(name__contains=query)
        else:
            bookstores = bookstores.filter(addr__contains=query)
        addr = []
        name = []
        storepk = []
        for a in bookstores:
            addr.append(a.addr)
            name.append(a.name)
            storepk.append(a.bookstore_id)
        addrlist = simplejson.dumps(addr)
        namelist = simplejson.dumps(name)
        pklist = simplejson.dumps(storepk)
        return render(request, 'realmap.html', {
            'bs':bookstores, 
            'bsaddr' : addrlist, 
            'bsname' : namelist,
            'pklist' : pklist})

def store_edit(request, bookstore_id):
    store = get_object_or_404(BookStore, pk=bookstore_id)
    if store.img:
        pic=store.img.path
    else:
        pic=None

    if request.method=='POST':
        form = StoreEditForm(request.POST, request.FILES, instance=store)
        if request.FILES and pic:
            os.remove(pic)
        if form.is_valid():
            intro = request.POST['introduce'] 
            b = Bossprofile.objects.get(user=store.boss)
            b.introduce = intro
            b.save()

            editing = form.save(commit=False)
            editing.save()
            return redirect('storedetail', bookstore_id=bookstore_id)
        else:
            return redirect('bookstore') #폼이 유효하지 않은 경우 처리하기
    else:
        form = StoreEditForm(instance=store)
        b = Bossprofile.objects.get(user=store.boss)
        introduce = b.introduce
        return render(request,'store_edit.html', {'form' : form, 'store' : store, 'introduce':introduce})