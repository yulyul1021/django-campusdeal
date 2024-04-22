from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404,redirect
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Deal
from .forms import DealForm


def index(request):
    deal_list = Deal.objects.order_by('-create_date')
    context = {'deal_list':deal_list}
    return render(request, 'deal/deal_list.html',context)

# deal 목록 페이지
def deal_list_detail(request):
    deal_list = Deal.objects.order_by('-create_date')
    context = {'deal_list':deal_list}
    return render(request,'deal/deal_list_detail.html',context)

#deal 상품 상세 페이지
def detail(request,deal_id):
    deal = Deal.objects.get(id=deal_id)
    context = {'deal':deal}
    return render(request,'deal/deal_detail.html',context)

# 글쓰기, 수정, 삭제
@login_required(login_url='user:login')
def deal_create(request):
    if request.method == 'POST':
        form = DealForm(request.POST, request.FILES)
        if form.is_valid():
            deal = form.save(commit=False)
            deal.author = request.user
            deal.create_date = timezone.now()
            deal.is_complete = False
            try:
                deal.image = request.FILES['image']
            except:
                deal.image = None
            deal.save()
            return redirect('deal:index')
    else:
        form=DealForm()
    context = {'form':form}
    return render(request, 'deal/deal_form.html',context)

@login_required(login_url='user:login')
def deal_edit(request,deal_id):
    deal = get_object_or_404(Deal,pk=deal_id)
    if request.user != deal.author:
        messages.error(request,'수정권한이 없습니다')
        return redirect('deal:deal_detail',deal_id=deal.id)
    if request.method == "POST":
        form = DealForm(request.POST, instance=deal)
        if form.is_valid():
            deal = form.save(commit=False)
            deal.modify_date = timezone.now()
            deal.save()
            return redirect('deal:deal_detail',deal_id=deal.id)
    else:
        form = DealForm(instance=deal)
    context = {'form':form}
    return render(request,'deal/deal_form.html',context)

@login_required(login_url='user:login')
def deal_delete(request, deal_id):
    deal = get_object_or_404(Deal, pk=deal_id)
    if request.user != deal.author:
        messages.error(request,'삭제권한이 없습니다')
        return redirect('deal:deal_detail',deal_id=deal.id)
    deal.delete()
    return redirect('deal:index')