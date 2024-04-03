from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import UserForm

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        print(form.username, form.password)
        if form.is_valid():
            # 사용자를 직접 저장하고, 패스워드를 해싱하여 저장
            user = form.save(commit=False)
            user.deal_count = 0
            user.save()

            # 회원가입된 사용자로 로그인을 시도
            print(user.password)
            login(request, user)
            return redirect('deal:index')
    else:
        form = UserForm()
    return render(request, 'user/signup.html', {'form': form})