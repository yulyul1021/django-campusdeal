from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import UserForm
from django.contrib import messages

'''
def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # 로그인 후 이동할 페이지로 redirect
            return redirect('index')
        else:
            # 인증 실패 시 에러 처리
             messages.error(request, 'Invalid username or password. Please try again.')
             return render(request, 'user/login.html')
    else:
        # GET 요청 시 로그인 폼 보여주기
        return render(request, 'user/login.html')
'''
def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            # 사용자를 직접 저장하고, 패스워드를 해싱하여 저장
            user = form.save(commit=False)
            user.deal_count = 0
            user.save()

            # 회원가입된 사용자로 로그인을 시도
            login(request, user)
            return redirect('deal:index')
    else:
        form = UserForm()
    return render(request, 'user/signup.html', {'form': form})