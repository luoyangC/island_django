# Generated by Django 3.0.1 on 2020-05-04 04:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('content', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('delete_at', models.DateTimeField(blank=True, null=True, verbose_name='删除时间')),
                ('content', models.TextField(verbose_name='评论内容')),
                ('like_nums', models.IntegerField(default=0, verbose_name='点赞数')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='content.Article', verbose_name='评论的文章')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='评论者')),
            ],
            options={
                'verbose_name': '评论',
                'verbose_name_plural': '评论',
            },
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('delete_at', models.DateTimeField(blank=True, null=True, verbose_name='删除时间')),
                ('content', models.TextField(verbose_name='回复内容')),
                ('like_nums', models.IntegerField(default=0, verbose_name='点赞数')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='action.Comment', verbose_name='评论')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reply_from', to=settings.AUTH_USER_MODEL, verbose_name='发送者')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reply_to', to=settings.AUTH_USER_MODEL, verbose_name='发送者')),
            ],
            options={
                'verbose_name': '回复',
                'verbose_name_plural': '回复',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('delete_at', models.DateTimeField(blank=True, null=True, verbose_name='删除时间')),
                ('content', models.TextField(verbose_name='留言信息')),
                ('anonymous', models.BooleanField(default=True, verbose_name='是否匿名')),
                ('creator', models.ForeignKey(default=999, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='留言者')),
            ],
            options={
                'verbose_name': '留言',
                'verbose_name_plural': '留言',
            },
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('delete_at', models.DateTimeField(blank=True, null=True, verbose_name='删除时间')),
                ('like_id', models.IntegerField(verbose_name='被点赞的ID')),
                ('like_type', models.CharField(choices=[('article', '文章'), ('comment', '评论'), ('reply', '回复')], max_length=7, verbose_name='点赞类型')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '点赞',
                'verbose_name_plural': '点赞',
            },
        ),
        migrations.CreateModel(
            name='Fav',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('delete_at', models.DateTimeField(blank=True, null=True, verbose_name='删除时间')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='faves', to='content.Article', verbose_name='收藏的文章')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='faves', to=settings.AUTH_USER_MODEL, verbose_name='收藏的用户')),
            ],
            options={
                'verbose_name': '收藏',
                'verbose_name_plural': '收藏',
            },
        ),
    ]
