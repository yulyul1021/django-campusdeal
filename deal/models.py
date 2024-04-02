from django.db import models
from user.models import User


class Deal(models.Model):
    author      = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='user_deal', null=True) #작성자
    subject     = models.CharField(max_length=200) # 제목
    content     = models.TextField() # 본문
    price       = models.IntegerField() # 가격
    create_date = models.DateTimeField() # 글 작성시간
    modify_date = models.DateTimeField(null=True, blank=True) # 글 수정시간
    is_complete = models.BooleanField(auto_created=False) # 거래완료 여부


class DealFile(models.Model):   # 게시글 사진
    image   = models.FileField(upload_to='deal/', null=True, blank=True) # 사진 파일
    deal    = models.ForeignKey(Deal, on_delete=models.CASCADE, related_name='images') # 해당 사진이 있는 게시글


class DealTage(models.Model):   # 게시글 태그
    tag     = models.CharField(max_length=10) # 태그
    deal    = models.ForeignKey(Deal, on_delete=models.CASCADE, related_name='tags') # 해당 태그가 달린 게시글