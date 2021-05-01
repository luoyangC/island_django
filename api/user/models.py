from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager

from custom.model import BaseModel, BaseManager


class CustomUserManager(UserManager, BaseManager):

    use_in_migrations = True

    def create(self, username, mobile=None, password=None, **extra_fields):
        return self.create_user(username, mobile, password, **extra_fields)

    def _create_user(self, username, mobile, password, **extra_fields):
        if not mobile:
            raise ValueError('手机号不能为空')
        username = self.model.normalize_username(username)
        user = self.model(username=username, mobile=mobile, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, mobile=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, mobile, password, **extra_fields)

    def create_superuser(self, username, mobile=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, mobile, password, **extra_fields)


class UserProfile(AbstractBaseUser, BaseModel):
    """
    用户信息
    """
    username = models.CharField(
        max_length=100, unique=True, verbose_name='用户名')
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')
    email = models.EmailField(null=True, blank=True,
                              max_length=100, verbose_name='邮箱')
    avatar = models.CharField(null=True, blank=True,
                              max_length=100, verbose_name='头像')

    is_staff = models.BooleanField(default=False, verbose_name='权限状态')
    is_active = models.BooleanField(default=True, verbose_name='账户状态')
    is_superuser = models.BooleanField(default=False, verbose_name='管理员权限')

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['mobile']

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
