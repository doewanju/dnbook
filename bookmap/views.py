from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from .models import BookStore, Scrap
from django.core import serializers
import simplejson

# Create your views here.

def bookstore(request):
    bookstores = BookStore.objects
    return render(request,'bookstore.html', {'bookstores' : bookstores})

def detail(request, bookstore_id):
    store_detail = get_object_or_404(BookStore, pk = bookstore_id)
    scrap = Scrap.objects.filter(user=request.user, store=store_detail)
    return render(request, 'storedetail.html', {'store' : store_detail, 'scrap' : scrap})

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
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))