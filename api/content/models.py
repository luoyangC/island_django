from django.db import models
from mdeditor.fields import MDTextField

from custom.model import BaseModel

# Create your models here.


class Sentence(BaseModel):
    """
    定场诗
    """
    lines = models.TextField()

    class Meta:
        verbose_name = '定场诗'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.lines


class Category(BaseModel):
    """
    分类
    """
    title = models.CharField(max_length=100, verbose_name='分类标题')
    info = models.CharField(max_length=100, null=True, blank=True, verbose_name='描述')

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Article(BaseModel):
    """
    文章
    """
    title = models.CharField(max_length=100, null=False, blank=False, verbose_name='文章标题')
    tags = models.CharField(max_length=100, null=True, blank=True, verbose_name='Tag标签')
    image = models.CharField(max_length=100, null=True, blank=True, verbose_name='顶部图片')
    profile = models.TextField(null=True, blank=True, verbose_name='文章简介')
    content = MDTextField(null=True, blank=True, verbose_name='文章内容')
    view_nums = models.IntegerField(default=0, verbose_name='浏览数')
    like_nums = models.IntegerField(default=0, verbose_name='点赞数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏数')
    comment_nums = models.IntegerField(default=0, verbose_name='评论数')

    creator = models.ForeignKey('user.UserProfile', on_delete=models.CASCADE, verbose_name='作者')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='分类')

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
