from django.core.cache import cache
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from custom.exception import CustomException

User = get_user_model()


class CustomBackend(ModelBackend):
    """
    验证用户
    """
    def authenticate(self, request, username=None, password=None, code=None, mobile=None, **kwargs):
        if code and mobile:
            return self.check_by_code(code, mobile)
        if username and password:
            return self.check_by_password(username, password)

    def check_by_code(self, code, mobile):
        # 通过手机号获取缓存
        verify_records = cache.get(mobile)

        if not verify_records:
            raise CustomException(code=4111, message='验证码失效')
        if verify_records[0] != 2:
            raise CustomException(code=4112, message='验证码类型错误')
        if verify_records[1] != code:
            raise CustomException(code=4113, message='验证码错误')

        user = User.objects.get_or_404(mobile=mobile)
        return user

    def check_by_password(self, username, password):
        # 做并集进行查询
        user = User.objects.filter(Q(username=username) | Q(mobile=username)).first()
        if not user:
            raise CustomException(code=4114, message='用户不存在')
        if not user.check_password(password):
            raise CustomException(code=4115, message='密码错误')
        if not self.user_can_authenticate(user):
            raise CustomException(code=4116, message='账户不可用')

        return user
