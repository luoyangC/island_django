from django.core.cache import cache
from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from custom.exception import CustomException
from core.models import TalkRecord
from user.serializers import UserDetailSerializer

User = get_user_model()
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER


class SMSCodeSerializer(serializers.Serializer):

    SEND_TYPE = (
        (1, 'register'),
        (2, 'login'),
        (0, 'other'),
    )

    mobile = serializers.CharField(label='手机号')
    type = serializers.ChoiceField(choices=SEND_TYPE, label='验证码类型')

    def validate(self, attrs):
        if cache.get(attrs['mobile']):
            raise CustomException(code='4100', message='距离上次发生不足1分钟，或稍后再试')
        if attrs['type'] == 1:
            if User.objects.filter(mobile=attrs['mobile']).count():
                raise CustomException(code='4101', message='该手机号已存在')
        elif attrs['type'] == 2:
            if not User.objects.filter(mobile=attrs['mobile']).count():
                raise CustomException(code='4102', message='用户不存在')
        return attrs


class CustomTokenSerializer(serializers.Serializer):

    username = serializers.CharField(required=False, label='用户名')
    password = serializers.CharField(required=False, label='密码')

    code = serializers.CharField(required=False, max_length=6, min_length=6, label='验证码')
    mobile = serializers.CharField(required=False, max_length=11, min_length=11, label='手机号')

    def validate(self, attrs):
        user = None
        by_password = {
            'username': attrs.get('username'),
            'password': attrs.get('password')
        }
        by_code = {
            'mobile': attrs.get('mobile'),
            'code': attrs.get('code')
        }
        if not all(by_password.values()) and not all(by_code.values()):
            raise CustomException(code=4110, message='参数错误')

        if all(by_password.values()):
            user = authenticate(**by_password)
        elif all(by_code.values()):
            user = authenticate(**by_code)

        payload = jwt_payload_handler(user)
        return {'token': jwt_encode_handler(payload), 'user': UserDetailSerializer(user).data}


class TalkRecordSerializer(serializers.ModelSerializer):

    talk = serializers.CharField(required=True, label='请求')
    result = serializers.CharField(read_only=True, label='回复')
    username = serializers.CharField(required=True, label='用户名')

    class Meta:
        model = TalkRecord
        fields = ('talk', 'result', 'username')
