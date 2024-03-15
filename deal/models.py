from django.db import models
from user.models import User


class Deal(models.Model):
    author      = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='user_deal', null=True)
    subject     = models.CharField(max_length=200)
    content     = models.TextField()
    price       = models.IntegerField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    is_complete = models.BooleanField(auto_created=False)


class DealFile(models.Model):   # 게시글 사진
    image   = models.FileField(upload_to='deal/', null=True, blank=True)
    deal    = models.ForeignKey(Deal, on_delete=models.CASCADE, related_name='images')


class DealTage(models.Model):   # 게시글 태그
    tag     = models.CharField(max_length=10)
    deal    = models.ForeignKey(Deal, on_delete=models.CASCADE, related_name='tags')