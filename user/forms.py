from django import forms
from .models import User
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model

class UserForm(forms.ModelForm):
    password = forms.CharField(label='비밀번호', widget=forms.PasswordInput)
    re_password = forms.CharField(label='비밀번호 확인', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'nickname', 'phone_number']
        labels = {
            'password': '비밀번호',
            're_password': '비밀번호 확인',
            'nickname': '닉네임',
            'username': '학번',
            'phone_number': '휴대폰 번호'
        }

    def clean_re_password(self):
        cd = self.cleaned_data
        password = cd.get("password")
        re_password = cd.get("re_password")
        if password and re_password and password != re_password:
            raise forms.ValidationError('비밀번호가 일치하지 않습니다.')

        return cd['re_password']

class UpdateForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ["username", "nickname", "email", "phone_number"]