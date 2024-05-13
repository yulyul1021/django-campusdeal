from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404,redirect
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Deal
from .forms import DealForm

from django.core.paginator import Paginator
from django.db.models import Q, Case, When, Value, IntegerField


# 검색 기능
def index(request):
    page = request.GET.get('page', '1')  # 페이지
    search = request.GET.get('search', '')  # 검색어
    sort = request.GET.get('sort', 'recent')  # 정렬기준.

    if sort == 'old':
        deal_list = Deal.objects.order_by('create_date')
    elif sort == 'min_price':
        deal_list = Deal.objects.order_by('price')
    elif sort == 'max_price':
        deal_list = Deal.objects.order_by('-price')
    elif sort == 'f_complete':
        deal_list = Deal.objects.order_by('is_complete', '-create_date')
    elif sort == 't_image':
        deal_list = Deal.objects.annotate(
            has_image=Case(
                When(image='', then=Value(0)),
                default=Value(1),
                output_field=IntegerField()
            )
        ).order_by('-has_image', '-create_date')

    else:
        deal_list = Deal.objects.order_by('-create_date')

    if search:
        deal_list = deal_list.filter(
            Q(subject__contains=search) |
            Q(content__contains=search) |
            Q(author__username__contains=search)
        ).distinct()

    paginator = Paginator(deal_list, 8)  # 페이지당 8개씩 보여줌.
    page_obj = paginator.get_page(page)

    context = {'deal_list': page_obj, 'page': page, 'search': search, 'sort': sort}
    return render(request, 'deal/deal_list.html', context)


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

@login_required(login_url='user:login')
def deal_complete(request,deal_id):
    deal = get_object_or_404(Deal, pk=deal_id)
    if request.user != deal.author:
        messages.error(request,'작성자만 변경할 수 있습니다')
        return redirect('deal:deal_detail',deal_id=deal.id)
    if deal.is_complete:
        deal.is_complete=False
    else:
        deal.is_complete = True
    deal.save()
    return redirect('deal:deal_detail',deal_id=deal.id)