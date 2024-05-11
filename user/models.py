from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

class User(AbstractUser):
    username        = models.CharField(max_length=8, unique=True)  # 학번(ID): 기존 student_id(학번)이라고 생각.
    nickname        = models.CharField(max_length=10, unique=True) # 닉네임
    icon            = models.FileField(default="default/icon.png", upload_to='icon/', null=True, blank=True) # 프로필사진
    phone_number    = models.CharField( # default="default/icon.png", 
                        max_length=11,
                        unique=True,
                        validators=[
                            RegexValidator(
                                regex=r'^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})',
                                message="010-1234-5678 형식이어야 합니다."
                            ),
                        ],
                    )
    deal_count      = models.IntegerField(default=0) # 거래횟수

    def __str__(self):
        return self.username

