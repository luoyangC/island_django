from django.db import models

from custom.model import BaseModel

# Create your models here.


class Like(BaseModel):
    """
    用户点赞
    """
    LIKE_TYPE = (
        ('article', '文章'),
        ('comment', '评论'),
        ('reply', '回复')
    )
    user = models.ForeignKey('user.UserProfile', on_delete=models.CASCADE, verbose_name='用户')
    like_id = models.IntegerField(verbose_name='被点赞的ID')
    like_type = models.CharField(max_length=7, choices=LIKE_TYPE, verbose_name='点赞类型')

    class Meta:
        verbose_name = '点赞'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.like_id)


class Fav(BaseModel):
    """
    用户收藏
    """
    article = models.ForeignKey('content.Article', related_name='faves', on_delete=models.CASCADE, verbose_name='收藏的文章')
    user = models.ForeignKey('user.UserProfile', related_name='faves', on_delete=models.CASCADE, verbose_name='收藏的用户')

    class Meta:
        verbose_name = '收藏'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.article.title


class Comment(BaseModel):
    """
    用户评论
    """
    content = models.TextField(verbose_name='评论内容')
    like_nums = models.IntegerField(default=0, verbose_name='点赞数')

    article = models.ForeignKey('content.Article', related_name='comments', on_delete=models.CASCADE, verbose_name='评论的文章')
    creator = models.ForeignKey('user.UserProfile', related_name='comments', on_delete=models.CASCADE, verbose_name='评论者')

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content


class Reply(BaseModel):
    """
    用户回复
    """
    content = models.TextField(verbose_name='回复内容')
    like_nums = models.IntegerField(default=0, verbose_name='点赞数')

    comment = models.ForeignKey('Comment', related_name='replies', on_delete=models.CASCADE, verbose_name='评论')
    creator = models.ForeignKey('user.UserProfile', on_delete=models.CASCADE, related_name='reply_from', verbose_name='发送者')
    receiver = models.ForeignKey('user.UserProfile', on_delete=models.CASCADE, related_name='reply_to', verbose_name='发送者')

    class Meta:
        verbose_name = '回复'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content


class Message(BaseModel):
    """
    留言
    """
    content = models.TextField(verbose_name='留言信息')
    anonymous = models.BooleanField(default=True, verbose_name='是否匿名')
    creator_ip = models.CharField(max_length=100, null=True, blank=True, verbose_name='留言者IP')

    creator = models.ForeignKey('user.UserProfile', default=999, on_delete=models.CASCADE, verbose_name='留言者')

    class Meta:
        verbose_name = '留言'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content
