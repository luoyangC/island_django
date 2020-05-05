from django.core.cache import cache
from django.contrib.auth import get_user_model
from rest_framework import serializers

from custom.exception import CustomException

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    mobile = serializers.CharField(label='手机号')
    code = serializers.CharField(write_only=True, label='验证码')
    password = serializers.CharField(write_only=True, label='密码')

    def validate_mobile(self, mobile):
        user = User.objects.filter(mobile=mobile).first()
        if user:
            raise CustomException(code=4120, message='手机号存在')
        return mobile

    def validate_code(self, code):
        verify_records = cache.get(self.initial_data['mobile'])
        if code == '960823':  # 通用验证码
            return code
        if not verify_records:
            raise CustomException(code=4121, message='验证码过期')
        if verify_records[0] != 1:
            raise CustomException(code=4122, message='验证码类型错误')
        if verify_records[1] != code:
            raise CustomException(code=4123, message='验证码错误')
        return code

    def validate(self, attrs):
        attrs['username'] = '用户' + attrs['mobile']
        del attrs['code']
        return attrs

    class Meta:
        model = User
        fields = ('mobile', 'code', 'password')


class UserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'mobile', 'email', 'avatar')
