from django.shortcuts import render, get_object_or_404, redirect
from .models import Culture, Comment
from .forms import CommentForm
# Create your views here.
def board(request):
    cultures=Culture.objects
    return render(request, 'board.html', {'cultures':cultures})

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