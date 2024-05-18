import re

from django import forms
from django.core.exceptions import ValidationError

from .models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(label='비밀번호', widget=forms.PasswordInput)
    re_password = forms.CharField(label='비밀번호 확인', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'nickname', 'phone_number', 'email']
        labels = {
            'password': '비밀번호',
            're_password': '비밀번호 확인',
            'nickname': '닉네임',
            'username': '학번',
            'phone_number': '휴대폰 번호',
            'email': '이메일'
        }

    # def clean_password(self):
    #     password = self.cleaned_data.get('password')
    #     if len(password) < 10:
    #         raise ValidationError('비밀번호는 10글자 이상이어야 합니다.')
    #     if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
    #         raise ValidationError('비밀번호에는 1자 이상의 특수문자가 포함되어야 합니다.')
    #     return password

    def clean_re_password(self):
        cd = self.cleaned_data
        password = cd.get("password")
        re_password = cd.get("re_password")
        if password and re_password and password != re_password:
            raise forms.ValidationError('비밀번호가 일치하지 않습니다.')

        return cd['re_password']


# class UserEditForm(forms.ModelForm):
