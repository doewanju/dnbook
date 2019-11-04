from django.shortcuts import render, get_object_or_404, redirect
from .models import Culture, Comment
from bookmap.models import BookStore
from main.models import Bossprofile, Normalprofile
from .forms import CommentForm, CultureForm
from el_pagination.views import AjaxListView
# Create your views here.

def board(request):
    cultures=Culture.objects.order_by('-write_date')
    key = False
    if request.user.is_authenticated:
        try:
            Bossprofile.objects.get(user=request.user)
            key = True
        except Bossprofile.DoesNotExist:
            key = False
    return render(request, 'board.html', {'cultures':cultures, 'key':key})

def entry_index(reuqest, template='others/board.html'):
    context = {
        'cultures' : Culture.objects.all().order_by('-write_date'),
    }
    return render(request, template, context)

def detail(request, culture_id):
    culture_detail = get_object_or_404(Culture, pk = culture_id)
    comments = culture_detail.comment_set.all().order_by('-created_at')
    if request.user.is_authenticated:
        form = CommentForm()
        return render(request, 'culturedetail.html', {'comments':comments,'culture':culture_detail, 'form':form})
    else:
        return render(request,'culturedetail.html', {'comments':comments,'culture' : culture_detail})
    

def guide(request):
    return render(request,'guide.html')

def commentcreate(request, culture_id):
    culture = get_object_or_404(Culture, pk=culture_id)
    if request.method=='POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.culture = culture
            comment.user = request.user
            comment.save()
            return redirect('culturedetail', culture_id=culture.pk)
        else:
            redirect('board')
    else:
        form = CommentForm()
        return render(request, 'culturedetail.html', {'form':form, 'culture':culture})
    
def commentdelete(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.delete()
    return redirect('culturedetail', culture_id=comment.culture.pk)

def new(request):
    return render(request, 'boardnew.html')

def boardcreate(request):
    if request.method=='POST':
        form = CultureForm(request.POST, request.FILES)
        storename = request.POST['storename']
        bookstore = BookStore.objects.get(name=storename)
        if form.is_valid(): 
            post = form.save(commit=False)
            post.store = bookstore
            post.save()
            return redirect('culturedetail', culture_id=post.pk)
        else:
            return redirect('board')
    else:
        form = CultureForm()
        storename = BookStore.objects.get(boss=request.user)
        return render(request, 'boardnew.html', {'form':form, 'storename':storename})


def boardsearch(request):
    key = False
    if request.user.is_authenticated:
        try:
            profile = Bossprofile.objects.get(user=request.user)
            key = True
        except Bossprofile.DoesNotExist:
            key = False
        
    query = request.GET.get('query','')

    if query:
        culture = Culture.objects.filter(title__contains=query)
    return render(request, 'board.html', {'cultures':culture, 'key':key})