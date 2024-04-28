from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from deal.models import Deal
from .forms import UserForm
from .models import User

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            # 사용자를 직접 저장하고, 패스워드를 해싱하여 저장
            user = form.save(commit=False)
            user.is_active = False
            user.set_password(request.POST["password"])
            user.deal_count = 0
            user.save()

            # 회원가입된 사용자로 로그인을 시도
            login(request, user)
            return redirect('deal:index')
    else:
        form = UserForm()
    return render(request, 'user/signup.html', {'form': form})


def info(request):
    deals = Deal.objects.filter(author=request.user)
    context = {
        'user': request.user,
        'deals': deals
    }
    return render(request, 'user/information.html', context)