from django.shortcuts import render, get_object_or_404
from .models import Culture

# Create your views here.
def board(request):
    cultures=Culture.objects
    return render(request,'board.html', {'cultures' : cultures})

def detail(request, culture_id):
    culture_detail = get_object_or_404(Culture, pk = culture_id)
    return render(request,'culturedetail.html', {'culture' : culture_detail})

def guide(request):
    return render(request,'guide.html')