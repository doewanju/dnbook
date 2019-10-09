from django.shortcuts import render, get_object_or_404
from .models import BookStore
from django.core import serializers
from .review import reviewFuc
import simplejson

# Create your views here.

def bookstore(request):
    bookstores = BookStore.objects
    return render(request,'bookstore.html', {'bookstores' : bookstores})

def detail(request, bookstore_id):
    store_detail = get_object_or_404(BookStore, pk = bookstore_id)
    rev=reviewFuc(store_detail.name,store_detail.addr)
    return render(request, 'storedetail.html', {'store' : store_detail, 'rev':rev})

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