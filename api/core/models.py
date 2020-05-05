from django.db import models

from custom.model import BaseModel

# Create your models here.


class TalkRecord(BaseModel):

    talk = models.CharField(max_length=256, null=True, blank=True, verbose_name='请求')
    result = models.CharField(max_length=256, null=True, blank=True, verbose_name='回复')
    user_id = models.IntegerField(null=True, blank=True, verbose_name='用户ID')
    user_ip = models.CharField(max_length=100, null=True, blank=True, verbose_name='用户IP')
    username = models.CharField(max_length=10, null=True, blank=True, verbose_name='用户名称')

    class Meta:
        verbose_name = '对话记录'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.username}:{self.request}'
