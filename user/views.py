from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render, redirect, get_object_or_404

from deal.models import Deal
from .forms import UserForm
from .models import User


def anonymous_required(function=None, redirect_url=None):
    if not redirect_url:
        redirect_url = '/'  # 로그인한 사용자를 리디렉션할 URL

    actual_decorator = user_passes_test(
        lambda user: not user.is_authenticated,
        login_url=redirect_url
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


@anonymous_required()
def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            # 사용자를 직접 저장하고, 패스워드를 해싱하여 저장
            user = form.save(commit=False)
            user.set_password(request.POST["password"])
            user.email = request.POST["email"]
            user.deal_count = 0
            user.save()

            # 회원가입된 사용자로 로그인을 시도
            login(request, user)
            return redirect('deal:index')
    else:
        form = UserForm()
    return render(request, 'user/signup.html', {'form': form})


@login_required(login_url='user:login')
def myinfo(request):
    deal_list = Deal.objects.filter(author=request.user)
    context = {
        'user': request.user,
        'deal_list': deal_list
    }
    return render(request, 'user/myinfo.html', context)


def user_info(request, pk):
    user = get_object_or_404(User, pk=pk)
    deals = Deal.objects.filter(author=user)
    context = {
        'user': user,
        'deals': deals
    }
    return render(request, 'user/user_info.html', context)


#이메일 인증
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse


def send_verification_email(request):
    user = request.user
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    link = request.build_absolute_uri(
        reverse('user:activate_user', kwargs={'uidb64': uid, 'token': token})
    )
    subject = 'Activate your account'
    message = f'Please click the link to activate your account: {link}'
    send_mail(subject, message, 'admin@example.com', [user.email])
    return redirect('user:myinfo')


def activate_user(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_certified = True
        user.save()
        return render(request, 'user/activation_complete.html')
    return render(request, 'user/activation_invalid.html')