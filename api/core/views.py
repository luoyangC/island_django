from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework_jwt.views import JSONWebTokenAPIView
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from core.serializers import SMSCodeSerializer, CustomTokenSerializer, TalkRecordSerializer
from custom.exception import CustomException
from custom.response import JsonResponse
from utils.ali_sms import send_sms
from utils.tulin_talk import talk
from utils.tools import get_client_ip
from utils.ali_oss import get_oss_token


class TulinTalkApiView(GenericAPIView):
    """
    图灵机器人接口
    """
    permission_classes = ()
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = TalkRecordSerializer

    def post(self, request, *args, **kwargs):

        result = talk(request.data['talk'], request.data['username'])
        user_id = self.request.user.id or 0
        user_ip = get_client_ip(request)

        serializer = self.get_serializer(data={
            'talk': request.data['talk'],
            'username': request.data['username'],
        })
        serializer.is_valid(raise_exception=True)
        serializer.save(result=result, user_id=user_id, user_ip=user_ip)
        return JsonResponse({'result': result})


class SMSCodeAPIView(GenericAPIView):
    """
    发送短信验证码
    """
    permission_classes = ()
    authentication_classes = ()
    serializer_class = SMSCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mobile = serializer.validated_data['mobile']
        send_type = serializer.validated_data['type']
        res = send_sms(mobile, send_type)
        if res['code'] != 'OK':
            raise CustomException(code=4103, message=res['message'])
        return JsonResponse(message='短信发送成功')


class CustomTokenAPIView(JSONWebTokenAPIView):
    """
    获取token
    """
    permission_classes = ()
    authentication_classes = ()
    serializer_class = CustomTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data.get('user') or request.user
        token = serializer.validated_data.get('token')
        return JsonResponse({'user': user, 'token': token})


class GetAliOSSToken(GenericAPIView):

    permission_classes = ()
    authentication_classes = ()
    pagination_class = None

    def get(self, request, *args, **kwargs):
        res = get_oss_token()
        return JsonResponse(res)


send_sms_code = SMSCodeAPIView.as_view()
get_token = CustomTokenAPIView.as_view()
tulin_talk = TulinTalkApiView.as_view()
get_upload_token = GetAliOSSToken.as_view()
