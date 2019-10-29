from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from django.contrib.auth.models import User
from .models import BookStore, Scrap, Review
from main.models import Bossprofile
from django.core import serializers
from .review import reviewFuc
import simplejson
from .forms import ReviewForm
from django.db.models import Avg

# Create your views here.

def bookstore(request):
    bookstores = BookStore.objects
    return render(request,'bookstore.html', {'bookstores' : bookstores})

def detail(request, bookstore_id):
    introduce = None
    store_detail = get_object_or_404(BookStore, pk = bookstore_id)
    scrap = Scrap.objects.filter(store=store_detail)
    rev = " "
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
                    edit = None
            except:
                edit = None
        else:
            edit = None
    else:
        edit = None
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

def crawling(request, bookstore_id):
    store_detail = get_object_or_404(BookStore, pk = bookstore_id)
    rev=reviewFuc(store_detail.name,store_detail.addr)
    scrap = Scrap.objects.filter(store=store_detail)
    scrap_count = scrap.count()

    tot = 0
    for i in store_detail.review_set.all():
        tot += i.star
    if store_detail.review_set.all().count():
        star_avg = '%.1f' %(tot/(store_detail.review_set.all().count()))
    else:
        star_avg = 0
    
    if request.user.is_authenticated:
        store_scrap = scrap.filter(user=request.user)
        form = ReviewForm()
        return render(request, 'storedetail.html', {'rev' : rev, 'store' : store_detail, 'scrap' : store_scrap, 'count':scrap_count, 'form':form, 'star_avg':star_avg})
    else:
        return render(request, 'storedetail.html', {'rev' : rev, 'store' : store_detail, 'count' : scrap_count, 'star_avg':star_avg})

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

def csstest(request):
    return render(request,'csstest.html')

def edit_intro(request, bookstore_id):
    edit=True
    return render(request, 'result.html',{'edit':edit, 'id':bookstore_id})

def edit_save(request, bookstore_id):
    book = get_object_or_404(BookStore, pk = bookstore_id)
    intro = request.GET['introduce'] 
    boss = book.boss
    b = Bossprofile.objects.get(user=boss)
    b.introduce = intro
    b.save()
    return redirect('storedetail', bookstore_id=bookstore_id)