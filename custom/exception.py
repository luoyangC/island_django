import logging

from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException

from custom.response import JsonResponse

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    code = 9999
    message = '未知异常'
    detail = None
    logger.error('error：{}'.format(exc))
    if isinstance(exc, CustomException):
        code = exc.detail['code']
        message = exc.detail['message']
        detail = exc.detail['detail']
    else:
        response = exception_handler(exc, context)
        if response is not None:
            if response.status_code == 404:
                code = 4004
                message = "资源未找到"
            elif response.status_code == 400:
                code = 4000
                message = '请求参数错误'
            elif response.status_code == 401:
                code = 4001
                message = '用户身份验证失败'
            elif response.status_code == 403:
                code = 4003
                message = "用户无此操作权限"
            elif response.status_code == 405:
                code = 4005
                message = '请求方式错误'
            elif response.status_code >= 500:
                code = 5000
                message = "服务器错误"

            detail = response.data

    return JsonResponse(code=code, message=message, detail=detail)


class CustomException(APIException):
    default_detail = ''
    default_code = 4000
    default_message = ''

    def __init__(self, detail=None, code=None, message=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code
        if message is None:
            message = self.default_message

        self.detail = {'code': code, 'message': message, 'detail': detail}
